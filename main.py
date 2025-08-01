#!/usr/bin/env python3

# Import the Twitter analyzer
from twitter_analyzer import TwitterCompetitorAnalyzer, main

# This makes the main.py use Twitter analysis instead of Instagram
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())