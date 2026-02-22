# route/applications.py
from flask import Blueprint, request, jsonify
from models import get_db_connection

applications_bp = Blueprint('applications', __name__)

@applications_bp.route('/', methods=['POST'])
def create_application():
    data = request.json
    pet_id = data.get('pet_id')
    adopter_id = data.get('adopter_id')
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    message = data.get('message')

    print(f"📥 Received Application: {data}")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO applications (pet_id, adopter_id, applicant_name, applicant_email, phone, address, message) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (pet_id, adopter_id, name, email, phone, address, message)
        )
        conn.commit()
        application_id = cursor.lastrowid
        print(f"✅ Application saved successfully with ID: {application_id}")
        
        # Get pet details and lender_id for notification
        cursor.execute(
            "SELECT p.name as pet_name, p.lender_id FROM pets p WHERE p.id = %s",
            (pet_id,)
        )
        pet_info = cursor.fetchone()
        
        if pet_info and pet_info['lender_id']:
            # Send notification to lender
            lender_id = pet_info['lender_id']
            pet_name = pet_info['pet_name']
            notification_msg = f"New adoption request for {pet_name} from {name}!"
            
            cursor.execute(
                "INSERT INTO notifications (user_id, application_id, title, message, type) VALUES (%s, %s, %s, %s, 'application_request')",
                (lender_id, application_id, "New Adoption Request", notification_msg)
            )
            conn.commit()
            print(f"✅ Notification sent to lender ID: {lender_id}")
        
        return jsonify({"message": "Application submitted successfully"}), 201
    except Exception as e:
        conn.rollback()
        print(f"❌ DB ERROR in create_application: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@applications_bp.route('/', methods=['GET'])
def get_applications():
    lender_id = request.args.get('lender_id')
    adopter_id = request.args.get('adopter_id')
    pet_id = request.args.get('pet_id')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT a.*, p.name as pet_name, p.lender_id,
               lender.name as lender_name, lender.lender_type,
               adopter.name as adopter_name
        FROM applications a 
        JOIN pets p ON a.pet_id = p.id
        LEFT JOIN users lender ON p.lender_id = lender.id
        LEFT JOIN users adopter ON a.adopter_id = adopter.id
    """
    params = []
    
    if lender_id:
        query += " WHERE p.lender_id = %s"
        params.append(lender_id)
    elif adopter_id:
        query += " WHERE a.adopter_id = %s"
        params.append(adopter_id)
    elif pet_id:
        query += " WHERE a.pet_id = %s"
        params.append(pet_id)
        
    print(f"🔍 Fetching applications. Filter: lender_id={lender_id}, pet_id={pet_id}")
    cursor.execute(query, tuple(params))
    apps = cursor.fetchall()
    print(f"✅ Found {len(apps)} applications")

    # 🔧 FIX: Serialize datetime objects for JSON
    for app in apps:
        if app.get('created_at'):
            app['created_at'] = str(app['created_at'])
    
    cursor.close()
    conn.close()
    return jsonify(apps)

@applications_bp.route('/<int:app_id>/status', methods=['PUT'])
def update_application_status(app_id):
    data = request.json
    new_status = data.get('status') # Approved, Rejected
    lender_name = data.get('lender_name', 'A lender')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 1. Update status
        cursor.execute("UPDATE applications SET status = %s WHERE id = %s", (new_status, app_id))
        
        # 2. Get adopter_id and pet_name for notification
        cursor.execute("""
            SELECT a.adopter_id, p.name as pet_name 
            FROM applications a 
            JOIN pets p ON a.pet_id = p.id 
            WHERE a.id = %s
        """, (app_id,))
        app_info = cursor.fetchone()
        
        if app_info:
            adopter_id = app_info['adopter_id']
            pet_name = app_info['pet_name']
            
            # 3. Create Notification
            if new_status == 'Approved':
                msg = f"Request Accepted for {pet_name}!"
                title = "Application Approved"
            else:
                msg = f"We're sorry, your request for {pet_name} was declined."
                title = "Application Declined"

            cursor.execute(
                "INSERT INTO notifications (user_id, application_id, title, message, type) VALUES (%s, %s, %s, %s, 'application_update')",
                (adopter_id, app_id, title, msg)
            )
            
            # 4. If approved and requested, mark pet as adopted
            mark_as_adopted = data.get('mark_as_adopted', False)
            if new_status == 'Approved' and mark_as_adopted:
                cursor.execute("UPDATE pets SET status = 'adopted' WHERE id = (SELECT pet_id FROM applications WHERE id = %s)", (app_id,))

        conn.commit()
        return jsonify({"message": f"Application {new_status}"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
@applications_bp.route('/<int:app_id>', methods=['DELETE'])
def delete_application(app_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM applications WHERE id = %s", (app_id,))
        conn.commit()
        return jsonify({"message": "Application removed successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
