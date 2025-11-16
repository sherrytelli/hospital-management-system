import psycopg2
import logging
import hashlib
from config import DATABASE_CONFIG

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, provided_password):
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

def get_db_conn():
    "returns a connection to the database"
    
    try:
        conn = psycopg2.connect(
            host=DATABASE_CONFIG["db_host"],
            database=DATABASE_CONFIG["db_name"],
            user=DATABASE_CONFIG["db_user"],
            password=DATABASE_CONFIG["db_pass"],
            port=DATABASE_CONFIG["db_port"]
            )
        return conn
    
    except Exception as e:
        logging.error(f"database connection error: {e}")
        return None
    
def add_patient(name, contact, diagnosis):
    """adds new patient in the database"""
    
    conn = get_db_conn()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT INTO patients (name, contact, diagnosis) VALUES (%s, %s, %s, ''. '') RETURNING patient_id;
                        """, (name, contact, diagnosis))
            patient_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return patient_id
        
        except Exception as e:
            logging.error(f"Error adding patient: {e}")
            return None
        
        finally:
            conn.close()
    else:
        print("Failed to connect to the database to add patient.")
        return None

def annonymize_patient_data(patient_id):
    """applies masking logic to patient data and inserts into database"""
    
    conn = get_db_conn()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                    SELECT contact FROM patients WHERE patient_id = %s
                        """, (patient_id,))
            result = cursor.fetchone()
            
            if result:
                original_contact = result
                
                anon_name = f"ANNON_{patient_id}"
                anon_contact = "XXX-XXX-XXXX" if original_contact else ''
                
                cursor.execute("""
                        UPDATE patients SET anonymized_name = %s, anonymized_contact = %s WHERE patient_id = %s;
                            """, (anon_name, anon_contact, patient_id))
                
                conn.commit()
                cursor.close()
                return True
            
            else:
                cursor.close()
                return False
        
        except Exception as e:
            logging.error(f"Error anonymizing patient data: {e}")
            cursor.close()
            return False
        
        finally:
            cursor.close()
            conn.cursor()
    
    else:
        logging.error("Failed to connect to the database to anonymize patient data.")
        return False
    
def log_action(user_id, roll, action, details):
    """logs the actions of all the employees in the logs table"""
    
    conn = get_db_conn()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT INTO logs(user_id, role, action, details) VALUES (%s, %s, %s, %s);
                        """, (user_id, roll, action, details))
            conn.commit()
            cursor.close()
        
        except Exception as e:
            logging.error(f"Error logging action: {e}")
            
        finally:
            cursor.close()
            conn.close()
    
    else:
        logging.error("Failed to connect to the database to log action.")

def init_db():
    conn = get_db_conn()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(64) NOT NULL, -- SHA-256 produces 64 hex characters
                    role VARCHAR(20) NOT NULL
                );
            """)
            
            # Create patients table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    contact VARCHAR(100),
                    diagnosis TEXT,
                    anonymized_name VARCHAR(100),
                    anonymized_contact VARCHAR(100),
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    log_id SERIAL PRIMARY KEY,
                    user_id INTEGER,
                    role VARCHAR(20) NOT NULL,
                    action TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    details TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );
            """)
            
            # Check if users already exist before inserting
            cursor.execute("SELECT COUNT(*) FROM users;")
            user_count = cursor.fetchone()[0]
            
            if user_count == 0:
                # Insert sample users with hashed passwords using hashlib
                sample_users = [
                    ('admin', hash_password('admin123'), 'admin'),
                    ('Dr. Bob', hash_password('doc123'), 'doctor'),
                    ('Alice_recep', hash_password('rec123'), 'receptionist')
                ]
                
                for username, hashed_password, role in sample_users:
                    cursor.execute(
                        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                        (username, hashed_password, role)
                    )
                
                print("Sample users with hashed passwords inserted successfully.")
            else:
                print("Sample users already exist in the database.")
            
            conn.commit()
            cursor.close()
            print("Database initialized successfully!")
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    init_db()