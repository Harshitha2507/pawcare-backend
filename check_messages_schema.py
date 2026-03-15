# check_messages_schema.py
import mysql.connector
import config

def check():
    try:
        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            port=config.MYSQL_PORT
        )
        cursor = conn.cursor()
        
        print("🔍 Checking 'messages' table schema...")
        cursor.execute("DESCRIBE messages")
        for col in cursor.fetchall():
            print(col)
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Check failed: {e}")

if __name__ == "__main__":
    check()
