import mysql.connector
import config
from models import get_db_connection

def run_migration():
    print("Starting database migration for scheduled_at column...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("SHOW COLUMNS FROM notifications LIKE 'scheduled_at'")
        result = cursor.fetchone()
        
        if not result:
            print("Adding 'scheduled_at' column to 'notifications' table...")
            cursor.execute("ALTER TABLE notifications ADD COLUMN scheduled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("OK 'scheduled_at' column added.")
        else:
            print("INFO 'scheduled_at' column already exists.")
            
        conn.commit()
        print("SUCCESS Migration completed successfully!")
        
    except Exception as e:
        print(f"FAILED to migrate: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    run_migration()
