"""
Script to inspect Neostox website structure and find correct element IDs
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("="*60)
print("Neostox Website Inspector")
print("="*60)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

print("\n1. Launching Chrome browser...")
driver = webdriver.Chrome(options=options)
driver.maximize_window()

print("2. Loading Neostox website...")
driver.get("https://neostox.com")
time.sleep(3)

print("\n3. Page title:", driver.title)
print("4. Current URL:", driver.current_url)

print("\n5. Searching for login/signin elements...")

# Common login element patterns
search_patterns = [
    ("ID", "ctl00_li_signin"),
    ("ID", "signin"),
    ("ID", "login"),
    ("CLASS_NAME", "signin"),
    ("CLASS_NAME", "login"),
    ("LINK_TEXT", "Sign In"),
    ("LINK_TEXT", "Login"),
    ("LINK_TEXT", "Sign in"),
    ("PARTIAL_LINK_TEXT", "Sign"),
    ("PARTIAL_LINK_TEXT", "Login"),
]

found_elements = []

for method, value in search_patterns:
    try:
        if method == "ID":
            elements = driver.find_elements(By.ID, value)
        elif method == "CLASS_NAME":
            elements = driver.find_elements(By.CLASS_NAME, value)
        elif method == "LINK_TEXT":
            elements = driver.find_elements(By.LINK_TEXT, value)
        elif method == "PARTIAL_LINK_TEXT":
            elements = driver.find_elements(By.PARTIAL_LINK_TEXT, value)

        if elements:
            for elem in elements:
                try:
                    text = elem.text
                    tag = elem.tag_name
                    elem_id = elem.get_attribute('id')
                    elem_class = elem.get_attribute('class')
                    href = elem.get_attribute('href')
                    found_elements.append((method, value, tag, elem_id, elem_class, text, href))
                    print(f"   ✓ Found via {method}='{value}':")
                    print(f"     Tag: {tag}, ID: {elem_id}, Class: {elem_class}")
                    print(f"     Text: {text}, Href: {href}")
                except:
                    pass
    except Exception as e:
        pass

if not found_elements:
    print("   ✗ No elements found with common patterns")
    print("\n6. Let's check the page source for sign in related text...")

    page_source = driver.page_source.lower()
    if 'sign in' in page_source or 'signin' in page_source or 'login' in page_source:
        print("   ✓ Found 'sign in' or 'login' text in page source")
        print("   Let's get all clickable links...")

        all_links = driver.find_elements(By.TAG_NAME, 'a')
        print(f"\n7. Found {len(all_links)} links on the page")
        print("   Links containing 'sign', 'login', or 'account':")

        for link in all_links:
            try:
                text = link.text.lower()
                href = link.get_attribute('href') or ""
                elem_id = link.get_attribute('id') or ""
                elem_class = link.get_attribute('class') or ""

                if any(keyword in text or keyword in href.lower() or keyword in elem_id.lower()
                       for keyword in ['sign', 'login', 'account', 'auth']):
                    print(f"\n   Link text: '{link.text}'")
                    print(f"   ID: {elem_id}")
                    print(f"   Class: {elem_class}")
                    print(f"   Href: {href}")
            except:
                pass

        # Also check buttons
        all_buttons = driver.find_elements(By.TAG_NAME, 'button')
        print(f"\n8. Found {len(all_buttons)} buttons on the page")
        print("   Buttons containing 'sign', 'login', or 'account':")

        for button in all_buttons:
            try:
                text = button.text.lower()
                elem_id = button.get_attribute('id') or ""
                elem_class = button.get_attribute('class') or ""

                if any(keyword in text or keyword in elem_id.lower()
                       for keyword in ['sign', 'login', 'account', 'auth']):
                    print(f"\n   Button text: '{button.text}'")
                    print(f"   ID: {elem_id}")
                    print(f"   Class: {elem_class}")
            except:
                pass

print("\n" + "="*60)
print("INSTRUCTIONS:")
print("="*60)
print("1. Look at the Chrome browser window")
print("2. Manually inspect the Sign In / Login button")
print("3. Right-click -> Inspect Element")
print("4. Note the ID, class, or other attributes")
print("5. Come back here and press Enter to close")
print("="*60)

input("\nPress Enter to close browser...")
driver.quit()
print("\n✓ Browser closed")

