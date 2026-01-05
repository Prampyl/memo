
import psycopg2
import os
import sys

def check_db():
    print("🔍 DIAGNOSTIC: Checking Database Status...")
    
    # 1. Config
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASS", "postgres")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    
    print(f"   Config: user={user}, host={host}:{port}, dbname=memo_db")
    print(f"   Password set? {'Yes' if password else 'No (Empty string)'}")

    # 2. Check Server Connection (connect to default 'postgres' db)
    print("\n1️⃣  Testing Connection to Server...")
    try:
        conn = psycopg2.connect(
            user=user, password=password, host=host, port=port, dbname="postgres"
        )
        conn.close()
        print("   ✅ Server is RUNNING and accepting connections.")
    except Exception as e:
        print(f"   ❌ Connection Failed: {e}")
        print("   -> Is PostgreSQL service running?")
        print("   -> Is the password correct?")
        return

    # 3. Check if 'memo_db' exists
    print("\n2️⃣  Checking for 'memo_db'...")
    try:
        conn = psycopg2.connect(
            user=user, password=password, host=host, port=port, dbname="postgres"
        )
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'memo_db'")
        exists = cur.fetchone()
        conn.close()
        
        if exists:
            print("   ✅ Database 'memo_db' EXISTS.")
        else:
            print("   ❌ Database 'memo_db' DOES NOT EXIST.")
            print("   -> Run 'python backend/init_db.py' to create it.")
            return
    except Exception as e:
        print(f"   ❌ Failed to check database existence: {e}")
        return

    # 4. Check Tables in 'memo_db'
    print("\n3️⃣  Checking Tables in 'memo_db'...")
    try:
        conn = psycopg2.connect(
            user=user, password=password, host=host, port=port, dbname="memo_db"
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT count(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        count = cur.fetchone()[0]
        conn.close()
        
        print(f"   ✅ Database contains {count} tables.")
        if count < 5:
            print("   ⚠️  Warning: Table count usually low (expected 10+). Did schema apply?")
    except Exception as e:
        print(f"   ❌ Failed to inspect 'memo_db': {e}")
        return

    print("\n✅ Verification COMPLETE. Database is ready.")

if __name__ == "__main__":
    check_db()
