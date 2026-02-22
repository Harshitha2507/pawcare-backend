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

        print("🔄 Updating messages table schema...")
        try:
            # 1. Add receiver_id if not exists
            cursor.execute("SHOW COLUMNS FROM messages LIKE 'receiver_id'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE messages ADD COLUMN receiver_id INT AFTER sender_id")
                cursor.execute("ALTER TABLE messages ADD CONSTRAINT fk_receiver FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE")
                print("✅ receiver_id added.")
            else:
                print("ℹ️ receiver_id already exists.")

            # 2. Rename created_at to timestamp if exists
            cursor.execute("SHOW COLUMNS FROM messages LIKE 'created_at'")
            if cursor.fetchone():
                cursor.execute("ALTER TABLE messages CHANGE COLUMN created_at timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                print("✅ Renamed created_at to timestamp.")
            else:
                print("ℹ️ created_at not found (possibly already renamed).")

        except mysql.connector.Error as err:
            print(f"❌ Migration Error: {err}")

        conn.commit()
        cursor.close()
        conn.close()
        print("✨ Migration complete.")

    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    migrate()
