# fix_messages_table.py
import mysql.connector
import config

def fix():
    try:
        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            port=config.MYSQL_PORT
        )
        cursor = conn.cursor()
        
        print("🛠️ Fixing 'messages' table...")
        
        # 1. Check for receiver_id
        cursor.execute("SHOW COLUMNS FROM messages LIKE 'receiver_id'")
        if not cursor.fetchone():
            print("➕ Adding column 'receiver_id'...")
            cursor.execute("ALTER TABLE messages ADD COLUMN receiver_id INT AFTER sender_id")
            cursor.execute("ALTER TABLE messages ADD CONSTRAINT fk_msg_receiver FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE")
            print("✅ 'receiver_id' added.")
        else:
            print("ℹ️ 'receiver_id' already exists.")
            
        # 2. Check for created_at vs timestamp
        cursor.execute("SHOW COLUMNS FROM messages LIKE 'created_at'")
        if cursor.fetchone():
            print("ℹ️ Found 'created_at'. Keeping it as the primary time column for compatibility.")
        else:
            print("ℹ️ 'created_at' not found. Checking for 'timestamp'...")
            cursor.execute("SHOW COLUMNS FROM messages LIKE 'timestamp'")
            if cursor.fetchone():
                print("➕ Creating 'created_at' as an alias for 'timestamp'...")
                # Unfortunately MySQL doesn't have easy aliases, so we ensure the code uses the right name.
                # If 'timestamp' exists but code wants 'created_at', we rename it back.
                cursor.execute("ALTER TABLE messages CHANGE COLUMN timestamp created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                print("✅ Renamed 'timestamp' back to 'created_at' for universal compatibility.")

        conn.commit()
        
        # 3. Check chats table
        print("🛠️ Checking 'chats' table...")
        cursor.execute("SHOW COLUMNS FROM chats LIKE 'pet_id'")
        if not cursor.fetchone():
            print("➕ Adding 'pet_id' to chats...")
            cursor.execute("ALTER TABLE chats ADD COLUMN pet_id INT AFTER user2_id")
            print("✅ 'pet_id' added.")
            
        cursor.close()
        conn.close()
        print("✨ Database is now in sync with the code!")
    except Exception as e:
        print(f"❌ Fix failed: {e}")

if __name__ == "__main__":
    fix()
