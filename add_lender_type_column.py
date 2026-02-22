import mysql.connector
import config

def add_column():
    print("Connecting to database...")
    try:
        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            port=config.MYSQL_PORT
        )
        cursor = conn.cursor()
        
        print("Checking if 'lender_type' column exists...")
        cursor.execute("SHOW COLUMNS FROM users LIKE 'lender_type'")
        result = cursor.fetchone()
        
        if result:
            print("Column 'lender_type' already exists.")
        else:
            print("Column 'lender_type' missing. Adding it now...")
            cursor.execute("ALTER TABLE users ADD COLUMN lender_type VARCHAR(50) DEFAULT NULL")
            conn.commit()
            print("Column 'lender_type' added successfully!")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_column()
