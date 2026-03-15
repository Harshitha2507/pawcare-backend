import mysql.connector
import config
import os

def get_db_connection():
    try:
        # Determine the path to ca.pem
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ssl_ca_path = os.path.join(base_dir, config.MYSQL_SSL_CA) if hasattr(config, "MYSQL_SSL_CA") else None

        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            port=config.MYSQL_PORT,
            ssl_ca=ssl_ca_path,
            ssl_disabled=False,
            connect_timeout=5 # Fail fast if DB is down
        )
        return conn
    except Exception as e:
        print(f"❌ DATABASE CONNECTION ERROR: {e}")
        raise e