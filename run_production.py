#!/usr/bin/env python3
"""
Production Twitter Agent Runner - Automated execution with real API calls
"""

import asyncio
import json
import os
from datetime import datetime
from twitter_analyzer import TwitterCompetitorAnalyzer

async def run_production_analysis():
    """Run production analysis with real API calls"""
    
    print("🐦 Twitter Competitor Analyzer - PRODUCTION RUN")
    print("=" * 60)
    print("🚀 Using real API keys for live Twitter data analysis")
    print()
    
    # Check API keys
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ OPENROUTER_API_KEY not set")
        return False
    
    if not os.getenv('APIFY_TOKEN'):
        print("❌ APIFY_TOKEN not set")
        return False
    
    print("✅ API keys configured")
    print()
    
    # Production configuration - analyzing real tech influencers
    config = {
        'user_username': 'elonmusk',  # High-profile user for competitor discovery
        'competitor_usernames': ['naval', 'sama', 'paulg', 'garyvee'],  # Manual competitors
        'tweets_per_competitor': 15,  # More tweets for better analysis
        'auto_discover': True,
        'min_competitors': 8
    }
    
    print("📋 Production Configuration:")
    print(f"  • Target user: @{config['user_username']}")
    print(f"  • Manual competitors: {', '.join('@' + c for c in config['competitor_usernames'])}")
    print(f"  • Auto-discover: {config['auto_discover']}")
    print(f"  • Tweets per competitor: {config['tweets_per_competitor']}")
    print(f"  • Minimum competitors: {config['min_competitors']}")
    print()
    
    try:
        analyzer = TwitterCompetitorAnalyzer()
        
        print("🔍 Starting Production Analysis...")
        print("=" * 40)
        
        # Build competitor list
        final_competitors = list(config['competitor_usernames'])
        
        # Auto-discover competitors if needed
        if config['auto_discover'] and config['user_username']:
            print(f"🔍 Auto-discovering competitors for @{config['user_username']}...")
            try:
                discovered = await analyzer.discover_competitors(
                    config['user_username'], 
                    config['min_competitors'] - len(final_competitors)
                )
                final_competitors.extend(discovered)
                print(f"✅ Discovered {len(discovered)} additional competitors")
            except Exception as e:
                print(f"⚠️  Auto-discovery failed: {e}")
                print("📝 Continuing with manual competitor list...")
        
        # Remove duplicates and limit
        final_competitors = list(set(final_competitors))[:12]  # Limit for production
        
        if len(final_competitors) < 3:
            print("❌ Need at least 3 competitors to analyze")
            return False
        
        print(f"\n📊 Final competitor list ({len(final_competitors)} accounts):")
        for i, competitor in enumerate(final_competitors, 1):
            print(f"  {i:2d}. @{competitor}")
        print()
        
        # Analyze each competitor's tweets
        competitor_tweets_data = {}
        successful_analyses = 0
        
        for i, username in enumerate(final_competitors):
            print(f"📱 [{i+1}/{len(final_competitors)}] Analyzing @{username}...")
            
            try:
                tweets = await analyzer.get_top_performing_tweets(username, config['tweets_per_competitor'])
                
                if tweets:
                    competitor_tweets_data[username] = tweets
                    avg_engagement = sum(t['engagement_score'] for t in tweets) / len(tweets)
                    successful_analyses += 1
                    
                    print(f"  ✅ Found {len(tweets)} tweets (avg engagement: {avg_engagement:.1f})")
                    
                    # Show top tweet preview
                    top_tweet = tweets[0]
                    text_preview = top_tweet.get('text', '')[:70] + "..." if len(top_tweet.get('text', '')) > 70 else top_tweet.get('text', '')
                    print(f"  🔥 Top tweet: \"{text_preview}\"")
                    print(f"      💫 {top_tweet.get('likes', 0)} likes, {top_tweet.get('retweets', 0)} RTs, {top_tweet.get('replies', 0)} replies")
                else:
                    print(f"  ⚠️  No tweets found")
                    
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                continue
            
            # Rate limiting delay
            if i < len(final_competitors) - 1:
                print(f"  😴 Rate limiting pause...")
                await asyncio.sleep(3)
            
            print()
        
        if not competitor_tweets_data:
            print("❌ No competitor data available")
            return False
        
        total_tweets = sum(len(tweets) for tweets in competitor_tweets_data.values())
        print(f"📈 Production Analysis Summary:")
        print(f"  • Competitors successfully analyzed: {successful_analyses}/{len(final_competitors)}")
        print(f"  • Total tweets analyzed: {total_tweets}")
        print(f"  • Analysis success rate: {(successful_analyses/len(final_competitors)*100):.1f}%")
        print()
        
        # Analyze patterns
        print("🔍 Analyzing patterns across all competitor tweets...")
        patterns_analysis = await analyzer.analyze_tweet_patterns(competitor_tweets_data)
        
        # Display detailed insights
        print("\n📊 PRODUCTION PATTERN ANALYSIS")
        print("=" * 45)
        
        avg_engagement = patterns_analysis.get('avg_engagement_score', 0)
        print(f"📈 Overall Performance: {avg_engagement:.1f} average engagement score")
        print()
        
        # Top hashtags
        top_hashtags = patterns_analysis.get('top_hashtags', [])[:10]
        if top_hashtags:
            print("🏷️  Most Effective Hashtags:")
            for i, hashtag_data in enumerate(top_hashtags, 1):
                print(f"  {i:2d}. #{hashtag_data['hashtag']:<20} ({hashtag_data['frequency']:2d} uses)")
            print()
        
        # Hook patterns
        hook_patterns = patterns_analysis.get('hook_patterns', {})
        top_hooks = hook_patterns.get('top_performing_hooks', [])[:8]
        if top_hooks:
            print("🎣 Highest Performing Hook Examples:")
            for i, hook_data in enumerate(top_hooks, 1):
                hook_text = hook_data['hook'][:65] + "..." if len(hook_data['hook']) > 65 else hook_data['hook']
                print(f"  {i}. \"{hook_text}\"")
                print(f"     💫 {hook_data['engagement_score']:.1f} engagement (@{hook_data['competitor']})")
            print()
        
        # Hook starters
        hook_starters = hook_patterns.get('common_hook_starters', [])[:8]
        if hook_starters:
            print("🚀 Most Successful Hook Starters:")
            for i, starter_data in enumerate(hook_starters, 1):
                print(f"  {i}. \"{starter_data['starter']}...\"")
                print(f"     📊 {starter_data['avg_engagement']:.1f} avg engagement ({starter_data['count']} uses)")
            print()
        
        # Topic themes
        topics = patterns_analysis.get('topic_themes', [])[:12]
        if topics:
            print("📝 Trending Topic Themes:")
            # Display in rows of 4
            for i in range(0, len(topics), 4):
                row = topics[i:i+4]
                print(f"  • {' • '.join(row)}")
            print()
        
        # Posting optimization
        posting_patterns = patterns_analysis.get('posting_patterns', {})
        best_days = posting_patterns.get('best_days', [])[:5]
        if best_days:
            print("📅 Optimal Posting Schedule:")
            for day, score in best_days:
                print(f"  • {day:<10}: {score:.1f} avg engagement")
            print()
        
        # Generate AI-powered content ideas
        print("🤖 Generating AI-Powered Content Strategy...")
        print("=" * 50)
        
        try:
            content_ideas = await analyzer.generate_content_ideas(patterns_analysis, competitor_tweets_data)
            ai_generated = True
            print("✅ AI content generation successful")
        except Exception as e:
            print(f"⚠️  AI generation failed: {e}")
            print("📝 Using fallback content generation...")
            content_ideas = analyzer._generate_fallback_ideas(patterns_analysis)
            ai_generated = False
        
        print()
        
        # Display content strategy
        tweet_ideas = content_ideas.get('tweet_ideas', [])
        if tweet_ideas:
            print(f"🐦 CONTENT IDEAS ({len(tweet_ideas)} suggestions):")
            print("-" * 50)
            for i, tweet in enumerate(tweet_ideas, 1):
                print(f"{i:2d}. {tweet}")
            print()
        
        hook_ideas = content_ideas.get('hook_ideas', [])
        if hook_ideas:
            print(f"🎣 HOOK TEMPLATES ({len(hook_ideas)} patterns):")
            print("-" * 45)
            # Display in columns
            for i in range(0, len(hook_ideas), 2):
                if i + 1 < len(hook_ideas):
                    print(f"  • {hook_ideas[i]:<30} • {hook_ideas[i+1]}")
                else:
                    print(f"  • {hook_ideas[i]}")
            print()
        
        strategy_insights = content_ideas.get('strategy_insights', [])
        if strategy_insights:
            print(f"📈 STRATEGIC RECOMMENDATIONS:")
            print("-" * 35)
            for i, insight in enumerate(strategy_insights, 1):
                print(f"{i}. {insight}")
            print()
        
        # Save comprehensive results
        results = {
            "production_run": True,
            "ai_generated": ai_generated,
            "timestamp": datetime.now().isoformat(),
            "config": config,
            "execution_summary": {
                "competitors_analyzed": successful_analyses,
                "total_competitors_attempted": len(final_competitors),
                "total_tweets_analyzed": total_tweets,
                "success_rate": successful_analyses / len(final_competitors),
                "avg_engagement_score": avg_engagement
            },
            "patterns_analysis": patterns_analysis,
            "content_ideas": content_ideas,
            "competitor_performance": {
                username: {
                    "tweets_analyzed": len(tweets),
                    "avg_engagement": sum(t['engagement_score'] for t in tweets) / len(tweets),
                    "top_performing_tweet": {
                        "text": tweets[0]['text'][:100] + "..." if len(tweets[0]['text']) > 100 else tweets[0]['text'],
                        "engagement_score": tweets[0]['engagement_score'],
                        "metrics": {
                            "likes": tweets[0]['likes'],
                            "retweets": tweets[0]['retweets'],
                            "replies": tweets[0]['replies']
                        }
                    } if tweets else None
                }
                for username, tweets in competitor_tweets_data.items()
            }
        }
        
        filename = f"production_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print("💾 PRODUCTION RESULTS SUMMARY")
        print("=" * 35)
        print(f"📄 Detailed results: {filename}")
        print(f"🎯 Analysis success rate: {(successful_analyses/len(final_competitors)*100):.1f}%")
        print(f"📊 {total_tweets} tweets from {successful_analyses} competitors analyzed")
        print(f"💡 {len(tweet_ideas)} content ideas generated")
        print(f"🎣 {len(hook_ideas)} hook templates provided")
        print(f"🤖 AI-powered generation: {'✅ Yes' if ai_generated else '❌ Fallback used'}")
        
        print(f"\n✅ PRODUCTION ANALYSIS COMPLETED!")
        print("=" * 50)
        print("🚀 Key Insights:")
        print(f"   • Average engagement: {avg_engagement:.1f}")
        print(f"   • Top performing hook: \"{top_hooks[0]['hook'][:50]}...\"" if top_hooks else "   • No hook data available")
        print(f"   • Best posting day: {best_days[0][0]}" if best_days else "   • No timing data available")
        print(f"   • Most common theme: {topics[0]}" if topics else "   • No theme data available")
        
        return True
        
    except Exception as e:
        print(f"❌ Production analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the production analysis"""
    success = asyncio.run(run_production_analysis())
    return success

if __name__ == "__main__":
    main()