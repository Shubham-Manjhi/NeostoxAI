"""
Test script to validate broker functionality without running the full strategy
"""
from broker import broker
import time

class TestBroker(broker):
    def __init__(self):
        super().__init__()

    def test_connection(self):
        """Test if connection was successful"""
        print("\n=== CONNECTION TEST ===")
        print(f"Driver status: {'Active' if self.driver else 'Inactive'}")
        print(f"Current URL: {self.driver.current_url}")
        return True

    def test_instruments(self):
        """Test if instruments were loaded"""
        print("\n=== INSTRUMENTS TEST ===")
        print(f"Number of instruments loaded: {len(self.instruments)}")
        if self.instruments:
            print("\nFirst 5 instruments:")
            for i, (name, data) in enumerate(list(self.instruments.items())[:5]):
                print(f"  {i+1}. {name} - Index: {data[0]}, ID: {data[1]}")
            return True
        else:
            print("ERROR: No instruments loaded!")
            return False

    def test_data_fetch(self):
        """Test data fetching"""
        print("\n=== DATA FETCH TEST ===")
        print("Fetching data...")
        self.get_data()

        if self.data:
            print(f"Data fetched for {len(self.data)} instruments")
            # Show first 3 instruments' data
            for i, (name, prices) in enumerate(list(self.data.items())[:3]):
                print(f"  {name}: {prices}")
            return True
        else:
            print("ERROR: No data fetched!")
            return False

    def run_tests(self):
        """Run all tests"""
        print("\n" + "="*50)
        print("STARTING BROKER TESTS")
        print("="*50)

        tests_passed = 0
        tests_total = 3

        # Test 1: Connection
        if self.test_connection():
            tests_passed += 1

        # Test 2: Instruments
        if self.test_instruments():
            tests_passed += 1

        # Test 3: Data fetch
        if self.test_data_fetch():
            tests_passed += 1

        # Summary
        print("\n" + "="*50)
        print(f"TEST SUMMARY: {tests_passed}/{tests_total} tests passed")
        print("="*50)

        # Keep browser open for inspection
        input("\nPress Enter to close browser and exit...")
        self.driver.quit()


if __name__ == "__main__":
    print("Starting broker tests...")
    print("Note: You will need to complete the reCaptcha manually")
    test = TestBroker()
    test.run_tests()

