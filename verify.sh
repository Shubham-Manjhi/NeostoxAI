#!/bin/bash
# Quick verification script for NeostoxAI service

echo "=========================================="
echo "NeostoxAI Service Verification"
echo "=========================================="
echo ""

# Check Python version
echo "1. Checking Python version..."
python3 --version
echo ""

# Check if dependencies are installed
echo "2. Checking dependencies..."
python3 -c "import selenium; print('  ✓ selenium:', selenium.__version__)"
python3 -c "import dotenv; print('  ✓ python-dotenv: installed')"
python3 -c "import webdriver_manager; print('  ✓ webdriver-manager: installed')"
echo ""

# Check if files exist
echo "3. Checking files..."
for file in broker.py strategy.py test_broker.py demo.py .env requirements.txt; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file missing"
    fi
done
echo ""

# Syntax check
echo "4. Checking Python syntax..."
python3 -m py_compile broker.py && echo "  ✓ broker.py - OK"
python3 -m py_compile strategy.py && echo "  ✓ strategy.py - OK"
python3 -m py_compile test_broker.py && echo "  ✓ test_broker.py - OK"
python3 -m py_compile demo.py && echo "  ✓ demo.py - OK"
echo ""

echo "=========================================="
echo "Verification Complete!"
echo "=========================================="
echo ""
echo "To run the service:"
echo "  Demo mode:  python3 demo.py"
echo "  Test mode:  python3 test_broker.py"
echo "  Live mode:  python3 strategy.py"
echo ""

