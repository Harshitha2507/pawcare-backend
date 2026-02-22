import mysql.connector
import config
import json

def test_query():
    print("Connecting to DB...")
    try:
        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            port=config.MYSQL_PORT
        )
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT p.*, u.name as lender_name, u.lender_type 
            FROM pets p 
            LEFT JOIN users u ON p.lender_id = u.id
        """
        
        print("Executing query...")
        cursor.execute(query)
        pets = cursor.fetchall()
        
        print(f"Query successful. Found {len(pets)} pets.")
        if len(pets) > 0:
            print("First pet sample:")
            # Convert datetime etc to string for printing
            print(pets[0])
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error executing query: {e}")

if __name__ == "__main__":
    test_query()
