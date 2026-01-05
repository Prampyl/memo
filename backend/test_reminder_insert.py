
import sys
import os
sys.path.append(os.getcwd())
from backend.models.db_manager import MemoDB
import datetime

def test_insert():
    print("Testing Reminder Insertion found in E2E failure...")
    try:
        db = MemoDB()
        
        # 1. Get a patient
        patients = db.get_all_patients()
        if not patients:
            print("No patients found. Run E2E seed first.")
            return
            
        pid = patients[0]['id']
        print(f"   Using Patient ID: {pid}")
        
        # 2. Try Insertion (replicating what the API does)
        # Note: API passes "2026-01-05T16:00:00" as string. Postgres 'TIME' column might want just time.
        try:
            db.add_reminder(pid, "Reminder", "Call doctor", "2026-01-05T16:00:00", "General")
            print("Insertion SUCCESS! (It implies the server loop was just stale)")
        except Exception as e:
            print(f"Insertion FAILED: {e}")
            print("   -> Attempting with Time-only format...")
            try:
                # Try just time
                db.add_reminder(pid, "Reminder", "Call doctor (Time only)", "16:00:00", "General")
                print("   Time-only Insertion SUCCESS. The issue is Schema expects TIME but we send DATETIME.")
            except Exception as e2:
                print(f"   Time-only Insertion Also FAILED: {e2}")

    except Exception as e:
        print(f"DB Connection Failed: {repr(e)}")

if __name__ == "__main__":
    test_insert()
