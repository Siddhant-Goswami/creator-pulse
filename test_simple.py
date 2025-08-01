#!/usr/bin/env python3

import asyncio
import json
import os
from main import InstagramReelAnalyzer

async def test_simple():
    """Simple test with direct input - bypasses Apify Actor input system"""
    
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ OPENROUTER_API_KEY environment variable not set")
        return False
    
    print("🧪 Testing Instagram analyzer directly...")
    
    # Test data (smaller accounts that might be less rate-limited)
    test_competitors = ["100xengineers", "thevarunmayya", "rowancheung"]
    
    try:
        analyzer = InstagramReelAnalyzer()
        
        print(f"🔍 Analyzing {len(test_competitors)} competitors...")
        competitor_reels_data = {}
        
        for username in test_competitors:
            print(f"  📱 Analyzing @{username}...")
            
            try:
                reels = await analyzer.get_top_performing_reels(username, count=5)  # Small count to avoid rate limits
                
                if reels:
                    competitor_reels_data[username] = reels
                    avg_engagement = sum(r['engagement_rate'] for r in reels) / len(reels)
                    print(f"    ✅ Success - {len(reels)} reels, avg engagement: {avg_engagement:.2f}%")
                else:
                    print(f"    ⚠️  No reels found for @{username}")
                    
            except Exception as e:
                print(f"    ❌ Error analyzing @{username}: {str(e)}")
                continue
        
        if not competitor_reels_data:
            print("❌ No competitor data available")
            return False
        
        print(f"\n📊 Successfully analyzed {len(competitor_reels_data)} competitors")
        
        # Generate some basic analysis
        patterns_analysis = await analyzer.analyze_reel_patterns(competitor_reels_data)
        content_ideas = await analyzer.generate_content_ideas(patterns_analysis, competitor_reels_data)
        
        print(f"\n✨ Sample Generated Ideas:")
        
        topic_ideas = content_ideas.get('topic_ideas', [])[:3]
        hook_ideas = content_ideas.get('hook_ideas', [])[:3]
        
        print(f"\n🎯 Topic Ideas:")
        for i, topic in enumerate(topic_ideas, 1):
            print(f"  {i}. {topic}")
        
        print(f"\n🎣 Hook Ideas:")
        for i, hook in enumerate(hook_ideas, 1):
            print(f"  {i}. {hook}")
        
        # Save simplified results
        results = {
            "competitors_analyzed": list(competitor_reels_data.keys()),
            "total_reels": sum(len(reels) for reels in competitor_reels_data.values()),
            "patterns_analysis": patterns_analysis,
            "content_ideas": content_ideas
        }
        
        with open("simple_test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to simple_test_results.json")
        print("✅ Test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_simple())
    if not success:
        print("\n💡 Instagram scraping can be rate-limited. Try again in a few minutes or use different accounts.")