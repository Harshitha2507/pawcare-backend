import mysql.connector
import config
from models import get_db_connection

def run_migration():
    print("Starting database migration for notifications table...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("SHOW COLUMNS FROM notifications LIKE 'type'")
        result = cursor.fetchone()
        
        if not result:
            print("Adding 'type' column to 'notifications' table...")
            cursor.execute("ALTER TABLE notifications ADD COLUMN type VARCHAR(50) DEFAULT 'general'")
            print("OK 'type' column added.")
        else:
            print("INFO 'type' column already exists.")
            
        conn.commit()
        print("SUCCESS Migration completed successfully!")
        
    except Exception as e:
        print(f"FAILED to migrate: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    run_migration()
