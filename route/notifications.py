# route/notifications.py
from flask import Blueprint, request, jsonify
from models import get_db_connection

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/', methods=['GET'])
def get_notifications():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Filter: Show Unread OR (Read AND Type='application_update')
    # AND scheduled_at <= NOW() (Don't show future reminders)
    query = """
        SELECT * FROM notifications 
        WHERE (user_id = %s OR user_id IS NULL)
        AND (is_read = FALSE OR type = 'application_update')
        AND (scheduled_at <= NOW())
        ORDER BY created_at DESC
    """
    cursor.execute(query, (user_id,))
    notifications = cursor.fetchall()
    
    for n in notifications:
        if n.get('created_at'):
            n['created_at'] = str(n['created_at'])
        if n.get('scheduled_at'):
            n['scheduled_at'] = str(n['scheduled_at'])
        # application_id is already included because of SELECT *
    
    cursor.close()
    conn.close()
    return jsonify(notifications)

@notifications_bp.route('/<int:notif_id>/read', methods=['PUT'])
def mark_as_read(notif_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = TRUE WHERE id = %s", (notif_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Marked as read"})

@notifications_bp.route('/read-all/', methods=['POST'])
def mark_all_as_read():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE notifications SET is_read = TRUE WHERE user_id = %s OR user_id IS NULL", (user_id,))
        conn.commit()
        return jsonify({"message": "All notifications marked as read", "success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@notifications_bp.route('/', methods=['POST'])
def add_notification():
    data = request.json
    user_id = data.get('user_id')
    title = data.get('title')
    message = data.get('message')
    n_type = data.get('type', 'general')
    scheduled_at = data.get('scheduled_at') # Optional, default NOW() by DB if None

    if not title or not message:
        return jsonify({"error": "Title and message required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if scheduled_at:
            cursor.execute(
                "INSERT INTO notifications (user_id, title, message, type, scheduled_at) VALUES (%s, %s, %s, %s, %s)",
                (user_id, title, message, n_type, scheduled_at)
            )
        else:
             cursor.execute(
                "INSERT INTO notifications (user_id, title, message, type) VALUES (%s, %s, %s, %s)",
                (user_id, title, message, n_type)
            )
        conn.commit()
        return jsonify({"message": "Notification added", "success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
