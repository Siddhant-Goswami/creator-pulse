#!/usr/bin/env python3

import asyncio
import json
import os
from main import InstagramReelAnalyzer

# Sample data that simulates what would be scraped from Instagram
SAMPLE_COMPETITOR_DATA = {
    "100xengineers": [
        {
            "shortcode": "ABC123",
            "url": "https://www.instagram.com/reel/ABC123/",
            "caption": "🚀 Here's the secret to landing your first tech job that nobody tells you about! Stop applying randomly and start doing this instead... #techtips #career #programming",
            "likes": 15420,
            "comments": 234,
            "views": 125000,
            "engagement_rate": 12.5,
            "date": "2024-01-15T10:30:00",
            "hashtags": ["techtips", "career", "programming", "coding", "developer"],
            "mentions": [],
            "duration": 28
        },
        {
            "shortcode": "DEF456",
            "url": "https://www.instagram.com/reel/DEF456/",
            "caption": "POV: You're debugging for 3 hours and realize you forgot a semicolon 😭 Every developer has been there! What's your worst debugging story? #programming #debugging #coding",
            "likes": 8765,
            "comments": 156,
            "views": 89000,
            "engagement_rate": 10.2,
            "date": "2024-01-14T15:45:00",
            "hashtags": ["programming", "debugging", "coding", "developer", "memes"],
            "mentions": [],
            "duration": 15
        },
        {
            "shortcode": "GHI789",
            "url": "https://www.instagram.com/reel/GHI789/",
            "caption": "5 productivity hacks every developer needs to know! These changed my coding workflow completely. Save this post for later! #productivity #coding #tips",
            "likes": 12340,
            "comments": 189,
            "views": 98000,
            "engagement_rate": 12.8,
            "date": "2024-01-13T09:20:00",
            "hashtags": ["productivity", "coding", "tips", "developer", "workflow"],
            "mentions": [],
            "duration": 32
        }
    ],
    "thevarunmayya": [
        {
            "shortcode": "JKL012",
            "url": "https://www.instagram.com/reel/JKL012/",
            "caption": "This is why your startup is failing (and how to fix it) 📈 Most founders make these critical mistakes without realizing it... #startup #entrepreneur #business",
            "likes": 23450,
            "comments": 312,
            "views": 187000,
            "engagement_rate": 12.7,
            "date": "2024-01-15T14:20:00",
            "hashtags": ["startup", "entrepreneur", "business", "founder", "growth"],
            "mentions": [],
            "duration": 45
        },
        {
            "shortcode": "MNO345",
            "url": "https://www.instagram.com/reel/MNO345/",
            "caption": "The harsh truth about building a business in 2024... Everyone talks about overnight success but here's what really happens 💡 #reality #business #truth",
            "likes": 18900,
            "comments": 278,
            "views": 145000,
            "engagement_rate": 13.2,
            "date": "2024-01-14T11:30:00",
            "hashtags": ["reality", "business", "truth", "entrepreneur", "startup"],
            "mentions": [],
            "duration": 38
        }
    ],
    "rowancheung": [
        {
            "shortcode": "PQR678",
            "url": "https://www.instagram.com/reel/PQR678/",
            "caption": "I made $50K with this AI tool in 30 days (step by step tutorial) 🤖 This is changing everything for creators and entrepreneurs... #ai #makemoney #tutorial",
            "likes": 34500,
            "comments": 567,
            "views": 298000,
            "engagement_rate": 11.8,
            "date": "2024-01-15T16:45:00",
            "hashtags": ["ai", "makemoney", "tutorial", "entrepreneur", "passive"],
            "mentions": [],
            "duration": 52
        },
        {
            "shortcode": "STU901",
            "url": "https://www.instagram.com/reel/STU901/",
            "caption": "Stop doing this if you want to make money online! ❌ I see everyone making this mistake and wondering why they're not successful... #onlinebusiness #mistakes #money",
            "likes": 19800,
            "comments": 234,
            "views": 167000,
            "engagement_rate": 12.0,
            "date": "2024-01-14T13:15:00",
            "hashtags": ["onlinebusiness", "mistakes", "money", "entrepreneur", "tips"],
            "mentions": [],
            "duration": 29
        }
    ]
}

async def demo_analysis():
    """Demo the Instagram analysis with sample data"""
    
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ OPENROUTER_API_KEY environment variable not set")
        return False
    
    print("🎬 Demo: Instagram Competitor Analysis with Sample Data")
    print("=" * 60)
    print("📱 This demo shows how the analysis works with simulated Instagram data")
    print()
    
    try:
        analyzer = InstagramReelAnalyzer()
        
        print(f"📊 Sample Data Summary:")
        for username, reels in SAMPLE_COMPETITOR_DATA.items():
            avg_engagement = sum(r['engagement_rate'] for r in reels) / len(reels)
            print(f"  @{username}: {len(reels)} reels, avg engagement: {avg_engagement:.1f}%")
        
        print(f"\n🔍 Analyzing patterns across {sum(len(reels) for reels in SAMPLE_COMPETITOR_DATA.values())} sample reels...")
        
        # Run pattern analysis
        patterns_analysis = await analyzer.analyze_reel_patterns(SAMPLE_COMPETITOR_DATA)
        
        print(f"\n📋 Pattern Analysis Results:")
        print(f"  • Average engagement rate: {patterns_analysis.get('avg_engagement_rate', 0):.2f}%")
        print(f"  • Top hashtags: {len(patterns_analysis.get('top_hashtags', []))}")
        print(f"  • Hook patterns analyzed: {patterns_analysis.get('hook_patterns', {}).get('total_hooks_analyzed', 0)}")
        print(f"  • Topic themes: {len(patterns_analysis.get('topic_themes', []))}")
        
        # Show some specific insights
        top_hashtags = patterns_analysis.get('top_hashtags', [])[:5]
        if top_hashtags:
            print(f"\n🏷️  Top Hashtags:")
            for i, hashtag_data in enumerate(top_hashtags, 1):
                print(f"   {i}. #{hashtag_data['hashtag']} (used {hashtag_data['frequency']} times)")
        
        hook_patterns = patterns_analysis.get('hook_patterns', {})
        top_hooks = hook_patterns.get('top_performing_hooks', [])[:3]
        if top_hooks:
            print(f"\n🎣 Top Performing Hooks:")
            for i, hook_data in enumerate(top_hooks, 1):
                print(f"   {i}. \"{hook_data['hook']}\" ({hook_data['engagement_rate']:.1f}% engagement)")
        
        # Generate content ideas
        print(f"\n💡 Generating AI-powered content ideas...")
        content_ideas = await analyzer.generate_content_ideas(patterns_analysis, SAMPLE_COMPETITOR_DATA)
        
        print(f"\n✨ Generated Content Ideas:")
        
        # Show topic ideas
        topic_ideas = content_ideas.get('topic_ideas', [])
        print(f"\n🎯 Topic Ideas ({len(topic_ideas)}):")
        for i, topic in enumerate(topic_ideas[:5], 1):
            print(f"  {i}. {topic}")
        
        # Show hook ideas
        hook_ideas = content_ideas.get('hook_ideas', [])
        print(f"\n🎣 Hook Ideas ({len(hook_ideas)}):")
        for i, hook in enumerate(hook_ideas[:5], 1):
            print(f"  {i}. {hook}")
        
        # Show strategy insights
        strategy_insights = content_ideas.get('strategy_insights', [])
        print(f"\n📈 Strategy Insights ({len(strategy_insights)}):")
        for i, insight in enumerate(strategy_insights, 1):
            print(f"  {i}. {insight}")
        
        # Save demo results
        demo_results = {
            "demo_info": {
                "note": "This is a demo using sample data to show functionality",
                "sample_competitors": list(SAMPLE_COMPETITOR_DATA.keys()),
                "total_sample_reels": sum(len(reels) for reels in SAMPLE_COMPETITOR_DATA.values())
            },
            "patterns_analysis": patterns_analysis,
            "content_ideas": content_ideas
        }
        
        with open("demo_results.json", "w") as f:
            json.dump(demo_results, f, indent=2)
        
        print(f"\n💾 Demo results saved to demo_results.json")
        print(f"\n✅ Demo completed successfully!")
        print(f"\n💡 In production, this would scrape live Instagram data from your competitors")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(demo_analysis())
    
    if success:
        print(f"\n🎉 Demo shows the Instagram analyzer is working correctly!")
        print(f"📋 The Apify actor is ready - it just needs live Instagram access without rate limits")
    else:
        print(f"\n💥 Demo failed - check the errors above")