#!/usr/bin/env python3
"""
Automated demo of Twitter Competitor Analyzer (no user input required)
"""

import asyncio
import json
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

async def run_automated_demo():
    """Run a fully automated demo"""
    
    print("🐦 Twitter Competitor Analyzer - AUTOMATED DEMO")
    print("=" * 60)
    print("📝 Running demo with preset configuration (no API keys needed)")
    print()
    
    # Demo configuration
    config = {
        'user_username': '100xengineers',
        'competitor_usernames': ['naval', 'sama', 'paulg'],
        'tweets_per_competitor': 8,
        'auto_discover': True
    }
    
    print("📋 Demo Configuration:")
    print(f"  • Target user: @{config['user_username']}")
    print(f"  • Initial competitors: {', '.join('@' + c for c in config['competitor_usernames'])}")
    print(f"  • Auto-discover: {config['auto_discover']}")
    print(f"  • Tweets per competitor: {config['tweets_per_competitor']}")
    print()
    
    try:
        analyzer = DemoTwitterAnalyzer()
        
        print("🔍 Starting Analysis...")
        print("=" * 30)
        
        # Build competitor list
        final_competitors = list(config['competitor_usernames'])
        
        # Auto-discover competitors
        if config['auto_discover'] and config['user_username']:
            print(f"🔍 Auto-discovering competitors for @{config['user_username']}...")
            discovered = await analyzer.discover_competitors(config['user_username'], 4)
            final_competitors.extend(discovered)
            final_competitors = list(set(final_competitors))[:8]  # Limit for demo
            print(f"✅ Discovered {len(discovered)} additional competitors")
        
        print(f"\n📊 Final competitor list ({len(final_competitors)} accounts):")
        for i, competitor in enumerate(final_competitors, 1):
            print(f"  {i}. @{competitor}")
        print()
        
        # Analyze each competitor's tweets
        competitor_tweets_data = {}
        
        for i, username in enumerate(final_competitors):
            print(f"📱 [{i+1}/{len(final_competitors)}] Analyzing @{username}...")
            
            tweets = await analyzer.get_top_performing_tweets(username, config['tweets_per_competitor'])
            
            if tweets:
                competitor_tweets_data[username] = tweets
                avg_engagement = sum(t['engagement_score'] for t in tweets) / len(tweets)
                print(f"  ✅ Found {len(tweets)} tweets (avg engagement: {avg_engagement:.1f})")
                
                # Show top tweet preview
                top_tweet = tweets[0]
                text_preview = top_tweet.get('text', '')[:70] + "..." if len(top_tweet.get('text', '')) > 70 else top_tweet.get('text', '')
                print(f"  🔥 Top tweet: \"{text_preview}\"")
                print(f"      Engagement: {top_tweet.get('engagement_score', 0):.1f} ({top_tweet.get('likes', 0)} likes, {top_tweet.get('retweets', 0)} RTs)")
            else:
                print(f"  ⚠️  No tweets found")
            
            print()  # Add spacing between competitors
        
        if not competitor_tweets_data:
            print("❌ No competitor data available")
            return False
        
        total_tweets = sum(len(tweets) for tweets in competitor_tweets_data.values())
        print(f"📈 Analysis Summary:")
        print(f"  • Competitors analyzed: {len(competitor_tweets_data)}")
        print(f"  • Total tweets analyzed: {total_tweets}")
        print()
        
        # Analyze patterns
        print("🔍 Analyzing patterns across all tweets...")
        patterns_analysis = await analyzer.analyze_tweet_patterns(competitor_tweets_data)
        
        # Display detailed pattern insights
        print("\n📊 PATTERN ANALYSIS RESULTS")
        print("=" * 40)
        
        print(f"📈 Overall engagement: {patterns_analysis.get('avg_engagement_score', 0):.1f} average score")
        print()
        
        # Top hashtags
        top_hashtags = patterns_analysis.get('top_hashtags', [])[:8]
        if top_hashtags:
            print("🏷️  Most Popular Hashtags:")
            for i, hashtag_data in enumerate(top_hashtags, 1):
                print(f"  {i:2d}. #{hashtag_data['hashtag']:<15} ({hashtag_data['frequency']:2d} uses)")
            print()
        
        # Hook patterns
        hook_patterns = patterns_analysis.get('hook_patterns', {})
        top_hooks = hook_patterns.get('top_performing_hooks', [])[:5]
        if top_hooks:
            print("🎣 Top Performing Hook Examples:")
            for i, hook_data in enumerate(top_hooks, 1):
                hook_text = hook_data['hook'][:60] + "..." if len(hook_data['hook']) > 60 else hook_data['hook']
                print(f"  {i}. \"{hook_text}\"")
                print(f"     Engagement: {hook_data['engagement_score']:.1f} (@{hook_data['competitor']})")
            print()
        
        # Common hook starters
        hook_starters = hook_patterns.get('common_hook_starters', [])[:5]
        if hook_starters:
            print("🚀 Most Effective Hook Starters:")
            for i, starter_data in enumerate(hook_starters, 1):
                print(f"  {i}. \"{starter_data['starter']}...\" (avg: {starter_data['avg_engagement']:.1f}, used {starter_data['count']}x)")
            print()
        
        # Topic themes
        topics = patterns_analysis.get('topic_themes', [])[:8]
        if topics:
            print("📝 Common Topic Themes:")
            topic_chunks = [topics[i:i+4] for i in range(0, len(topics), 4)]
            for chunk in topic_chunks:
                print(f"  • {' • '.join(chunk)}")
            print()
        
        # Length patterns
        length_patterns = patterns_analysis.get('optimal_length', {})
        if length_patterns:
            print("📏 Tweet Length Performance:")
            sorted_lengths = sorted(length_patterns.items(), key=lambda x: x[1].get('avg_engagement', 0), reverse=True)
            for length_range, data in sorted_lengths:
                avg_eng = data.get('avg_engagement', 0)
                count = data.get('count', 0)
                print(f"  • {length_range:<15}: {avg_eng:6.1f} avg engagement ({count:2d} tweets)")
            print()
        
        # Posting patterns
        posting_patterns = patterns_analysis.get('posting_patterns', {})
        best_days = posting_patterns.get('best_days', [])[:5]
        if best_days:
            print("📅 Best Days to Post:")
            for day, score in best_days:
                print(f"  • {day:<9}: {score:.1f} avg engagement")
            print()
        
        best_hours = posting_patterns.get('best_hours', [])[:5]
        if best_hours:
            print("🕐 Best Hours to Post:")
            for hour, score in best_hours:
                time_str = f"{hour:02d}:00"
                print(f"  • {time_str:<6}: {score:.1f} avg engagement")
            print()
        
        # Generate content ideas
        print("💡 Generating Content Ideas...")
        print("=" * 35)
        content_ideas = await analyzer.generate_content_ideas(patterns_analysis, competitor_tweets_data)
        
        # Display content ideas
        tweet_ideas = content_ideas.get('tweet_ideas', [])
        if tweet_ideas:
            print(f"\n🐦 TWEET IDEAS ({len(tweet_ideas)} suggestions):")
            print("-" * 45)
            for i, tweet in enumerate(tweet_ideas, 1):
                print(f"{i:2d}. {tweet}")
            print()
        
        hook_ideas = content_ideas.get('hook_ideas', [])
        if hook_ideas:
            print(f"🎣 HOOK FORMULAS ({len(hook_ideas)} patterns):")
            print("-" * 40)
            # Display in columns
            hook_chunks = [hook_ideas[i:i+2] for i in range(0, len(hook_ideas), 2)]
            for chunk in hook_chunks:
                if len(chunk) == 2:
                    print(f"  • {chunk[0]:<25} • {chunk[1]}")
                else:
                    print(f"  • {chunk[0]}")
            print()
        
        strategy_insights = content_ideas.get('strategy_insights', [])
        if strategy_insights:
            print(f"📈 STRATEGY INSIGHTS ({len(strategy_insights)} recommendations):")
            print("-" * 50)
            for i, insight in enumerate(strategy_insights, 1):
                print(f"{i}. {insight}")
            print()
        
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
            "content_ideas": content_ideas,
            "competitor_data": {
                username: {
                    "tweets_count": len(tweets),
                    "avg_engagement": sum(t['engagement_score'] for t in tweets) / len(tweets),
                    "top_tweet": tweets[0] if tweets else None
                }
                for username, tweets in competitor_tweets_data.items()
            }
        }
        
        filename = f"twitter_demo_results.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print("💾 RESULTS SAVED")
        print("-" * 20)
        print(f"📄 Detailed results: {filename}")
        print(f"📊 {total_tweets} tweets analyzed from {len(competitor_tweets_data)} competitors")
        print(f"💡 {len(tweet_ideas)} tweet ideas and {len(hook_ideas)} hook formulas generated")
        
        print("\n✅ DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("🚀 This demo shows how the Twitter agent:")
        print("   • Discovers competitor accounts automatically")
        print("   • Analyzes tweet patterns and engagement")
        print("   • Extracts successful content formulas")
        print("   • Generates actionable content ideas")
        print("\n💡 For real Twitter data, set up API keys and use cli_test.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the automated demo"""
    success = asyncio.run(run_automated_demo())
    return success

if __name__ == "__main__":
    main()