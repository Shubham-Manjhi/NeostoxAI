"""Test ChromeDriver installation and find correct path"""
from webdriver_manager.chrome import ChromeDriverManager
import os
import glob

print("="*60)
print("ChromeDriver Path Finder")
print("="*60)

try:
    print("\n1. Downloading/locating ChromeDriver...")
    driver_path = ChromeDriverManager().install()
    print(f"   Path returned: {driver_path}")

    print("\n2. Checking if path is executable...")
    print(f"   Exists: {os.path.exists(driver_path)}")
    print(f"   Is executable: {os.access(driver_path, os.X_OK)}")
    print(f"   Is file: {os.path.isfile(driver_path)}")

    if not os.access(driver_path, os.X_OK) or 'THIRD_PARTY' in driver_path:
        print("\n3. Path issue detected! Searching for correct chromedriver...")

        # Get base directory
        driver_dir = os.path.dirname(driver_path)
        base_dir = os.path.dirname(os.path.dirname(driver_path))

        print(f"   Driver dir: {driver_dir}")
        print(f"   Base dir: {base_dir}")

        # List contents of driver directory
        print(f"\n4. Contents of {driver_dir}:")
        try:
            for item in os.listdir(driver_dir):
                item_path = os.path.join(driver_dir, item)
                is_exec = os.access(item_path, os.X_OK)
                print(f"   - {item} (executable: {is_exec})")
        except:
            pass

        # Search for chromedriver
        print("\n5. Searching for chromedriver files...")
        found = glob.glob(os.path.join(base_dir, '**/chromedriver'), recursive=True)

        for f in found:
            if 'THIRD_PARTY' not in f and 'LICENSE' not in f:
                is_exec = os.access(f, os.X_OK)
                print(f"   ✓ Found: {f}")
                print(f"     Executable: {is_exec}")
                if is_exec:
                    print(f"     *** USE THIS PATH ***")
                    correct_path = f
    else:
        print("\n✓ Path is good!")
        correct_path = driver_path

    print("\n" + "="*60)
    print("RESULT:")
    print("="*60)
    if 'correct_path' in locals():
        print(f"Correct ChromeDriver path: {correct_path}")
    else:
        print("Could not find executable chromedriver")

except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()

