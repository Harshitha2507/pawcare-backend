import mysql.connector
import config
from models import get_db_connection

def run_migration():
    print("Starting database migration...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if health_status exists
        cursor.execute("SHOW COLUMNS FROM pets LIKE 'health_status'")
        if not cursor.fetchone():
            print("Adding 'health_status' column to 'pets' table...")
            cursor.execute("ALTER TABLE pets ADD COLUMN health_status VARCHAR(100) AFTER description")
            conn.commit()
            print("OK 'health_status' column added.")
        else:
            print("INFO 'health_status' column already exists.")

        # Check if album exists (consistency check based on pets.py usage)
        cursor.execute("SHOW COLUMNS FROM pets LIKE 'album'")
        if not cursor.fetchone():
            print("Adding 'album' column to 'pets' table...")
            cursor.execute("ALTER TABLE pets ADD COLUMN album TEXT AFTER health_status")
            conn.commit()
            print("OK 'album' column added.")
        else:
            print("INFO 'album' column already exists.")

        print("SUCCESS Migration completed successfully!")
    except Exception as e:
        print(f"ERROR Migration failed: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    run_migration()
