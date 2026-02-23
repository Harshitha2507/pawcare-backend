# app.py
import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from route.auth import auth_bp
from route.pets import pets_bp
from route.users import users_bp
from route.chat import chat_bp
from route.applications import applications_bp
from route.notifications import notifications_bp
from models import get_db_connection
from extensions import socketio

app = Flask(__name__, static_folder='static')
CORS(app)
# allow_eio3=True is CRITICAL for compatibility with flutter socket_io_client 2.x
socketio.init_app(app, cors_allowed_origins="*", async_mode='eventlet', logger=True, engineio_logger=True, allow_eio3=True)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(pets_bp, url_prefix='/pets')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(applications_bp, url_prefix='/applications')
app.register_blueprint(notifications_bp, url_prefix='/notifications')

@app.route('/')
def home():
    return "PawCare Backend is running with SocketIO!"

# ----------------- SOCKET EVENTS -----------------

@socketio.on('join')
def on_join(data):
    chat_id = data.get('chat_id') or data.get('room_id')
    if chat_id:
        room = str(chat_id)
        join_room(room)
        print(f"📡 [SOCKET] USER JOINED CHAT ROOM: {room}")
    else:
        print("⚠️ [SOCKET] Join attempt FAILED: No chat_id provided")

@socketio.on('join_user_room')
def on_join_user_room(data):
    user_id = data.get('user_id') or data.get('id')
    if user_id:
        user_room = f"user_{user_id}"
        join_room(user_room)
        print(f"👤 [SOCKET] USER {user_id} JOINED PERSONAL ROOM: {user_room}")
    else:
        print("⚠️ [SOCKET] Join user room FAILED: No user_id provided")

@socketio.on('send_message')
def handle_message(data):
    chat_id = data.get('chat_id')
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    message_text = data.get('message') or data.get('text')
    room = str(chat_id)

    if not all([chat_id, sender_id, receiver_id, message_text]):
        print("⚠️ Invalid message data received via socket")
        return

    # Save to database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (chat_id, sender_id, receiver_id, message) VALUES (%s, %s, %s, %s)",
            (chat_id, sender_id, receiver_id, message_text)
        )
        conn.commit()
        message_id = cursor.lastrowid
        cursor.close()
        conn.close()

        import datetime
        timestamp_iso = datetime.datetime.now().isoformat()
        
        payload = {
            "id": message_id,
            "chat_id": chat_id,
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message": message_text,
            "text": message_text,
            "timestamp": timestamp_iso
        }
        # 1. Broadcast to chat room (for users currently in the chat)
        emit('receive_message', payload, room=room)
        # 2. Also notify the receiver's personal room (for chat list refresh)
        emit('new_message_notification', payload, room=f"user_{receiver_id}")
        print(f"📡 Broadcasted to room {room} and user_{receiver_id}")
        
    except Exception as e:
        print(f"❌ Socket Error: {e}")

if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0", port=5000)