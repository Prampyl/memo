import psycopg2
from psycopg2.extras import RealDictCursor
import os

class MemoDB:
    def __init__(self):
        self.conn_params = {
            "dbname": "memo_db",
            "user": os.getlogin(),
            "password": "",
            "host": "localhost",
            "port": "5432"
        }

    def _execute_query(self, query, params=None, fetch=False):
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                if fetch: return cur.fetchall()
                conn.commit()

    def reset_database(self):
        """Drops all tables and recreates them from the updated schema.sql"""
        tables = [
            "ExerciseLog", "CognitiveExercise", "MediaItem", 
            "VoiceProfile", "Device", "Reminder", 
            "Address", "Doctor", "Caregiver", "Patient"
        ]
        
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                for table in tables:
                    cur.execute(f'DROP TABLE IF EXISTS {table} CASCADE;')
                with open(schema_path, 'r') as f:
                    cur.execute(f.read())

            conn.commit()

        print("✅ Database Reset: All tables (Patient, Caregiver, etc.) recreated.")


    # --- RETRIEVE FUNCTIONS ---

    def get_all_patients(self):
        """
        Returns a list of dictionaries. 
        Each dictionary represents one row from the Patient table.
        """
        query = 'SELECT * FROM Patient ORDER BY created_at DESC;'
        return self._execute_query(query, fetch=True)

    def get_all_caregivers(self):
        """
        Returns a list of dictionaries. 
        Each dictionary represents one row from the Caregiver table.
        """
        query = 'SELECT * FROM Caregiver ORDER BY last_name, first_name;'
        return self._execute_query(query, fetch=True)

    def get_all_addresses(self):
        """
        Returns a list of dictionaries. 
        Each dictionary represents one row from the Address table.
        """
        query = 'SELECT * FROM Address;'
        return self._execute_query(query, fetch=True)

    def get_all_doctors(self):
        """
        Returns a list of all doctors.
        """
        query = 'SELECT * FROM Doctor;'
        return self._execute_query(query, fetch=True)

    def get_doctors_from_patient(self, patient_id):
        """
        Returns a list of dictionaries,
        Which is a list of all doctors associated with a specific patient
        """
        query = """
            SELECT d.* FROM Doctor d
            JOIN PatientDoctor pd ON d.id = pd.doctor_id
            WHERE pd.patient_id = %s;
        """
        return self._execute_query(query, (patient_id,), fetch=True)

    def get_patients_from_doctor(self, doctor_id):
        """
        Returns a list of dictionaries,
        Which is a list of all patients associated with a specific doctor.
        """
        query = """
            SELECT p.* FROM Patient p
            JOIN PatientDoctor pd ON p.id = pd.patient_id
            WHERE pd.doctor_id = %s;
        """
        return self._execute_query(query, (doctor_id,), fetch=True)

    def get_patient_reminders(self, patient_id):
        """
        Returns a list of dictionaries. 
        Each dictionary represents one row from the Reminder table that matches the given patient_id.
        """
        query = 'SELECT * FROM Reminder WHERE patient_id = %s ORDER BY scheduled_time;'
        return self._execute_query(query, (patient_id,), fetch=True)

    def get_patient_media(self, patient_id):
        """
        Returns a list of dictionaries, 
        where each dictionary represents one row (one photo, video, or audio file) associated with that specific patient.
        """
        query = 'SELECT * FROM MediaItems WHERE patient_id = %s;'
        return self._execute_query(query, (patient_id,), fetch=True)

    # GET SINGLE ITEM FUNCTIONS 

    def get_patient(self, patient_id):
        """Returns a single patient dictionary by ID."""
        query = 'SELECT * FROM Patient WHERE id = %s;'
        result = self._execute_query(query, (patient_id,), fetch=True)
        return result[0] if result else None

    def get_caregiver(self, caregiver_id):
        """Returns a single caregiver dictionary by ID."""
        query = 'SELECT * FROM Caregiver WHERE id = %s;'
        result = self._execute_query(query, (caregiver_id,), fetch=True)
        return result[0] if result else None

    def get_doctor(self, doctor_id):
        """Returns a single doctor dictionary by ID."""
        query = 'SELECT * FROM Doctor WHERE id = %s;'
        result = self._execute_query(query, (doctor_id,), fetch=True)
        return result[0] if result else None

    def get_address(self, address_id):
        """Returns a single address dictionary by ID."""
        query = 'SELECT * FROM Address WHERE id = %s;'
        result = self._execute_query(query, (address_id,), fetch=True)
        return result[0] if result else None

    def get_address_id(self, street, city, zip_code):
        """
        Returns the UUID of an address if it exists in the database, 
        otherwise returns None.
        """
        query = """
            SELECT id FROM Address 
            WHERE street_line_1 = %s AND city = %s AND zip_code = %s;
        """
        result = self._execute_query(query, (street, city, zip_code), fetch=True)
        return result[0]['id'] if result else None

    # --- ADD FUNCTIONS ---

    def add_address(self, street, city, zip_code):
        """
        Ensures the address exists in the DB and returns its ID.
        Prevents duplicate rows for the same physical location.
        """
        # 1. Try to find it first
        existing_id = self.get_address_id(street, city, zip_code)
        
        if existing_id:
            return existing_id

        # 2. If not found, create it
        query = """
            INSERT INTO Address (street_line_1, city, zip_code) 
            VALUES (%s, %s, %s) 
            RETURNING id;
        """
        return self._execute_query(query, (street, city, zip_code), fetch=True)[0]['id']

    def add_patient(self, first_name, last_name, date_of_birth, diagnosis_stage, preferred_name=None, address_id=None):
        """Inserts a patient, optionally linked to an address."""
        query = """
            INSERT INTO Patient (first_name, last_name, date_of_birth, diagnosis_stage, preferred_name, address_id) 
            VALUES (%s, %s, %s, %s, %s, %s) 
            RETURNING id;
        """
        return self._execute_query(query, (first_name, last_name, date_of_birth, diagnosis_stage, preferred_name, address_id), fetch=True)[0]['id']
    
    def add_caregiver(self, email, password_hash, first_name, last_name, patient_id, relationship=None, address_id=None, phone_number=None):
        query = """
            INSERT INTO Caregiver (email, password_hash, first_name, last_name, patient_id, relationship, address_id, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """
        params = (email, password_hash, first_name, last_name, patient_id, relationship, address_id, phone_number)
        return self._execute_query(query, params, fetch=True)[0]['id']

    def add_doctor(self, full_name, specialty, phone_number, email):
        query = """
            INSERT INTO Doctor (full_name, specialty, phone_number, email)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """
        return self._execute_query(query, (full_name, specialty, phone_number, email), fetch=True)[0]['id']

    def link_doctor_to_patient(self, patient_id, doctor_id):
        """Links a doctor to a patient in the junction table."""
        query = """
            INSERT INTO PatientDoctor (patient_id, doctor_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING; 
        """
        self._execute_query(query, (patient_id, doctor_id))
        print(f"🔗 Doctor {doctor_id} linked to Patient {patient_id}")

    def add_media(self, patient_id, file_path, media_type, description):
        query = "INSERT INTO MediaItems (patient_id, file_path, media_type, description) VALUES (%s, %s, %s, %s);"
        self._execute_query(query, (patient_id, file_path, media_type, description))

    def add_reminder(self, patient_id, title, message, time, category):
        query = "INSERT INTO Reminder (patient_id, title, spoken_message, scheduled_time, category) VALUES (%s, %s, %s, %s, %s);"
        self._execute_query(query, (patient_id, title, message, time, category))


    # --- EDIT FUNCTIONS ---

    def link_address(self, entity_type, entity_id, street, city, zip_code):
        """Links an address to a person. If address doesn't exist, it creates it."""
        # This will either find the old ID or create a new one
        address_id = self.add_address(street, city, zip_code)
        
        query = f'UPDATE "{entity_type}" SET address_id = %s WHERE id = %s;'
        self._execute_query(query, (address_id, entity_id))
        
        return address_id

    # --- REMOVE FUNCTIONS ---

    def unlink_doctor_from_patient(self, patient_id, doctor_id):
        """
        Removes the connection between a doctor and a patient.
        Neither the patient nor the doctor record is deleted.
        """
        query = """
            DELETE FROM PatientDoctor 
            WHERE patient_id = %s AND doctor_id = %s;
        """
        self._execute_query(query, (patient_id, doctor_id))
        print(f"✂️ Link removed between Doctor {doctor_id} and Patient {patient_id}")