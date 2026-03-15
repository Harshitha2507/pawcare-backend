# routes/pets.py
from flask import Blueprint, request, jsonify
import models
from models import get_db_connection
import cloudinary
import cloudinary.uploader
import config

# Configure Cloudinary
cloudinary.config(
    cloud_name = config.CLOUDINARY_CLOUD_NAME,
    api_key = config.CLOUDINARY_API_KEY,
    api_secret = config.CLOUDINARY_API_SECRET
)

pets_bp = Blueprint('pets', __name__)

@pets_bp.route('/', methods=['GET'])
def get_pets():
    status = request.args.get('status', 'available')
    lender_id = request.args.get('lender_id')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    import json
    try:
        query = """
            SELECT p.*, u.name as lender_name, u.lender_type 
            FROM pets p 
            LEFT JOIN users u ON p.lender_id = u.id
        """
        params = []
        filters = []
        
        if status != 'all':
            filters.append("COALESCE(p.status, 'available') = %s")
            params.append(status)
            
        if lender_id:
            filters.append("p.lender_id = %s")
            params.append(lender_id)
            
        if filters:
            query += " WHERE " + " AND ".join(filters)
            
        cursor.execute(query, tuple(params))
        pets = cursor.fetchall()
        
        # 🔄 Post-process album (string to list)
        for p in pets:
            if p.get('album'):
                try:
                    p['album'] = json.loads(p['album'])
                except:
                    p['album'] = p['album'].split(',') # Fallback
            else:
                p['album'] = [p['image']] if p.get('image') else []
                
        return jsonify(pets)
    except Exception as e:
        print(f"❌ API ERROR: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@pets_bp.route('/<int:pet_id>/status', methods=['PUT'])
def update_pet_status(pet_id):
    data = request.json
    new_status = data.get("status") # 'available' or 'adopted'
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE pets SET status = %s WHERE id = %s", (new_status, pet_id))
        conn.commit()
        return jsonify({"message": f"Pet status updated to {new_status}"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

import os
import time

@pets_bp.route('/', methods=['POST'])
def add_pet():
    print("📡 [DEBUG] Received add_pet request")
    # Handle both JSON and Form Data (for files)
    try:
        if request.content_type and request.content_type.startswith('multipart/form-data'):
            data = request.form
            file = request.files.get('image')
            print(f"📁 [DEBUG] Form data received: {data.to_dict()}")
            # Save file if exists
            image_url = "https://images.unsplash.com/photo-1543466835-00a7907e9de1" # Default
            if file:
                print(f"☁️ [DEBUG] Attempting Cloudinary upload for: {file.filename}")
                # ☁️ CLOUDINARY UPLOAD (Permanent)
                try:
                    upload_result = cloudinary.uploader.upload(file)
                    image_url = upload_result.get("secure_url")
                    print(f"✅ Cloudinary upload success: {image_url}")
                except Exception as ce:
                    print(f"⚠️ Cloudinary failed: {ce}. Falling back to local storage.")
                    filename = f"{int(time.time())}_{file.filename}"
                    upload_path = os.path.join('static', 'uploads', filename)
                    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                    file.save(upload_path)
                    image_url = f"{request.host_url}static/uploads/{filename}"
        else:
            # Fallback to JSON
            data = request.json
            print(f"📄 [DEBUG] JSON data received: {data}")
            image_url = data.get("image")
    except Exception as e:
        print(f"❌ Error parsing request data: {e}")
        return jsonify({"error": f"Request parsing failed: {e}"}), 400

    name = data.get("name")
    category = data.get("category")
    breed = data.get("breed", "Unknown")
    location = data.get("location", "Local City")
    age = data.get("age")
    sex = data.get("sex")
    color = data.get("color", "Mixed")
    health_status = data.get("health_status", "Healthy")
    description = data.get("description")
    lender_id_raw = data.get("lender_id")
    lender_id = None
    if lender_id_raw and lender_id_raw != "0" and lender_id_raw != "":
        try:
            lender_id = int(lender_id_raw)
        except:
            lender_id = None

    adoption_fee_raw = data.get("adoption_fee", "0")
    try:
        adoption_fee = int(adoption_fee_raw) if adoption_fee_raw else 0
    except:
        adoption_fee = 0
    
    print(f"📝 [DEBUG] Preparing to insert pet: {name}, lender: {lender_id}, fee: {adoption_fee}")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        print("🗄️ [DEBUG] Database connection successful")
    except Exception as e:
        print(f"❌ DATABASE CONNECTION ERROR: {e}")
        return jsonify({"error": f"Database connection failed: {e}"}), 500

    import json
    try:
        # 🔄 Handle album (list to string)
        album_data = data.get("album")
        album_str = json.dumps(album_data) if isinstance(album_data, list) else None

        print("🔮 [DEBUG] Executing INSERT into pets")
        cursor.execute(
            "INSERT INTO pets (name, category, breed, image, album, location, age, sex, color, health_status, description, lender_id, adoption_fee) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (name, category, breed, image_url, album_str, location, age, sex, color, health_status, description, lender_id, adoption_fee)
        )
        conn.commit()
        print("✅ [DEBUG] Pet inserted successfully")

        # 🔔 Global Notification for New Pet
        try:
            print("🔔 [DEBUG] Creating global notification")
            cursor.execute(
                "INSERT INTO notifications (user_id, title, message, type) VALUES (NULL, %s, %s, 'new_pet')",
                ("New Pet Alert!", f"A new {category} named {name} just joined PawCare!")
            )
            conn.commit()
            print("✅ [DEBUG] Notification created successfully")
        except Exception as ne:
            print(f"⚠️ Warning: Could not create global notification: {ne}")

        return jsonify({"message": "Pet added successfully", "image_url": image_url})
    except Exception as e:
        if conn: conn.rollback()
        print(f"❌ DB ERROR in add_pet: {e}")
        return jsonify({"error": f"Database operation failed: {e}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        print("🔌 [DEBUG] Database connection closed")

@pets_bp.route('/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM pets WHERE id = %s", (pet_id,))
        conn.commit()
        return jsonify({"message": "Pet removed successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()