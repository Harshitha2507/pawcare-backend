# test_notification_insert.py
import mysql.connector
import config

def test():
    try:
        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            port=config.MYSQL_PORT
        )
        cursor = conn.cursor()
        
        # 1. Check columns
        print("🔍 Checking 'notifications' table columns...")
        cursor.execute("DESCRIBE notifications")
        columns = [col[0] for col in cursor.fetchall()]
        print(f"✅ Found columns: {columns}")
        
        if 'application_id' not in columns:
            print("❌ ATENTION: 'application_id' is MISSING!")
        else:
            print("✅ 'application_id' is PRESENT.")
            
            # 2. Try a test insert
            print("🛠️ Trying a test INSERT with application_id=NULL...")
            cursor.execute(
                "INSERT INTO notifications (user_id, application_id, title, message) VALUES (%s, %s, %s, %s)",
                (1, None, "Test Notification", "This is a test")
            )
            print("✅ Test insert SUCCESSFUL (Rolling back now...)")
            conn.rollback()
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test()
