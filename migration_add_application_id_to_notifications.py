# migration_add_application_id_to_notifications.py
import mysql.connector
import config

def migrate():
    try:
        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            port=config.MYSQL_PORT
        )
        cursor = conn.cursor()
        
        print("🛠️ Adding application_id column to notifications table...")
        # Check if column exists first to avoid error
        cursor.execute("SHOW COLUMNS FROM notifications LIKE 'application_id'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE notifications ADD COLUMN application_id INT AFTER user_id")
            cursor.execute("ALTER TABLE notifications ADD CONSTRAINT fk_notif_app FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE")
            print("✅ Column 'application_id' added successfully!")
        else:
            print("ℹ️ Column 'application_id' already exists.")
            
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    migrate()
