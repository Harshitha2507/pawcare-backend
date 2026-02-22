from flask import Blueprint, request, jsonify
import mysql.connector
import config
import hashlib
import jwt
import time

auth_bp = Blueprint("auth", __name__)

from models import get_db_connection

# -----------------------------

# -----------------------------
# Register Route
# -----------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    role = data.get("role", "adopter")

    if not all([name, email, password]):
        return jsonify({"error": "Name, email, and password are required"}), 400

    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, phone, password, role, lender_type, location) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, email, phone, hashed_password, role, data.get("lender_type"), data.get("location"))
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User registered successfully"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Login Route
# -----------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Email and password are required"}), 400

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, hashed_password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            user.pop("password")  # Remove password before sending
            
            # Generate JWT Token
            token = jwt.encode({
                'user_id': user['id'],
                'exp': time.time() + 86400  # 24 hours
            }, config.SECRET_KEY, algorithm='HS256')
            
            return jsonify({"user": user, "token": token}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500