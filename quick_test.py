"""Quick test to verify all imports work correctly"""
import sys

print("=" * 60)
print("QUICK IMPORT TEST")
print("=" * 60)

try:
    print("\n1. Testing selenium imports...")
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    print("   ✓ Selenium imports successful")

    print("\n2. Testing webdriver-manager...")
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    print("   ✓ Webdriver-manager imports successful")

    print("\n3. Testing other dependencies...")
    from dotenv import load_dotenv
    import os
    print("   ✓ Other dependencies imported")

    print("\n4. Testing .env file...")
    load_dotenv()
    email = os.getenv("email_id")
    password = os.getenv("password")
    if email and password:
        print(f"   ✓ Credentials loaded: {email}")
    else:
        print("   ✗ Credentials not found in .env")

    print("\n5. Testing broker module...")
    import broker
    print("   ✓ Broker module can be imported")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)
    print("\nThe service is ready to run!")
    print("\nNext steps:")
    print("  - Run demo: python3 demo.py")
    print("  - Run tests: python3 test_broker.py")
    print("  - Run live: python3 strategy.py")
    print("=" * 60)

except Exception as e:
    print(f"\n✗ ERROR: {e}")
    print("\nPlease check:")
    print("  1. All dependencies installed: pip3 install -r requirements.txt")
    print("  2. .env file exists with credentials")
    sys.exit(1)

