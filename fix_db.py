import mysql.connector
import config

def fix_database():
    try:
        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB
        )
        cursor = conn.cursor()

        print("Checking database structure...")

        # 0. Ensure tables exist (Basic Schema)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20),
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'adopter'
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(50),
                breed VARCHAR(100),
                image VARCHAR(500),
                location VARCHAR(100),
                age VARCHAR(50),
                sex VARCHAR(20),
                color VARCHAR(50),
                description TEXT,
                is_favorited BOOLEAN DEFAULT FALSE,
                status VARCHAR(20) DEFAULT 'available',
                lender_id INT,
                FOREIGN KEY (lender_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)

        # 1. Add missing columns to pets
        try:
            cursor.execute("SHOW COLUMNS FROM pets LIKE 'lender_id'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE pets ADD COLUMN lender_id INT")
                cursor.execute("ALTER TABLE pets ADD CONSTRAINT fk_lender FOREIGN KEY (lender_id) REFERENCES users(id) ON DELETE SET NULL")
                print("Added 'lender_id' to pets.")
            
            cursor.execute("SHOW COLUMNS FROM pets LIKE 'album'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE pets ADD COLUMN album TEXT")
                print("Added 'album' to pets.")
        except Exception as e:
            print(f"Warning updating pets columns: {e}")

        # 2. Add lender_type to users if missing
        try:
            cursor.execute("SHOW COLUMNS FROM users LIKE 'lender_type'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE users ADD COLUMN lender_type VARCHAR(50) DEFAULT 'Pet Owner'")
                print("Added 'lender_type' to users.")
        except Exception as e:
            print(f"Warning adding lender_type: {e}")

        # 3. Handle applications table
        try:
            cursor.execute("SHOW TABLES LIKE 'applications'")
            exists = cursor.fetchone()
            if not exists:
                print("Creating applications table...")
                cursor.execute("""
                    CREATE TABLE applications (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        pet_id INT,
                        adopter_id INT,
                        applicant_name VARCHAR(100),
                        applicant_email VARCHAR(100),
                        phone VARCHAR(20),
                        address TEXT,
                        message TEXT,
                        status VARCHAR(20) DEFAULT 'Pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE,
                        FOREIGN KEY (adopter_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """)
                print("Created applications table.")
            else:
                cursor.execute("SHOW COLUMNS FROM applications LIKE 'adopter_id'")
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE applications ADD COLUMN adopter_id INT")
                    cursor.execute("ALTER TABLE applications ADD CONSTRAINT fk_adopter FOREIGN KEY (adopter_id) REFERENCES users(id) ON DELETE CASCADE")
                    print("Added 'adopter_id' to applications.")
        except Exception as e:
            print(f"❌ Error updating applications: {e}")

        # 4. Handle notifications table
        try:
            cursor.execute("SHOW TABLES LIKE 'notifications'")
            if not cursor.fetchone():
                print("Creating notifications table...")
                cursor.execute("""
                    CREATE TABLE notifications (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NULL,
                        application_id INT NULL,
                        title VARCHAR(255),
                        message TEXT,
                        type VARCHAR(50) DEFAULT 'general',
                        is_read BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE
                    )
                """)
                print("Created notifications table (user_id is nullable for global alerts).")
            else:
                cursor.execute("SHOW COLUMNS FROM notifications LIKE 'application_id'")
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE notifications ADD COLUMN application_id INT NULL")
                    cursor.execute("ALTER TABLE notifications ADD CONSTRAINT fk_notif_app FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE")
                    print("Added 'application_id' to notifications.")
                
                cursor.execute("SHOW COLUMNS FROM notifications LIKE 'type'")
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE notifications ADD COLUMN type VARCHAR(50) DEFAULT 'general'")
                    print("Added 'type' to notifications.")
        except Exception as e:
            print(f"❌ Error updating notifications: {e}")
            
        # 5. Handle chat tables
        try:
            cursor.execute("SHOW TABLES LIKE 'chats'")
            if not cursor.fetchone():
                print("Creating chats table...")
                cursor.execute("""
                    CREATE TABLE chats (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user1_id INT,
                        user2_id INT,
                        pet_id INT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user1_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (user2_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE SET NULL
                    )
                """)
                print("Created chats table.")

            cursor.execute("SHOW TABLES LIKE 'messages'")
            if not cursor.fetchone():
                print("Creating messages table...")
                cursor.execute("""
                    CREATE TABLE messages (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        chat_id INT,
                        sender_id INT,
                        message TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_read BOOLEAN DEFAULT FALSE,
                        FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE,
                        FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """)
                print("Created messages table.")
        except Exception as e:
            print(f"❌ Error updating chat tables: {e}")

        conn.commit()
        print("\nDatabase fix complete! You can now run the app.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    fix_database()
