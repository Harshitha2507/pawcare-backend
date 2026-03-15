"""
Migration: Add adoption_fee column to pets table.
Run this once to fix the 'add pet' functionality.
"""
import models
from models import get_db_connection

def run():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if column already exists
        cursor.execute("SHOW COLUMNS FROM pets LIKE 'adoption_fee'")
        exists = cursor.fetchone()
        if exists:
            print("✅ adoption_fee column already exists. Nothing to do.")
        else:
            cursor.execute("ALTER TABLE pets ADD COLUMN adoption_fee INT DEFAULT 0 AFTER status")
            conn.commit()
            print("✅ Successfully added adoption_fee column to pets table.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Migration failed: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    run()
