# routes/users.py
from flask import Blueprint, request, jsonify
from models import get_db_connection
import hashlib

users_bp = Blueprint('users', __name__)

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, phone FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET name=%s, email=%s, phone=%s WHERE id=%s",
                       (name, email, phone, user_id))
        conn.commit()
        return jsonify({"message": "Profile updated successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@users_bp.route('/<int:user_id>/role', methods=['PUT'])
def update_user_role(user_id):
    data = request.json
    role = data.get("role")
    
    if not role:
        return jsonify({"error": "Role is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET role=%s WHERE id=%s", (role, user_id))
        conn.commit()
        return jsonify({"message": f"Role updated to {role} successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()