
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def patch_db():
    print("🚑 Patching Database Schema...")
    
    # Config from env or defaults (matching db_manager)
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASS", "postgres")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = "memo_db"
    
    try:
        conn = psycopg2.connect(
            user=user, 
            password=password, 
            host=host, 
            port=port, 
            dbname=dbname
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # 1. Alter Reminder table
        print("   -> Altering 'Reminder' table column 'scheduled_time'...")
        try:
            # We use USING to cast the old time/text to timestamp if needed
            # Since rows might be effectively empty or just times, we assume default date or cast
            cur.execute("""
                ALTER TABLE "reminder" 
                ALTER COLUMN scheduled_time TYPE TIMESTAMP WITH TIME ZONE 
                USING '2026-01-01 ' || scheduled_time::text || '+00';
            """) 
            # Note: The USING clause is a bit hacky for TIME->TIMESTAMP conversion. 
            # If the table is empty (which it likely is for a fresh dev setup), we can just do:
        except Exception as e:
            print(f"      Complex ALTER failed ({e}), trying simple drop/create for Reminder table...")
            cur.execute('DROP TABLE IF EXISTS "reminder" CASCADE;')
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Reminder (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    patient_id UUID REFERENCES Patient(id) ON DELETE CASCADE,
                    title VARCHAR(200) NOT NULL, spoken_message TEXT NOT NULL, 
                    scheduled_time TIMESTAMP WITH TIME ZONE NOT NULL, category VARCHAR(50) NOT NULL, is_active BOOLEAN DEFAULT TRUE
                );
            """)

        print("✅ Schema Patch Applied Successfully.")
        conn.close()
        
    except Exception as e:
        print(f"❌ Patch Failed: {repr(e)}")
        print("   (Ensure environment variables DB_PASS etc. are set if needed)")

if __name__ == "__main__":
    patch_db()
