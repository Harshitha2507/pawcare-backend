# route/chat.py
from flask import Blueprint, request, jsonify
from models import get_db_connection
import jwt
import config
from functools import wraps

chat_bp = Blueprint('chat', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            if token.startswith('Bearer '):
                token = token.split(" ")[1]
            data = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
            current_user_id = data['user_id']
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
        return f(current_user_id, *args, **kwargs)
    return decorated

@chat_bp.route('/', methods=['GET'])
@token_required
def get_user_chats(current_user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Query to get all chats for a user, including the other person's details
    query = """
        SELECT c.id as chat_id, c.pet_id,
               u.id as other_user_id, u.name as other_user_name,
               p.name as pet_name, p.image as pet_image,
               (SELECT message FROM messages WHERE chat_id = c.id ORDER BY timestamp DESC LIMIT 1) as last_text,
               (SELECT timestamp FROM messages WHERE chat_id = c.id ORDER BY timestamp DESC LIMIT 1) as last_time
        FROM chats c
        JOIN users u ON (c.user1_id = %s AND u.id = c.user2_id) OR (c.user2_id = %s AND u.id = c.user1_id)
        LEFT JOIN pets p ON c.pet_id = p.id
        WHERE c.user1_id = %s OR c.user2_id = %s
        ORDER BY last_time DESC
    """
    cursor.execute(query, (current_user_id, current_user_id, current_user_id, current_user_id))
    chats = cursor.fetchall()
    
    # 🔧 FIX: Serialize datetime objects for JSON
    for chat in chats:
        if chat.get('last_time'):
            chat['last_time'] = str(chat['last_time'])
    
    cursor.close()
    conn.close()
    return jsonify(chats)

@chat_bp.route('/get-messages/<int:chat_id>', methods=['GET'])
@token_required
def get_chat_messages(current_user_id, chat_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Security check: current user must be part of the chat
        cursor.execute("SELECT user1_id, user2_id FROM chats WHERE id = %s", (chat_id,))
        chat = cursor.fetchone()
        if not chat or (chat['user1_id'] != current_user_id and chat['user2_id'] != current_user_id):
            return jsonify({"error": "Unauthorized"}), 403

        # 4️⃣ Load messages ordered by timestamp ASC
        cursor.execute(
            "SELECT * FROM messages WHERE chat_id = %s ORDER BY timestamp ASC",
            (chat_id,)
        )
        messages = cursor.fetchall()
        
        # 🔧 FIX: Serialize datetime objects for JSON
        for msg in messages:
            if msg.get('timestamp'):
                msg['timestamp'] = str(msg['timestamp'])
        
        return jsonify(messages)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@chat_bp.route('/get-or-create-chat', methods=['POST'])
@token_required
def get_or_create_chat(current_user_id):
    data = request.json
    user2_id = data.get('user2_id') # The other user
    pet_id = data.get('pet_id')

    if not user2_id:
        return jsonify({"error": "user2_id is required"}), 400

    user1_id = current_user_id
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # 1️⃣ Check if chat already exists for this pair AND pet context
        if pet_id:
            query = """
                SELECT id FROM chats 
                WHERE ((user1_id = %s AND user2_id = %s) 
                   OR (user1_id = %s AND user2_id = %s))
                  AND pet_id = %s
            """
            cursor.execute(query, (user1_id, user2_id, user2_id, user1_id, pet_id))
        else:
            # Fallback for general chats without pet context
            query = """
                SELECT id FROM chats 
                WHERE ((user1_id = %s AND user2_id = %s) 
                   OR (user1_id = %s AND user2_id = %s))
                  AND pet_id IS NULL
            """
            cursor.execute(query, (user1_id, user2_id, user2_id, user1_id))
            
        existing_chat = cursor.fetchone()
        
        if existing_chat:
            chat_id = existing_chat['id']
        else:
            # Create new chat
            cursor.execute(
                "INSERT INTO chats (user1_id, user2_id, pet_id) VALUES (%s, %s, %s)",
                (user1_id, user2_id, pet_id)
            )
            conn.commit()
            chat_id = cursor.lastrowid
        
        return jsonify({"chat_id": chat_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@chat_bp.route('/messages', methods=['POST'])
@token_required
def send_message(current_user_id):
    data = request.json
    chat_id = data.get('chat_id')
    receiver_id = data.get('receiver_id')
    text = data.get('text')

    if not (chat_id and receiver_id and text):
        return jsonify({"error": "chat_id, receiver_id, and text are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Security check: current user must be part of the chat
        cursor.execute("SELECT id FROM chats WHERE id = %s AND (user1_id = %s OR user2_id = %s)", 
                       (chat_id, current_user_id, current_user_id))
        if not cursor.fetchone():
            return jsonify({"error": "Unauthorized"}), 403

        # Insert message
        cursor.execute(
            "INSERT INTO messages (chat_id, sender_id, receiver_id, message) VALUES (%s, %s, %s, %s)",
            (chat_id, current_user_id, receiver_id, text)
        )
        conn.commit()
        message_id = cursor.lastrowid
        
        # 🟢 Real-time Broadcast via SocketIO
        try:
            from extensions import socketio
            import datetime
            payload = {
                "id": message_id,
                "chat_id": chat_id,
                "sender_id": current_user_id,
                "receiver_id": receiver_id,
                "message": text,
                "text": text,
                "timestamp": datetime.datetime.now().isoformat(),
                "is_real_time": True
            }
            # Broadcast to chat room (for both users currently in the chat)
            room_name = str(chat_id)
            socketio.emit('receive_message', payload, room=room_name, namespace='/')
            
            # Also notify the receiver's personal room (for chat list refresh)
            user_room = f"user_{receiver_id}"
            socketio.emit('new_message_notification', payload, room=user_room, namespace='/')
            
            print(f"🚀 [BROADCAST] Sent message {message_id} to room {room_name} and {user_room} (namespace: /)")
        except Exception as e:
            print(f"⚠️ [BROADCAST] Socket failed: {e}")
        
        return jsonify({"message": "Message sent successfully", "chat_id": chat_id, "id": message_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
