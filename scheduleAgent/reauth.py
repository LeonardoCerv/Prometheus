#!/usr/bin/env python3
"""
Re-authenticate with Google Calendar with the correct scopes.
This will delete the old token.json and create a new one with write permissions.
"""

import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def reauth():
    """Force re-authentication by deleting token.json"""
    token_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.json")
    
    if os.path.exists(token_file):
        print(f"🗑️  Deleting old token: {token_file}")
        os.remove(token_file)
        print("✅ Old token deleted")
    else:
        print("ℹ️  No existing token found")
    
    print("\n" + "=" * 50)
    print("Now running authentication...")
    print("=" * 50 + "\n")
    
    # Import and run the get_credentials function
    from my_agent.agent import get_credentials
    
    try:
        creds = get_credentials()
        print("\n" + "=" * 50)
        print("✅ Authentication successful!")
        print("=" * 50)
        print("\nYou can now run: adk run my_agent")
        return True
    except Exception as e:
        print("\n" + "=" * 50)
        print(f"❌ Authentication failed: {e}")
        print("=" * 50)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Google Calendar Re-Authentication")
    print("=" * 50)
    print("\nThis will:")
    print("1. Delete your existing token.json")
    print("2. Open a browser for you to authorize the app")
    print("3. Save a new token with calendar write permissions")
    print("\n" + "=" * 50)
    
    response = input("Continue? (y/n): ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        sys.exit(0)
    
    print()
    success = reauth()
    sys.exit(0 if success else 1)
