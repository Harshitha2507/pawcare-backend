import mysql.connector
import config

def check_data():
    try:
        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB
        )
        cursor = conn.cursor(dictionary=True)

        print("--- USERS ---")
        cursor.execute("SELECT id, name, email, role FROM users")
        for row in cursor.fetchall():
            print(row)

        print("\n--- PETS ---")
        cursor.execute("SELECT id, name, lender_id FROM pets")
        for row in cursor.fetchall():
            print(row)

        print("\n--- CHATS ---")
        cursor.execute("SELECT * FROM chats")
        for row in cursor.fetchall():
            print(row)

        print("\n--- MESSAGES ---")
        cursor.execute("SELECT * FROM messages")
        for row in cursor.fetchall():
            print(row)

        print("\n--- APPLICATIONS ---")
        cursor.execute("SELECT * FROM applications")
        for row in cursor.fetchall():
            print(row)

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    check_data()
