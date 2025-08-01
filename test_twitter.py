#!/usr/bin/env python3

import asyncio
import json
import os
from datetime import datetime
from twitter_analyzer import TwitterCompetitorAnalyzer

async def test_twitter_analysis():
    """Test Twitter competitor analysis with sample data"""
    
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ OPENROUTER_API_KEY environment variable not set")
        return False
    
    print("🐦 Testing Twitter Competitor Analysis")
    print("=" * 50)
    print("📊 This test analyzes Twitter competitors and generates content ideas")
    print()
    
    # Test with popular tech Twitter accounts
    test_competitors = ["naval", "sama", "paulg"]
    
    try:
        analyzer = TwitterCompetitorAnalyzer()
        
        print(f"🔍 Analyzing {len(test_competitors)} Twitter competitors...")
        competitor_tweets_data = {}
        
        for i, username in enumerate(test_competitors, 1):
            print(f"  [{i}/{len(test_competitors)}] Analyzing @{username}...")
            
            try:
                tweets = await analyzer.get_top_performing_tweets(username, count=10)
                
                if tweets:
                    competitor_tweets_data[username] = tweets
                    avg_engagement = sum(t['engagement_score'] for t in tweets) / len(tweets)
                    print(f"    ✅ Success - {len(tweets)} tweets, avg engagement: {avg_engagement:.1f}")
                    
                    # Show top performing tweet
                    top_tweet = tweets[0]
                    print(f"    🔥 Top tweet: {top_tweet.get('engagement_score', 0):.1f} engagement")
                    print(f"    📝 Text preview: {top_tweet.get('text', '')[:80]}...")
                else:
                    print(f"    ⚠️  No tweets found for @{username}")
                    
            except Exception as e:
                print(f"    ❌ Error analyzing @{username}: {str(e)}")
                continue
        
        if not competitor_tweets_data:
            print("❌ No competitor data available")
            return False
        
        print(f"\n📊 Successfully analyzed {len(competitor_tweets_data)} competitors")
        total_tweets = sum(len(tweets) for tweets in competitor_tweets_data.values())
        print(f"📈 Total tweets analyzed: {total_tweets}")
        
        # Analyze patterns
        print("\n🔍 Analyzing patterns across competitor tweets...")
        patterns_analysis = await analyzer.analyze_tweet_patterns(competitor_tweets_data)
        
        print(f"📋 Pattern Analysis Results:")
        print(f"  • Average engagement score: {patterns_analysis.get('avg_engagement_score', 0):.1f}")
        print(f"  • Top hashtags found: {len(patterns_analysis.get('top_hashtags', []))}")
        print(f"  • Hook patterns analyzed: {patterns_analysis.get('hook_patterns', {}).get('total_hooks_analyzed', 0)}")
        print(f"  • Topic themes identified: {len(patterns_analysis.get('topic_themes', []))}")
        
        # Show some specific insights
        top_hashtags = patterns_analysis.get('top_hashtags', [])[:3]
        if top_hashtags:
            print(f"\n🏷️  Top Hashtags:")
            for i, hashtag_data in enumerate(top_hashtags, 1):
                print(f"   {i}. #{hashtag_data['hashtag']} (used {hashtag_data['frequency']} times)")
        
        hook_patterns = patterns_analysis.get('hook_patterns', {})
        top_hooks = hook_patterns.get('top_performing_hooks', [])[:3]
        if top_hooks:
            print(f"\n🎣 Top Performing Hooks:")
            for i, hook_data in enumerate(top_hooks, 1):
                print(f"   {i}. \"{hook_data['hook']}\" ({hook_data['engagement_score']:.1f} engagement)")
        
        # Generate content ideas
        print(f"\n💡 Generating AI-powered content ideas...")
        content_ideas = await analyzer.generate_content_ideas(patterns_analysis, competitor_tweets_data)
        
        print(f"\n✨ Generated Content Ideas:")
        
        # Show tweet ideas
        tweet_ideas = content_ideas.get('tweet_ideas', [])
        print(f"\n🐦 Tweet Ideas ({len(tweet_ideas)}):")
        for i, tweet in enumerate(tweet_ideas[:5], 1):
            print(f"  {i}. {tweet}")
        
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
        
        # Save test results
        test_results = {
            "test_metadata": {
                "timestamp": datetime.now().isoformat(),
                "test_type": "twitter_competitor_analysis",
                "competitors_tested": test_competitors,
                "successful_analyses": list(competitor_tweets_data.keys())
            },
            "analysis_summary": {
                "competitors_analyzed": len(competitor_tweets_data),
                "total_tweets_analyzed": total_tweets,
                "avg_engagement_score": patterns_analysis.get('avg_engagement_score', 0)
            },
            "patterns_analysis": patterns_analysis,
            "content_ideas": content_ideas
        }
        
        with open("twitter_test_results.json", "w") as f:
            json.dump(test_results, f, indent=2)
        
        print(f"\n💾 Test results saved to twitter_test_results.json")
        print("✅ Twitter analysis test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🐦 Twitter Competitor Analysis - Test")
    print("This test analyzes Twitter competitors using sample data")
    print()
    
    success = asyncio.run(test_twitter_analysis())
    
    if success:
        print("\n🎉 Twitter analysis is working correctly!")
        print("📋 Check twitter_test_results.json for detailed results.")
    else:
        print("\n💥 Test failed. Please check the errors above.")