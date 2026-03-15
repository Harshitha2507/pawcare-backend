# migration_ensure_is_read_in_messages.py
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
        
        print("🛠️ Checking for 'is_read' in messages table...")
        cursor.execute("SHOW COLUMNS FROM messages LIKE 'is_read'")
        if not cursor.fetchone():
            print("➕ Adding 'is_read' column...")
            cursor.execute("ALTER TABLE messages ADD COLUMN is_read BOOLEAN DEFAULT FALSE AFTER message")
            print("✅ 'is_read' added.")
        else:
            print("ℹ️ 'is_read' already exists.")
            
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    migrate()
