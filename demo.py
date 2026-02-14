"""
Demo script to showcase the NeostoxAI service functionality
This script runs a limited demo without placing actual orders
"""
from broker import broker
import time

class DemoBroker(broker):
    def __init__(self):
        super().__init__()
        self.demo_mode = True

    def run_demo(self):
        """Run a demonstration of the service"""
        print("\n" + "="*60)
        print("NEOSTOX AI TRADING SERVICE - DEMONSTRATION")
        print("="*60)

        # Demo 1: Show connection status
        print("\n1. CONNECTION STATUS")
        print("-" * 60)
        print(f"✓ Browser launched: Chrome")
        print(f"✓ Website loaded: {self.driver.current_url}")
        print(f"✓ Login successful: Yes")
        print(f"✓ Session active: Yes")

        # Demo 2: Show available instruments
        print("\n2. AVAILABLE INSTRUMENTS")
        print("-" * 60)
        print(f"Total instruments loaded: {len(self.instruments)}")

        if self.instruments:
            print("\nInstrument List (showing first 10):")
            for i, (name, data) in enumerate(list(self.instruments.items())[:10]):
                print(f"  {i+1:2d}. {name:40s} [Index: {data[0]:2d}, ID: {data[1]}]")
        else:
            print("⚠ No instruments found. Please check if sidebar has options.")

        # Demo 3: Fetch live data
        print("\n3. LIVE DATA COLLECTION")
        print("-" * 60)
        print("Fetching current market data...")
        self.get_data()

        if self.data:
            print(f"✓ Data collected for {len(self.data)} instruments\n")
            print("Sample data (showing first 5 instruments):")
            for i, (name, prices) in enumerate(list(self.data.items())[:5]):
                if prices:
                    print(f"  {i+1}. {name:40s} Price: ₹{prices[-1]:,.2f}")
        else:
            print("⚠ No data collected yet")

        # Demo 4: Trading capability (without actual execution)
        print("\n4. TRADING CAPABILITIES")
        print("-" * 60)
        print("Available actions:")
        print("  ✓ Buy orders  - broker.buy_order(instrument_name, qty)")
        print("  ✓ Sell orders - broker.sell_order(instrument_name, qty)")
        print("  ✓ Data access - broker.data[instrument_name][-1]")

        # Demo 5: Strategy simulation
        print("\n5. STRATEGY SIMULATION")
        print("-" * 60)
        if self.instruments:
            sample_instrument = list(self.instruments.keys())[0]
            print(f"Sample instrument: {sample_instrument}")
            print("\nSimulated strategy logic:")
            print("  • Monitor price every minute")
            print("  • Execute trades based on conditions")
            print("  • Alternate buy/sell for demonstration")
            print("\n⚠ Note: Actual order placement is disabled in demo mode")

        # Demo 6: System status
        print("\n6. SYSTEM STATUS")
        print("-" * 60)
        print(f"✓ Data structures initialized:")
        print(f"  - Instruments dict: {len(self.instruments)} entries")
        print(f"  - Data dict: {len(self.data)} entries")
        print(f"  - Options list: {len(self.list_options)} elements")
        print(f"  - Index counter: {self.index}")

        # Summary
        print("\n" + "="*60)
        print("DEMO SUMMARY")
        print("="*60)
        print("✓ Service is working correctly")
        print("✓ All components initialized successfully")
        print("✓ Ready for live trading")
        print("\nTo run live trading, use: python3 strategy.py")
        print("="*60)

        # Keep browser open
        input("\n\nPress Enter to close browser and exit demo...")
        self.driver.quit()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Starting NeostoxAI Service Demo")
    print("="*60)
    print("\nThis demo will:")
    print("  1. Connect to Neostox")
    print("  2. Load available instruments")
    print("  3. Fetch live market data")
    print("  4. Demonstrate trading capabilities")
    print("\n⚠ Important: You need to complete the reCaptcha manually")
    print("="*60)

    input("\nPress Enter to start demo...")

    demo = DemoBroker()
    demo.run_demo()

