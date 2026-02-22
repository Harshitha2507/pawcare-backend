import mysql.connector
import config
from models import get_db_connection

def run_migration():
    print("Starting database migration for users table...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if lender_type exists
        cursor.execute("SHOW COLUMNS FROM users LIKE 'lender_type'")
        if not cursor.fetchone():
            print("Adding 'lender_type' column to 'users' table...")
            cursor.execute("ALTER TABLE users ADD COLUMN lender_type VARCHAR(50) AFTER role")
            conn.commit()
            print("OK 'lender_type' column added.")
        else:
            print("INFO 'lender_type' column already exists.")

        # Check if location exists
        cursor.execute("SHOW COLUMNS FROM users LIKE 'location'")
        if not cursor.fetchone():
            print("Adding 'location' column to 'users' table...")
            cursor.execute("ALTER TABLE users ADD COLUMN location VARCHAR(100) AFTER lender_type")
            conn.commit()
            print("OK 'location' column added.")
        else:
            print("INFO 'location' column already exists.")

        print("SUCCESS Migration completed successfully!")
    except Exception as e:
        print(f"ERROR Migration failed: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    run_migration()
