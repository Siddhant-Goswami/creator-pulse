#!/usr/bin/env python3

import asyncio
import json
import os
import sys
from datetime import datetime
from main import InstagramReelAnalyzer

async def test_integration():
    """Integration test: analyze Instagram competitors and generate content ideas"""
    
    # Check environment variables
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ OPENROUTER_API_KEY environment variable not set")
        print("Please set your OpenRouter API key:")
        print("export OPENROUTER_API_KEY=your_key_here")
        return False
    
    print("🧪 Starting Instagram integration test...")
    print("📱 Testing Instagram reel analysis and content idea generation")
    
    # Test with popular Instagram accounts (public, business accounts)
    test_competitors = [
        "garyvee",  # Gary Vaynerchuk - Business/Marketing
        "mrbeast",  # MrBeast - Entertainment/Content
        "hubspot"   # HubSpot - Business/Marketing
    ]
    
    try:
        analyzer = InstagramReelAnalyzer()
        
        print(f"\n🔍 Analyzing {len(test_competitors)} test competitors...")
        competitor_reels_data = {}
        
        for i, username in enumerate(test_competitors, 1):
            print(f"  [{i}/{len(test_competitors)}] Analyzing @{username}...")
            
            try:
                reels = await analyzer.get_top_performing_reels(username, count=10)  # Smaller count for testing
                
                if reels:
                    competitor_reels_data[username] = reels
                    avg_engagement = sum(r['engagement_rate'] for r in reels) / len(reels)
                    print(f"    ✅ Success - {len(reels)} reels, avg engagement: {avg_engagement:.2f}%")
                    
                    # Show top performing reel
                    top_reel = reels[0]
                    print(f"    📈 Top reel: {top_reel.get('engagement_rate', 0):.2f}% engagement")
                    print(f"    📝 Caption preview: {top_reel.get('caption', '')[:100]}...")
                else:
                    print(f"    ⚠️  No reels found for @{username}")
                    
            except Exception as e:
                print(f"    ❌ Failed to analyze @{username}: {str(e)}")
                continue
        
        if not competitor_reels_data:
            print("❌ No competitor data available - cannot proceed with analysis")
            return False
        
        print(f"\n📊 Successfully analyzed {len(competitor_reels_data)} competitors")
        total_reels = sum(len(reels) for reels in competitor_reels_data.values())
        print(f"📈 Total reels analyzed: {total_reels}")
        
        # Analyze patterns
        print("\n🔍 Analyzing patterns across competitor reels...")
        patterns_analysis = await analyzer.analyze_reel_patterns(competitor_reels_data)
        
        print(f"📋 Pattern Analysis Results:")
        print(f"  • Average engagement rate: {patterns_analysis.get('avg_engagement_rate', 0):.2f}%")
        print(f"  • Top hashtags found: {len(patterns_analysis.get('top_hashtags', []))}")
        print(f"  • Hook patterns analyzed: {patterns_analysis.get('hook_patterns', {}).get('total_hooks_analyzed', 0)}")
        print(f"  • Topic themes identified: {len(patterns_analysis.get('topic_themes', []))}")
        
        # Generate content ideas
        print("\n💡 Generating content ideas based on analysis...")
        content_ideas = await analyzer.generate_content_ideas(patterns_analysis, competitor_reels_data)
        
        print(f"\n✨ Generated Content Ideas:")
        
        # Display topic ideas
        topic_ideas = content_ideas.get('topic_ideas', [])
        print(f"\n🎯 Topic Ideas ({len(topic_ideas)}):")
        for i, topic in enumerate(topic_ideas[:5], 1):  # Show first 5
            print(f"  {i}. {topic}")
        
        # Display hook ideas  
        hook_ideas = content_ideas.get('hook_ideas', [])
        print(f"\n🎣 Hook Ideas ({len(hook_ideas)}):")
        for i, hook in enumerate(hook_ideas[:5], 1):  # Show first 5
            print(f"  {i}. {hook}")
        
        # Display strategy insights
        strategy_insights = content_ideas.get('strategy_insights', [])
        print(f"\n📈 Strategy Insights ({len(strategy_insights)}):")
        for i, insight in enumerate(strategy_insights, 1):
            print(f"  {i}. {insight}")
        
        # Save comprehensive test results
        test_results = {
            "test_metadata": {
                "timestamp": datetime.now().isoformat(),
                "test_type": "instagram_integration_test",
                "competitors_tested": test_competitors,
                "successful_analyses": list(competitor_reels_data.keys())
            },
            "analysis_summary": {
                "competitors_analyzed": len(competitor_reels_data),
                "total_reels_analyzed": total_reels,
                "avg_engagement_rate": patterns_analysis.get('avg_engagement_rate', 0)
            },
            "patterns_analysis": patterns_analysis,
            "content_ideas": content_ideas,
            "sample_competitor_data": {
                username: {
                    "reels_count": len(reels),
                    "avg_engagement": sum(r['engagement_rate'] for r in reels) / len(reels) if reels else 0,
                    "top_reel_sample": reels[0] if reels else None
                }
                for username, reels in competitor_reels_data.items()
            }
        }
        
        with open("instagram_test_results.json", "w") as f:
            json.dump(test_results, f, indent=2)
        
        print(f"\n💾 Comprehensive test results saved to instagram_test_results.json")
        print("✅ Instagram integration test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the Instagram integration test"""
    print("🚀 Instagram Competitor Analysis & Content Ideas - Integration Test")
    print("=" * 70)
    print("📱 This test will analyze public Instagram accounts and generate content ideas")
    print("⏱️  Note: This may take a few minutes as we analyze Instagram data...")
    print()
    
    success = asyncio.run(test_integration())
    
    if success:
        print("\n🎉 All tests passed! The Instagram Apify actor is ready to use.")
        print("📋 Check instagram_test_results.json for detailed analysis results.")
        sys.exit(0)
    else:
        print("\n💥 Tests failed. Please check the errors above.")
        print("💡 Common issues:")
        print("   • Missing OPENROUTER_API_KEY environment variable")
        print("   • Instagram rate limiting (try again in a few minutes)")
        print("   • Network connectivity issues")
        sys.exit(1)

if __name__ == "__main__":
    main()