# check_notifications_schema.py
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
        
        print("🔍 Checking 'notifications' table schema...")
        cursor.execute("DESCRIBE notifications")
        for col in cursor.fetchall():
            print(col)
            
        print("\n🔍 Checking 'applications' table schema...")
        cursor.execute("DESCRIBE applications")
        for col in cursor.fetchall():
            print(col)
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Check failed: {e}")

if __name__ == "__main__":
    check()
