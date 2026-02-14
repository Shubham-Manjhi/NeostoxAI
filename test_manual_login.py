"""
Simple script to quickly test if demo can proceed with manual login
"""
from selenium import webdriver
import time

print("="*60)
print("Quick Manual Login Test")
print("="*60)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

print("\n1. Launching Chrome...")
driver = webdriver.Chrome(options=options)
driver.maximize_window()

print("2. Loading Neostox.com...")
driver.get("https://neostox.com")
time.sleep(3)

print(f"\n3. Current URL: {driver.current_url}")
print(f"4. Page title: {driver.title}")

print("\n" + "="*60)
print("MANUAL STEPS:")
print("="*60)
print("Please complete these steps in the browser:")
print("\n1. Click 'Sign In' or 'Login' button")
print("2. Enter credentials:")
print("   Email: quantflash.papertrading@gmail.com")
print("   Password: MANman#@2026")
print("3. Complete reCaptcha")
print("4. Wait for dashboard to load")
print("5. Look for instruments/options in sidebar")
print("\n" + "="*60)

input("\nPress Enter AFTER you've completed login and see the dashboard...")

print("\n6. After login:")
print(f"   Current URL: {driver.current_url}")
print(f"   Page title: {driver.title}")

# Try to find instruments
print("\n7. Searching for instruments/options...")
from selenium.webdriver.common.by import By

# Look for common patterns
all_links = driver.find_elements(By.TAG_NAME, 'a')
instrument_keywords = ['NIFTY', 'BANKNIFTY', 'SENSEX', 'CE', 'PE', 'CALL', 'PUT']

potential_instruments = []
for link in all_links:
    try:
        text = link.text
        if text and any(keyword in text.upper() for keyword in instrument_keywords):
            potential_instruments.append(text)
    except:
        pass

if potential_instruments:
    print(f"\n✓ Found {len(potential_instruments)} potential instruments:")
    for i, inst in enumerate(potential_instruments[:10], 1):
        print(f"   {i}. {inst[:60]}")

    if len(potential_instruments) > 10:
        print(f"   ... and {len(potential_instruments) - 10} more")

    print("\n✓ Great! Instruments are loading.")
    print("✓ The demo should work with manual login.")
else:
    print("\n⚠ No instruments found yet.")
    print("   Make sure you're on the trading dashboard.")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
print("\nConclusion:")
if potential_instruments:
    print("✓ Manual login works!")
    print("✓ Instruments can be accessed")
    print("\nYou can now run: python3 demo.py")
    print("Just complete login manually when prompted.")
else:
    print("⚠ Need to navigate to trading dashboard")
    print("  Make sure instruments are visible in sidebar")

input("\nPress Enter to close browser...")
driver.quit()
print("\n✓ Browser closed")

