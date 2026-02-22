import mysql.connector
import config

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            port=config.MYSQL_PORT,
            connect_timeout=5 # Fail fast if DB is down
        )
        return conn
    except Exception as e:
        print(f"❌ DATABASE CONNECTION ERROR: {e}")
        raise e