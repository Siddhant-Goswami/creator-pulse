#!/usr/bin/env python3
"""
CLI interface to test the Twitter Competitor Analyzer
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from twitter_analyzer import TwitterCompetitorAnalyzer

def print_header():
    print("🐦 Twitter Competitor Analyzer - CLI Test")
    print("=" * 50)
    print()

def check_environment():
    """Check if required environment variables are set"""
    required_vars = {
        'OPENROUTER_API_KEY': 'OpenRouter API key for AI content generation',
        'APIFY_TOKEN': 'Apify token for Twitter scraping (optional for demo)'
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"  ❌ {var}: {description}")
        else:
            print(f"  ✅ {var}: Set")
    
    if missing_vars:
        print("⚠️  Missing environment variables:")
        for var in missing_vars:
            print(var)
        print("\nTo set these variables:")
        print("export OPENROUTER_API_KEY='your_key_here'")
        print("export APIFY_TOKEN='your_token_here'")
        print()
        return False
    
    return True

def get_user_input():
    """Get user input for analysis parameters"""
    print("📝 Analysis Configuration:")
    print()
    
    # Get username for competitor discovery
    user_username = input("Enter your Twitter username (for competitor discovery): ").strip().replace('@', '')
    
    # Get manual competitor list
    print("\nEnter competitor usernames (comma-separated, optional):")
    competitors_input = input("Competitors: ").strip()
    
    competitor_usernames = []
    if competitors_input:
        competitor_usernames = [u.strip().replace('@', '') for u in competitors_input.split(',') if u.strip()]
    
    # Get number of tweets per competitor
    tweets_per_competitor = input("\nTweets per competitor (default: 10): ").strip()
    tweets_per_competitor = int(tweets_per_competitor) if tweets_per_competitor.isdigit() else 10
    
    # Auto-discover competitors
    auto_discover = True
    if competitor_usernames:
        auto_discover_input = input("\nAuto-discover additional competitors? (y/n, default: y): ").strip().lower()
        auto_discover = auto_discover_input != 'n'
    
    return {
        'user_username': user_username,
        'competitor_usernames': competitor_usernames,
        'tweets_per_competitor': tweets_per_competitor,
        'auto_discover': auto_discover,
        'min_competitors': 5
    }

async def run_analysis(config):
    """Run the Twitter competitor analysis"""
    try:
        analyzer = TwitterCompetitorAnalyzer()
        
        print("\n🔍 Starting Analysis...")
        print("=" * 30)
        
        # Build final competitor list
        final_competitors = list(config['competitor_usernames'])
        
        # Auto-discover competitors if needed
        if config['auto_discover'] and config['user_username'] and len(final_competitors) < config['min_competitors']:
            print(f"🔍 Auto-discovering competitors for @{config['user_username']}...")
            discovered = await analyzer.discover_competitors(
                config['user_username'], 
                config['min_competitors'] - len(final_competitors)
            )
            final_competitors.extend(discovered)
            print(f"✅ Discovered {len(discovered)} competitors")
        
        # Remove duplicates and limit
        final_competitors = list(set(final_competitors))[:15]
        
        if len(final_competitors) < 3:
            print("❌ Need at least 3 competitors to analyze.")
            print("💡 Tip: Provide more competitor usernames or ensure your username is valid for auto-discovery.")
            return False
        
        print(f"\n📊 Analyzing {len(final_competitors)} competitors:")
        for i, competitor in enumerate(final_competitors, 1):
            print(f"  {i}. @{competitor}")
        print()
        
        # Analyze each competitor's tweets
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
            
            # Small delay between requests
            if i < len(final_competitors) - 1:
                await asyncio.sleep(1)
        
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
        
        # Generate content ideas
        print("\n💡 Generating AI content ideas...")
        try:
            content_ideas = await analyzer.generate_content_ideas(patterns_analysis, competitor_tweets_data)
            print_content_ideas(content_ideas)
        except Exception as e:
            print(f"⚠️  AI content generation failed: {str(e)}")
            print("📝 Using fallback content ideas...")
            content_ideas = analyzer._generate_fallback_ideas(patterns_analysis)
            print_content_ideas(content_ideas)
        
        # Save results
        results = {
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
        
        filename = f"twitter_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to {filename}")
        print("✅ Analysis completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
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
    
    # Posting patterns
    posting_patterns = patterns_analysis.get('posting_patterns', {})
    best_days = posting_patterns.get('best_days', [])[:3]
    if best_days:
        print(f"\n📅 Best Posting Days:")
        for day, score in best_days:
            print(f"  • {day}: {score:.1f} avg engagement")

def print_content_ideas(content_ideas):
    """Print generated content ideas"""
    print("\n✨ Generated Content Ideas:")
    print("-" * 30)
    
    # Tweet ideas
    tweet_ideas = content_ideas.get('tweet_ideas', [])
    if tweet_ideas:
        print(f"\n🐦 Tweet Ideas ({len(tweet_ideas)}):")
        for i, tweet in enumerate(tweet_ideas[:5], 1):
            print(f"  {i}. {tweet}")
        if len(tweet_ideas) > 5:
            print(f"  ... and {len(tweet_ideas) - 5} more")
    
    # Hook ideas
    hook_ideas = content_ideas.get('hook_ideas', [])
    if hook_ideas:
        print(f"\n🎣 Hook Ideas ({len(hook_ideas)}):")
        for i, hook in enumerate(hook_ideas[:5], 1):
            print(f"  {i}. {hook}")
        if len(hook_ideas) > 5:
            print(f"  ... and {len(hook_ideas) - 5} more")
    
    # Strategy insights
    strategy_insights = content_ideas.get('strategy_insights', [])
    if strategy_insights:
        print(f"\n📈 Strategy Insights ({len(strategy_insights)}):")
        for i, insight in enumerate(strategy_insights, 1):
            print(f"  {i}. {insight}")

def main():
    """Main CLI function"""
    print_header()
    
    # Check environment
    print("🔧 Checking environment...")
    if not check_environment():
        print("\n💡 Set the required environment variables and try again.")
        sys.exit(1)
    
    print("\n✅ Environment OK")
    print()
    
    # Get user input
    config = get_user_input()
    
    # Confirm configuration
    print(f"\n📋 Configuration Summary:")
    print(f"  • User: @{config['user_username']}")
    print(f"  • Manual competitors: {len(config['competitor_usernames'])}")
    print(f"  • Auto-discover: {config['auto_discover']}")
    print(f"  • Tweets per competitor: {config['tweets_per_competitor']}")
    
    proceed = input("\nProceed with analysis? (y/n): ").strip().lower()
    if proceed != 'y':
        print("❌ Analysis cancelled")
        sys.exit(0)
    
    # Run analysis
    success = asyncio.run(run_analysis(config))
    
    if success:
        print("\n🎉 Twitter analysis completed successfully!")
        print("📊 Check the generated JSON file for detailed results.")
    else:
        print("\n💥 Analysis failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()