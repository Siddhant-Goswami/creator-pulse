#!/usr/bin/env python3
"""
Demo CLI interface for Twitter Competitor Analyzer (works without API keys)
"""

import asyncio
import json
import sys
from datetime import datetime
from twitter_analyzer import TwitterCompetitorAnalyzer

class DemoTwitterAnalyzer(TwitterCompetitorAnalyzer):
    """Demo version that doesn't require API keys"""
    
    def __init__(self):
        # Skip parent __init__ to avoid API key requirements
        pass
    
    async def generate_content_ideas(self, patterns_analysis, competitor_data):
        """Use fallback content generation (no API required)"""
        return self._generate_fallback_ideas(patterns_analysis)

def print_header():
    print("🐦 Twitter Competitor Analyzer - DEMO")
    print("=" * 50)
    print("📝 This demo works without API keys using sample data")
    print()

def get_demo_input():
    """Get simple input for demo"""
    print("📝 Demo Configuration:")
    print()
    
    # Show available demo profiles
    demo_profiles = {
        '1': {
            'name': '100x Engineer',
            'user_username': '100xengineers',
            'competitor_usernames': ['naval', 'sama', 'paulg', 'kentcdodds'],
            'description': 'Tech/Engineering focused analysis'
        },
        '2': {
            'name': 'Entrepreneur',
            'user_username': 'varunmayya',
            'competitor_usernames': ['elonmusk', 'naval', 'garyvee', 'dharmesh'],
            'description': 'Business/Startup focused analysis'
        },
        '3': {
            'name': 'Custom',
            'user_username': '',
            'competitor_usernames': [],
            'description': 'Enter your own usernames'
        }
    }
    
    print("Choose a demo profile:")
    for key, profile in demo_profiles.items():
        print(f"  {key}. {profile['name']} - {profile['description']}")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice in demo_profiles:
        profile = demo_profiles[choice]
        
        if choice == '3':
            # Custom input
            user_username = input("Enter your Twitter username: ").strip().replace('@', '')
            competitors_input = input("Enter competitor usernames (comma-separated): ").strip()
            competitor_usernames = [u.strip().replace('@', '') for u in competitors_input.split(',') if u.strip()]
            
            return {
                'user_username': user_username,
                'competitor_usernames': competitor_usernames,
                'tweets_per_competitor': 10,
                'auto_discover': True
            }
        else:
            return {
                'user_username': profile['user_username'],
                'competitor_usernames': profile['competitor_usernames'],
                'tweets_per_competitor': 10,
                'auto_discover': True
            }
    else:
        # Default to profile 1
        return {
            'user_username': '100xengineers',
            'competitor_usernames': ['naval', 'sama', 'paulg', 'kentcdodds'],
            'tweets_per_competitor': 10,
            'auto_discover': True
        }

async def run_demo_analysis(config):
    """Run demo analysis with sample data"""
    try:
        analyzer = DemoTwitterAnalyzer()
        
        print("\n🔍 Starting Demo Analysis...")
        print("=" * 30)
        
        # Use configured competitors
        final_competitors = config['competitor_usernames'][:5]  # Limit for demo
        
        # Auto-discover more if needed
        if config['auto_discover'] and config['user_username']:
            print(f"🔍 Auto-discovering competitors for @{config['user_username']}...")
            discovered = await analyzer.discover_competitors(config['user_username'], 3)
            final_competitors.extend(discovered)
            final_competitors = list(set(final_competitors))[:8]  # Limit for demo
            print(f"✅ Discovered additional competitors")
        
        print(f"\n📊 Analyzing {len(final_competitors)} competitors:")
        for i, competitor in enumerate(final_competitors, 1):
            print(f"  {i}. @{competitor}")
        print()
        
        # Analyze each competitor's tweets (using sample data)
        competitor_tweets_data = {}
        
        for i, username in enumerate(final_competitors):
            print(f"📱 [{i+1}/{len(final_competitors)}] Analyzing @{username}...")
            
            try:
                tweets = await analyzer.get_top_performing_tweets(username, config['tweets_per_competitor'])
                
                if tweets:
                    competitor_tweets_data[username] = tweets
                    avg_engagement = sum(t['engagement_score'] for t in tweets) / len(tweets)
                    print(f"  ✅ Found {len(tweets)} tweets (avg engagement: {avg_engagement:.1f})")
                    
                    # Show top tweet preview
                    top_tweet = tweets[0]
                    print(f"  🔥 Top tweet: \"{top_tweet.get('text', '')[:60]}...\"")
                else:
                    print(f"  ⚠️  No tweets found")
                    
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                continue
            
            # Small delay for demo effect
            await asyncio.sleep(0.5)
        
        if not competitor_tweets_data:
            print("❌ No competitor data available")
            return False
        
        print(f"\n📈 Successfully analyzed {len(competitor_tweets_data)} competitors")
        total_tweets = sum(len(tweets) for tweets in competitor_tweets_data.values())
        print(f"📊 Total tweets analyzed: {total_tweets}")
        
        # Analyze patterns
        print("\n🔍 Analyzing patterns...")
        patterns_analysis = await analyzer.analyze_tweet_patterns(competitor_tweets_data)
        
        # Display pattern insights
        print_pattern_insights(patterns_analysis)
        
        # Generate content ideas (using fallback method)
        print("\n💡 Generating content ideas...")
        content_ideas = await analyzer.generate_content_ideas(patterns_analysis, competitor_tweets_data)
        print_content_ideas(content_ideas)
        
        # Save results
        results = {
            "demo": True,
            "timestamp": datetime.now().isoformat(),
            "config": config,
            "analysis_summary": {
                "competitors_analyzed": len(competitor_tweets_data),
                "total_tweets_analyzed": total_tweets,
                "avg_engagement_score": patterns_analysis.get('avg_engagement_score', 0)
            },
            "patterns_analysis": patterns_analysis,
            "content_ideas": content_ideas
        }
        
        filename = f"demo_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Demo results saved to {filename}")
        print("✅ Demo analysis completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def print_pattern_insights(patterns_analysis):
    """Print pattern analysis insights"""
    print("\n📊 Pattern Analysis Results:")
    print("-" * 30)
    
    print(f"📈 Average engagement score: {patterns_analysis.get('avg_engagement_score', 0):.1f}")
    
    # Top hashtags
    top_hashtags = patterns_analysis.get('top_hashtags', [])[:5]
    if top_hashtags:
        print(f"\n🏷️  Top Hashtags:")
        for i, hashtag_data in enumerate(top_hashtags, 1):
            print(f"  {i}. #{hashtag_data['hashtag']} ({hashtag_data['frequency']} uses)")
    
    # Hook patterns
    hook_patterns = patterns_analysis.get('hook_patterns', {})
    top_hooks = hook_patterns.get('top_performing_hooks', [])[:3]
    if top_hooks:
        print(f"\n🎣 Top Performing Hooks:")
        for i, hook_data in enumerate(top_hooks, 1):
            print(f"  {i}. \"{hook_data['hook'][:50]}...\" ({hook_data['engagement_score']:.1f})")
    
    # Topic themes
    topics = patterns_analysis.get('topic_themes', [])[:5]
    if topics:
        print(f"\n📝 Top Topic Themes:")
        for i, topic in enumerate(topics, 1):
            print(f"  {i}. {topic}")
    
    # Length patterns
    length_patterns = patterns_analysis.get('optimal_length', {})
    if length_patterns:
        print(f"\n📏 Tweet Length Performance:")
        sorted_lengths = sorted(length_patterns.items(), key=lambda x: x[1].get('avg_engagement', 0), reverse=True)
        for length_range, data in sorted_lengths[:3]:
            avg_eng = data.get('avg_engagement', 0)
            count = data.get('count', 0)
            print(f"  • {length_range}: {avg_eng:.1f} avg engagement ({count} tweets)")

def print_content_ideas(content_ideas):
    """Print generated content ideas"""
    print("\n✨ Generated Content Ideas:")
    print("-" * 30)
    
    # Tweet ideas
    tweet_ideas = content_ideas.get('tweet_ideas', [])
    if tweet_ideas:
        print(f"\n🐦 Tweet Ideas ({len(tweet_ideas)}):")
        for i, tweet in enumerate(tweet_ideas[:7], 1):
            print(f"  {i}. {tweet}")
        if len(tweet_ideas) > 7:
            print(f"  ... and {len(tweet_ideas) - 7} more")
    
    # Hook ideas
    hook_ideas = content_ideas.get('hook_ideas', [])
    if hook_ideas:
        print(f"\n🎣 Hook Ideas ({len(hook_ideas)}):")
        for i, hook in enumerate(hook_ideas[:7], 1):
            print(f"  {i}. {hook}")
        if len(hook_ideas) > 7:
            print(f"  ... and {len(hook_ideas) - 7} more")
    
    # Strategy insights
    strategy_insights = content_ideas.get('strategy_insights', [])
    if strategy_insights:
        print(f"\n📈 Strategy Insights ({len(strategy_insights)}):")
        for i, insight in enumerate(strategy_insights, 1):
            print(f"  {i}. {insight}")

def main():
    """Main demo CLI function"""
    print_header()
    
    # Get demo configuration
    config = get_demo_input()
    
    # Confirm configuration
    print(f"\n📋 Demo Configuration:")
    print(f"  • User: @{config['user_username']}")
    print(f"  • Competitors: {', '.join('@' + c for c in config['competitor_usernames'])}")
    print(f"  • Auto-discover: {config['auto_discover']}")
    print(f"  • Tweets per competitor: {config['tweets_per_competitor']}")
    
    proceed = input("\nStart demo analysis? (y/n): ").strip().lower()
    if proceed != 'y':
        print("❌ Demo cancelled")
        sys.exit(0)
    
    # Run demo analysis
    success = asyncio.run(run_demo_analysis(config))
    
    if success:
        print("\n🎉 Demo completed successfully!")
        print("📊 Check the generated JSON file for detailed results.")
        print("\n💡 To run with real Twitter data, set up the API keys:")
        print("   export OPENROUTER_API_KEY='your_key'")
        print("   export APIFY_TOKEN='your_token'")
        print("   python cli_test.py")
    else:
        print("\n💥 Demo failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()