#!/bin/bash

# Twitter Competitor Analyzer - Quick Start Script
# This script shows how to run the Twitter agent with proper setup

echo "🐦 Twitter Competitor Analyzer - Setup & Run"
echo "=============================================="
echo

# Check if API keys are set
if [[ -z "$OPENROUTER_API_KEY" ]]; then
    echo "❌ OPENROUTER_API_KEY not set"
    echo "   Get your key from: https://openrouter.ai/"
    echo "   Then run: export OPENROUTER_API_KEY='your_key_here'"
    echo
    MISSING_KEYS=true
fi

if [[ -z "$APIFY_TOKEN" ]]; then
    echo "❌ APIFY_TOKEN not set"
    echo "   Get your token from: https://apify.com/"
    echo "   Then run: export APIFY_TOKEN='your_token_here'"
    echo
    MISSING_KEYS=true
fi

if [[ "$MISSING_KEYS" == "true" ]]; then
    echo "🔧 To set up API keys:"
    echo "   1. Get OpenRouter API key: https://openrouter.ai/"
    echo "   2. Get Apify token: https://apify.com/"
    echo "   3. Export them as environment variables:"
    echo "      export OPENROUTER_API_KEY='your_openrouter_key'"
    echo "      export APIFY_TOKEN='your_apify_token'"
    echo
    echo "💡 Then run this script again or use:"
    echo "   python cli_test.py        # Interactive CLI"
    echo "   python test_twitter.py    # Automated test"
    echo
    echo "🎯 For demo without API keys:"
    echo "   python auto_demo.py       # Runs with sample data"
    echo
    exit 1
fi

echo "✅ API keys are set up"
echo

# Check if dependencies are installed
echo "📦 Checking dependencies..."
if ! python -c "import apify, aiohttp" 2>/dev/null; then
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies OK"
fi

echo
echo "🚀 Choose how to run the Twitter agent:"
echo "  1. Interactive CLI (recommended)"
echo "  2. Automated test with sample competitors"
echo "  3. Demo with sample data (no API calls)"
echo

read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "🔍 Starting interactive CLI..."
        python cli_test.py
        ;;
    2)
        echo "🧪 Running automated test..."
        python test_twitter.py
        ;;
    3)
        echo "🎮 Running demo with sample data..."
        python auto_demo.py
        ;;
    *)
        echo "❌ Invalid choice. Running demo..."
        python auto_demo.py
        ;;
esac

echo
echo "✅ Done! Check the generated JSON files for detailed results."