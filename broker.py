from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import datetime
import os
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains

# Try to import webdriver-manager, but don't require it
try:
    from webdriver_manager.chrome import ChromeDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False

load_dotenv()

email_id = os.getenv("email_id")
password = os.getenv("password")


class broker():
    def __init__(self):
        """
        Parameters :
        1. Data dictionary that stores minute data for each of the options, indexed by its name
        2. Instruments dictionary stores the position of the option ID and the position of the option in the list of options, indexed by option name
        3. index is a variable that starts from 0 and increments after every minute, allows easy access to data
        """
        import glob

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        print("Initializing ChromeDriver...")

        # Strategy 1: Try Selenium 4's built-in driver management (selenium-manager)
        try:
            print("Attempting to use Selenium's built-in driver manager...")
            self.driver = webdriver.Chrome(options=options)
            print("✓ ChromeDriver initialized successfully with selenium-manager")

        except Exception as e1:
            print(f"Selenium-manager failed: {e1}")

            # Strategy 2: Try webdriver-manager if available
            if WEBDRIVER_MANAGER_AVAILABLE:
                try:
                    print("Attempting to use webdriver-manager...")
                    driver_path = ChromeDriverManager().install()
                    print(f"ChromeDriver path: {driver_path}")

                    # Fix for macOS ARM64 - the path might point to wrong file
                    if 'THIRD_PARTY_NOTICES' in driver_path or not os.access(driver_path, os.X_OK):
                        print("Fixing ChromeDriver path...")
                        # Get the directory containing the chromedriver
                        driver_dir = os.path.dirname(driver_path)

                        # Look for the actual chromedriver executable
                        possible_paths = [
                            os.path.join(driver_dir, 'chromedriver'),
                            os.path.join(os.path.dirname(driver_dir), 'chromedriver'),
                        ]

                        # Also search in subdirectories
                        base_dir = os.path.dirname(os.path.dirname(driver_dir))
                        found = glob.glob(os.path.join(base_dir, '**/chromedriver'), recursive=True)
                        possible_paths.extend(found)

                        # Find the first executable chromedriver
                        for path in possible_paths:
                            if (os.path.exists(path) and os.access(path, os.X_OK) and
                                'THIRD_PARTY' not in path and 'LICENSE' not in path):
                                driver_path = path
                                print(f"Found chromedriver at: {driver_path}")
                                break

                    service = Service(driver_path)
                    self.driver = webdriver.Chrome(service=service, options=options)
                    print("✓ ChromeDriver initialized successfully with webdriver-manager")

                except Exception as e2:
                    print(f"webdriver-manager failed: {e2}")
                    raise Exception("Could not initialize ChromeDriver. Please install it manually: brew install chromedriver")
            else:
                raise Exception("Could not initialize ChromeDriver. Please install webdriver-manager: pip install webdriver-manager")

        self.driver.maximize_window()
        self.driver.get("https://neostox.com")
        self.data = {}
        self.instruments = {}
        self.index = 0
        self.make_connection()

    def make_connection(self):
        driver = self.driver
        wait = WebDriverWait(driver, 20)  # Increased timeout for page load

        print("\n" + "="*60)
        print("Waiting for Neostox page to load...")
        print("="*60)

        try:
            # Try multiple possible selectors for sign in button
            sign_in = None
            selectors = [
                (By.ID, "ctl00_li_signin"),
                (By.LINK_TEXT, "Sign In"),
                (By.LINK_TEXT, "Login"),
                (By.PARTIAL_LINK_TEXT, "Sign"),
                (By.PARTIAL_LINK_TEXT, "Login"),
                (By.CSS_SELECTOR, "a[href*='signin']"),
                (By.CSS_SELECTOR, "a[href*='login']"),
                (By.CSS_SELECTOR, "button[class*='signin']"),
                (By.CSS_SELECTOR, "button[class*='login']"),
            ]

            print("\nSearching for Sign In button...")
            for by_method, selector in selectors:
                try:
                    print(f"  Trying: {by_method} = '{selector}'")
                    element = wait.until(EC.element_to_be_clickable((by_method, selector)))
                    if element:
                        sign_in = element
                        print(f"  ✓ Found Sign In button using {by_method} = '{selector}'")
                        break
                except:
                    continue

            if not sign_in:
                print("\n" + "="*60)
                print("ERROR: Could not find Sign In button!")
                print("="*60)
                print("\nThe Neostox website structure has changed.")
                print("Please follow these steps:")
                print("\n1. Look at the Chrome browser window")
                print("2. Find and click the Sign In / Login button manually")
                print("3. Complete the login form:")
                print(f"   Email: {email_id}")
                print(f"   Password: (use the password from .env)")
                print("4. Complete the reCaptcha")
                print("5. Wait for dashboard to load")
                print("\nPress Enter here AFTER you've logged in manually...")
                input()
                print("\nProceeding with manual login...")
                self.get_options_list()
                return

            # Click sign in
            sign_in.click()
            print("✓ Clicked Sign In button")

            time.sleep(2)

            # Try to find email field
            print("\nSearching for email field...")
            email_selectors = [
                (By.ID, "txt_emailaddress"),
                (By.NAME, "email"),
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.CSS_SELECTOR, "input[placeholder*='email' i]"),
            ]

            email_element = None
            for by_method, selector in email_selectors:
                try:
                    print(f"  Trying: {by_method} = '{selector}'")
                    element = wait.until(EC.presence_of_element_located((by_method, selector)))
                    if element:
                        email_element = element
                        print(f"  ✓ Found email field using {by_method} = '{selector}'")
                        break
                except:
                    continue

            if email_element:
                email_element.send_keys(email_id)
                print(f"✓ Entered email: {email_id}")
            else:
                print("⚠ Could not find email field automatically")

            # Try to find password field
            print("\nSearching for password field...")
            password_selectors = [
                (By.ID, "txt_password"),
                (By.NAME, "password"),
                (By.CSS_SELECTOR, "input[type='password']"),
            ]

            passwd_element = None
            for by_method, selector in password_selectors:
                try:
                    print(f"  Trying: {by_method} = '{selector}'")
                    element = driver.find_element(by_method, selector)
                    if element:
                        passwd_element = element
                        print(f"  ✓ Found password field using {by_method} = '{selector}'")
                        break
                except:
                    continue

            if passwd_element:
                passwd_element.send_keys(password)
                print("✓ Entered password")
            else:
                print("⚠ Could not find password field automatically")

            print("\n" + "="*60)
            if not email_element or not passwd_element:
                print("MANUAL ACTION REQUIRED:")
                print("Some fields could not be filled automatically.")
                print("Please fill in the login form manually in the browser.")
            print("\nPlease complete the reCaptcha and submit the form.")
            print("="*60)
            input("\nPress Enter AFTER you have logged in and see the dashboard...")

            current_url = driver.current_url
            print(f"\n✓ Current URL: {current_url}")
            print("✓ Connection Established")

            self.get_options_list()

        except Exception as e:
            print(f"\n✗ Error during connection: {e}")
            print("\n" + "="*60)
            print("FALLBACK: Manual Login Required")
            print("="*60)
            print("\nPlease complete the following steps manually:")
            print("1. Click Sign In / Login in the browser")
            print("2. Enter your credentials:")
            print(f"   Email: {email_id}")
            print(f"   Password: (from .env file)")
            print("3. Complete reCaptcha")
            print("4. Wait for dashboard to load")
            print("\nPress Enter here AFTER you've logged in...")
            input()
            print("\n✓ Proceeding...")
            self.get_options_list()

    def get_options_list(self):
        driver = self.driver
        wait = WebDriverWait(driver, 15)

        print("\n" + "="*60)
        print("Loading instruments from sidebar...")
        print("="*60)

        try:
            # Try multiple selectors for the tab content
            print("\nSearching for instruments container...")
            tab_content = None
            container_selectors = [
                (By.CLASS_NAME, "tab-content"),
                (By.ID, "home"),
                (By.CSS_SELECTOR, ".tab-content"),
                (By.CSS_SELECTOR, "#home"),
                (By.CSS_SELECTOR, "div[role='tabpanel']"),
            ]

            for by_method, selector in container_selectors:
                try:
                    print(f"  Trying: {by_method} = '{selector}'")
                    element = wait.until(EC.presence_of_element_located((by_method, selector)))
                    if element:
                        tab_content = element
                        print(f"  ✓ Found container using {by_method} = '{selector}'")
                        break
                except:
                    continue

            if not tab_content:
                print("\n⚠ Could not find instruments container")
                print("\nThis might mean:")
                print("  1. The website structure has changed significantly")
                print("  2. You're not on the trading dashboard yet")
                print("  3. No instruments are loaded in the sidebar")
                print("\nPlease check the browser window.")
                print("You should see a list of options/instruments in the sidebar.")
                print("\nIf you see instruments, we'll need to inspect the page structure.")
                print("Run: python3 inspect_neostox.py")

                # Try to find any links that might be instruments
                print("\nAttempting alternative search...")
                all_links = driver.find_elements(By.TAG_NAME, "a")
                potential_instruments = []

                for link in all_links:
                    try:
                        text = link.text
                        if text and '\n' in text and any(keyword in text.upper() for keyword in ['NIFTY', 'BANK', 'CE', 'PE']):
                            potential_instruments.append(link)
                    except:
                        pass

                if potential_instruments:
                    print(f"\n✓ Found {len(potential_instruments)} potential instrument links")
                    self.list_options = potential_instruments
                else:
                    print("\n✗ Could not find any instrument links")
                    self.list_options = []
                    self.instruments = {}
                    return
            else:
                # Try to find the home tab within tab content
                try:
                    tab_home = tab_content.find_element(By.ID, "home")
                except:
                    tab_home = tab_content

                # Get all links from the container
                self.list_options = tab_home.find_elements(By.TAG_NAME, "a")
                print(f"✓ Found {len(self.list_options)} links in container")

            # Process the instruments
            print("\nProcessing instruments...")
            for index, element in enumerate(self.list_options):
                try:
                    text = element.text
                    if not text or '\n' not in text:
                        continue

                    parts = text.split("\n")
                    if len(parts) >= 2:
                        name = parts[0]
                        value = parts[1]
                        option_id = element.get_attribute('id')

                        if option_id:
                            # Extract numeric ID from element ID
                            id_parts = option_id.split("_")
                            if len(id_parts) > 1:
                                numeric_id = id_parts[-1]
                            else:
                                numeric_id = option_id
                        else:
                            numeric_id = str(index)

                        self.instruments[name] = [index, numeric_id]
                        print(f"  {index+1}. {name:40s} Value: {value:15s} ID: {numeric_id}")
                except Exception as e:
                    continue

            if not self.instruments:
                print("\n⚠ No instruments were processed successfully")
                print("\nPossible issues:")
                print("  - Website structure has changed")
                print("  - No instruments loaded in sidebar")
                print("  - Need to navigate to trading page")
                print("\nFor detailed inspection, run: python3 inspect_neostox.py")
            else:
                print(f"\n✓ Successfully loaded {len(self.instruments)} instruments")

        except Exception as e:
            print(f"\n✗ Error loading instruments: {e}")
            print("\nPlease check:")
            print("  1. You are logged in to Neostox")
            print("  2. You are on the trading dashboard")
            print("  3. Instruments are visible in the sidebar")
            print("\nFor detailed inspection, run: python3 inspect_neostox.py")
            self.list_options = []
            self.instruments = {}

    def get_data(self):
        for element in self.list_options:
            name, value = (element.text).split("\n")
            pct_change, price = value.split("%")
            price = float(price)
            option_id = ((element.get_attribute('id')).split("_"))[1]
            if name not in self.data.keys():
                self.data[name] = []
            self.data[name].append(price)

    def buy_order(self, instrument_name, qty):
        option_id = self.instruments[instrument_name][1]
        index = self.instruments[instrument_name][0]
        element = self.list_options[index]
        buy_button_id = f"sb_bbtn{option_id}"
        buy_button = element.find_element(By.ID, buy_button_id)
        ActionChains(self.driver).move_to_element(element).perform()
        buy_button.click()
        list_links = self.driver.find_elements(By.TAG_NAME, 'a')
        for link in list_links:
            if (link.get_attribute('class') == "placeorderbutton placeorderbutton_buy"):
                link.click()
                break

    def sell_order(self, instrument_name, qty):
        option_id = self.instruments[instrument_name][1]
        index = self.instruments[instrument_name][0]
        element = self.list_options[index]
        sell_button_id = f"sb_sbtn{option_id}"
        sell_button = element.find_element(By.ID, sell_button_id)
        ActionChains(self.driver).move_to_element(element).perform()
        sell_button.click()
        list_links = self.driver.find_elements(By.TAG_NAME, 'a')
        for link in list_links:
            if (link.get_attribute('class') == "placeorderbutton placeorderbutton_sell"):
                link.click()
                break

    def run(self):
        while True:
            print(f"Before data fetching : {datetime.datetime.now()}")
            self.get_data()
            self.strategy()
            print(f"After strategy calling : {datetime.datetime.now()}")
            print(self.data)
            current_time = datetime.datetime.now()
            while (current_time.second % 60 < 58):
                current_time = datetime.datetime.now()
                time.sleep(1)
            self.index += 1



