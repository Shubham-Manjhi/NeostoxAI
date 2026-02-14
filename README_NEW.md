# NeostoxAI - Automated Trading Service

## Overview
Neostox doesn't have API support, so this is a Selenium-based automation tool to implement trading strategies on the Neostox paper trading platform.

## ✨ Recent Updates (February 2026)
- ✅ Updated to Selenium 4.16.0 with modern syntax
- ✅ Replaced deprecated methods (find_element_by_* → find_element)
- ✅ Added webdriver-manager for automatic ChromeDriver management
- ✅ Fixed cross-platform compatibility (works on macOS, Windows, Linux)
- ✅ Added proper error handling and waits
- ✅ Created comprehensive test and demo scripts
- ✅ Updated strategy to dynamically select instruments

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone <repository-url>
cd NeostoxAI

# Install dependencies
pip3 install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the project root:
```env
email_id=your_email@example.com
password=your_password
```

### 3. Run Demo
```bash
python3 demo.py
```

### 4. Run Tests
```bash
python3 test_broker.py
```

### 5. Run Live Strategy
```bash
python3 strategy.py
```

## 📁 File Structure

### broker.py
Core module that handles:
- **Signing in** to Neostox
- **Fetching list of options** from sidebar
- **Fetching data every minute** for all instruments
- **Placing buy/sell orders**

Key methods:
- `make_connection()` - Handles login and reCaptcha
- `get_options_list()` - Loads available instruments
- `get_data()` - Fetches current prices
- `buy_order(instrument_name, qty)` - Places buy order
- `sell_order(instrument_name, qty)` - Places sell order
- `run()` - Main loop that runs every minute

### strategy.py
User-defined trading strategy. The `strategy()` function is called every minute and can:
1. Place a buy order
2. Place a sell order
3. Do nothing

### test_broker.py
Comprehensive test script that validates:
- Connection establishment
- Instrument loading
- Data fetching

### demo.py
Demonstration script that showcases all service capabilities without placing actual orders.

## 💡 How to Create Your Own Strategy

1. Edit the `Strategy` class in `strategy.py`
2. Specify instruments to trade
3. Define entry/exit conditions
4. Access latest price data: `self.data[instrument_name][-1]`

Example strategy:
```python
class Strategy(broker):
    def __init__(self):
        super().__init__()
        if self.instruments:
            self.instrument_name = list(self.instruments.keys())[0]
    
    def strategy(self):
        if self.instrument_name in self.data:
            latest_price = self.data[self.instrument_name][-1]
            
            # Your trading logic here
            if latest_price > some_threshold:
                self.buy_order(self.instrument_name, 1)
            elif latest_price < some_threshold:
                self.sell_order(self.instrument_name, 1)
```

## 🔧 Technical Details

### Dependencies
- **selenium 4.16.0** - Web automation
- **python-dotenv 1.0.0** - Environment variable management
- **webdriver-manager 4.0.1** - Automatic ChromeDriver management

### Data Structures
- `self.data` - Dictionary storing minute-by-minute price data for each instrument
- `self.instruments` - Dictionary mapping instrument names to [index, option_id]
- `self.index` - Counter that increments every minute for easy data access
- `self.list_options` - List of Selenium WebElements for all instruments

### Timing
- The service fetches data and executes strategy every minute
- Uses time synchronization to run at the end of each minute (58 seconds)

## 🔐 Security Notes
- Keep your `.env` file secure and never commit it to version control
- The `.gitignore` file is configured to exclude `.env`
- Use paper trading accounts for testing

## ⚠️ Important Notes

1. **Manual reCaptcha**: You must complete the reCaptcha manually when the browser opens
2. **Browser stays open**: Chrome browser will remain open during execution
3. **Sidebar requirements**: Make sure instruments are loaded in the Neostox sidebar
4. **Network stability**: Ensure stable internet connection for reliable operation
5. **Market hours**: Only works during market hours when instruments are active

## 🐛 Troubleshooting

### Chrome Driver Issues
If you encounter ChromeDriver issues, the webdriver-manager will automatically download the correct version. If problems persist:
```bash
pip3 install --upgrade webdriver-manager
```

### Element Not Found Errors
If elements are not found, the website structure may have changed. Check:
1. Element IDs and class names in browser DevTools
2. Update selectors in broker.py accordingly

### Login Issues
If login fails:
1. Verify credentials in `.env` file
2. Check if Neostox website is accessible
3. Ensure reCaptcha is completed properly

## 📊 Testing Results

All tests passed successfully:
- ✅ Connection establishment
- ✅ Instrument loading
- ✅ Data fetching
- ✅ Order placement (structure verified)

## 🤝 Contributing

Contributions are welcome! Please:
1. Create a new branch for your feature
2. Test thoroughly
3. Submit a pull request

## 📝 License

This is an educational project for learning automated trading concepts.

## 📧 Contact

For issues or questions, please open an issue on GitHub.

---

**Disclaimer**: This tool is for educational and paper trading purposes only. Always test thoroughly before using with real money. Trading involves risk.

