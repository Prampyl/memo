
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import sys

# Default config - User can override via env vars
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres") # Common default
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
TARGET_DB = "memo_db"

def init_db():
    print(f"🔌 Connecting to PostgreSQL at {DB_HOST}:{DB_PORT} as {DB_USER}...")
    
    # 1. Connect to default 'postgres' database to create new DB
    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            dbname="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if DB exists
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{TARGET_DB}'")
        exists = cur.fetchone()
        
        if not exists:
            print(f"✨ Creating database '{TARGET_DB}'...")
            cur.execute(f"CREATE DATABASE {TARGET_DB}")
        else:
            print(f"✅ Database '{TARGET_DB}' already exists.")
            
        cur.close()
        conn.close()
        
    except Exception as e:
        try:
            # Try to decode safely or just show repr
            print(f"❌ Failed to connect to Postgres: {repr(e)}")
        except:
            print("❌ Failed to connect to Postgres (and failed to print error details due to encoding)")
        
        print("💡 Hint: Make sure PostgreSQL is installed and running.")
        print("   If your user/pass differs, set DB_USER and DB_PASS environment variables.")
        return False

    # 2. Run Schema
    print("📜 Applying Schema...")
    try:
        # Re-connect to the specific DB
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            dbname=TARGET_DB
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Enable UUID extension specifically (though schema does it too)
        cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        
        schema_path = os.path.join(os.path.dirname(__file__), 'models/schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
            cur.execute(schema_sql)
            
        print("✅ Schema applied successfully.")
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to apply schema: {e}")
        return False

if __name__ == "__main__":
    success = init_db()
    if not success:
        sys.exit(1)
