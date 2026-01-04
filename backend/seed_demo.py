from models.db_manager import MemoDB

def reset():
    """Wipes the database and recreates the schema."""
    db = MemoDB()
    db.reset_database()
    print("🧹 Database cleared and schema recreated.")

def seed():
    """Fills the database with demo data and verifies it using specific retrieval functions."""
    db = MemoDB()
    
    # --- 1. INSERTIONS ---
    addr_id = db.add_address("123 Memory Lane", "Paris", "75001")
    
    doc_id = db.add_doctor(
        full_name="Dr. Gregory House",
        specialty="Diagnostic Medicine",
        phone_number="+33123456789",
        email="house@princeton-plainsboro.com"
    )

    p_id = db.add_patient(
        "Alice", "Smith", "1945-03-12", "Moderate", 
        preferred_name="Grandma Alice", address_id=addr_id
    )
    
    c_id = db.add_caregiver(
        email="caregiver.john@example.com",
        password_hash="hashed_password_example_123",
        first_name="John",
        last_name="Doe",
        relationship="Son",
        phone_number="+33612345678",
        address_id=addr_id,
        patient_id=p_id
    )

    db.link_doctor_to_patient(p_id, doc_id)
    
    db.add_reminder(p_id, "Tea Time", "Time for your tea, Alice.", "16:00:00", "Hydration")
    db.add_media(p_id, "https://storage.memo.ai/wedding_1965.jpg", "Image", "Wedding day.")

    # --- 2. RETREIVAL ---

    patient = db.get_patient(p_id)
    caregiver = db.get_caregiver(c_id)
    doctor = db.get_doctor(doc_id)
    address = db.get_address(patient['address_id'])

    docs_linked = db.get_doctors_from_patient(p_id)
    reminders = db.get_patient_reminders(p_id)
    media = db.get_patient_media(p_id)

    print(f"\n🚀 DATABASE SEED SUCCESSFUL")
    print(f"--------------------------------------------------")
    print(f"🏠 LOCATION: {address['street_line_1']}, {address['city']}")
    
    print(f"👤 PATIENT: {patient['first_name']} {patient['last_name']}")
    print(f"   └─ Diagnosis: {patient['diagnosis_stage']}")
    
    print(f"👥 CAREGIVER: {caregiver['first_name']} {caregiver['last_name']}")
    print(f"   └─ Relationship: {caregiver['relationship']} of {patient['first_name']}")
    
    print(f"👨‍⚕️ MEDICAL: {len(docs_linked)} doctor(s) linked")
    for d in docs_linked:
        print(f"   └─ {d['full_name']} ({d['specialty']})")
    
    print(f"📅 CONTENT: {len(reminders)} reminder(s) and {len(media)} media item(s) created")
    print(f"--------------------------------------------------\n")

if __name__ == "__main__":
    reset()
    seed()