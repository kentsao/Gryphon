from src.utils.db import get_supabase
import sys

def test_connection():
    print("Testing Supabase Connection...")
    try:
        sb = get_supabase()
        # Try a simple public table read (profiles is robust enough if policy allows, or just check auth)
        # We'll try to get the auth session, which should be None but not error out
        session = sb.auth.get_session()
        print("✅ Supabase Client Initialized Successfully!")
        print(f"Auth Session: {session}")
        
    except Exception as e:
        print(f"❌ Connection Failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_connection()
