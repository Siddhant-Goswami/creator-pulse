#!/usr/bin/env python3

import os
import asyncio
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from apify import Actor
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwitterCompetitorAnalyzer:
    def __init__(self):
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        
        self.apify_token = os.getenv('APIFY_TOKEN')
        if not self.apify_token:
            raise ValueError("APIFY_TOKEN environment variable is required")
    
    async def discover_competitors(self, username: str, min_competitors: int = 5) -> List[str]:
        """Discover competitor accounts based on user's Twitter profile"""
        try:
            # Use Apify's Twitter scraper to get user's following/followers
            competitors = set()
            
            # Strategy: Get accounts that the user follows and accounts that follow similar users
            input_data = {
                "handles": [username],
                "tweetsDesired": 0,
                "addUserInfo": True,
                "onlyImage": False,
                "onlyQuote": False,
                "onlyTwitterBlue": False
            }
            
            # This would normally call Apify's Twitter actor, but for now we'll simulate
            # In a real implementation, you'd call: await self._call_apify_actor("apify/twitter-scraper", input_data)
            
            # For demo purposes, let's return some relevant accounts in the tech/business space
            if "100xengineers" in username.lower() or "engineer" in username.lower():
                competitors.update([
                    "naval", "elonmusk", "sama", "paulg", "dhh", "kentcdodds",
                    "dan_abramov", "ryanflorence", "wesbos", "addyosmani"
                ])
            elif "varun" in username.lower() or "entrepreneur" in username.lower():
                competitors.update([
                    "elonmusk", "naval", "sama", "paulg", "garyvee", "dharmesh",
                    "neerajkaushal", "kunalshah", "rohitjain_007", "rahulvohra"
                ])
            else:
                # General tech/business accounts
                competitors.update([
                    "naval", "sama", "paulg", "garyvee", "dharmesh", "kentcdodds",
                    "dan_abramov", "wesbos", "addyosmani", "elonmusk"
                ])
            
            competitor_list = list(competitors)[:min_competitors * 2]
            logger.info(f"Discovered {len(competitor_list)} potential competitors for @{username}")
            
            return competitor_list
            
        except Exception as e:
            logger.error(f"Error discovering competitors for @{username}: {e}")
            return []
    
    async def get_top_performing_tweets(self, username: str, count: int = 20) -> List[Dict[str, Any]]:
        """Get top performing tweets from a Twitter account using Apify"""
        try:
            input_data = {
                "handles": [username],
                "tweetsDesired": count * 2,  # Get more to filter for top performers
                "addUserInfo": True,
                "onlyImage": False,
                "onlyQuote": False,
                "onlyTwitterBlue": False
            }
            
            # In a real implementation, call Apify's Twitter scraper
            # For now, let's simulate realistic Twitter data
            sample_tweets = await self._generate_sample_tweets(username, count)
            
            # Sort by engagement (likes + retweets + replies) and return top performers
            sample_tweets.sort(key=lambda x: x.get('engagement_score', 0), reverse=True)
            top_tweets = sample_tweets[:count]
            
            logger.info(f"Retrieved {len(top_tweets)} top performing tweets from @{username}")
            return top_tweets
            
        except Exception as e:
            logger.error(f"Error getting tweets from @{username}: {e}")
            return []
    
    async def _generate_sample_tweets(self, username: str, count: int) -> List[Dict[str, Any]]:
        """Generate sample tweet data for demonstration"""
        # This simulates what would come from Apify's Twitter scraper
        sample_tweets = []
        
        # Define sample content based on username patterns
        if "100x" in username.lower() or "engineer" in username.lower():
            content_templates = [
                "🚀 Here's the secret to 10x your coding productivity that most developers miss:",
                "Stop doing this if you want to become a senior developer:",
                "The harsh truth about landing your first tech job in 2024:",
                "5 JavaScript concepts that will make you a better developer:",
                "Why most developers fail at system design interviews:",
                "This React pattern changed how I write components forever:",
                "The #1 mistake junior developers make with databases:",
                "How to debug like a senior developer (thread):",
                "CSS tricks that will blow your mind:",
                "Docker concepts every developer should know:"
            ]
        elif "varun" in username.lower() or "entrepreneur" in username.lower():
            content_templates = [
                "🔥 The startup advice that nobody gives you:",
                "This is why 90% of startups fail (and how to avoid it):",
                "The harsh reality of building a unicorn startup:",
                "Fundraising lessons I learned the hard way:",
                "How to build a product people actually want:",
                "The entrepreneurship myths that are keeping you broke:",
                "Why most business ideas fail before they start:",
                "Building a team when you have no money:",
                "The psychology of successful entrepreneurs:",
                "Scaling from 0 to $1M ARR (lessons learned):"
            ]
        else:
            content_templates = [
                "The best advice I ever received:",
                "This changed my entire perspective on success:",
                "Here's what I wish I knew 5 years ago:",
                "The uncomfortable truth about building wealth:",
                "Why most people never reach their potential:",
                "This mindset shift transformed my career:",
                "The skills that actually matter in 2024:",
                "How to think like a successful person:",
                "The difference between busy and productive:",
                "Why networking is overrated (and what works instead):"
            ]
        
        for i in range(count):
            base_engagement = 100 + (i * 50)  # Simulate decreasing engagement
            sample_tweets.append({
                "id": f"tweet_{username}_{i}",
                "url": f"https://twitter.com/{username}/status/{1000000000000000000 + i}",
                "text": content_templates[i % len(content_templates)],
                "likes": base_engagement + (i * 20),
                "retweets": base_engagement // 4,
                "replies": base_engagement // 6,
                "engagement_score": base_engagement * 1.5,
                "created_at": (datetime.now() - timedelta(days=i*2)).isoformat(),
                "hashtags": self._extract_hashtags_from_template(content_templates[i % len(content_templates)]),
                "mentions": []
            })
        
        return sample_tweets
    
    def _extract_hashtags_from_template(self, text: str) -> List[str]:
        """Extract or infer hashtags from tweet content"""
        hashtags = []
        if "javascript" in text.lower() or "js" in text.lower():
            hashtags.extend(["javascript", "webdev", "coding"])
        if "react" in text.lower():
            hashtags.extend(["react", "frontend", "webdev"])
        if "startup" in text.lower():
            hashtags.extend(["startup", "entrepreneur", "business"])
        if "developer" in text.lower() or "coding" in text.lower():
            hashtags.extend(["developer", "coding", "programming"])
        if "css" in text.lower():
            hashtags.extend(["css", "webdev", "frontend"])
        if "docker" in text.lower():
            hashtags.extend(["docker", "devops", "containers"])
        
        return hashtags[:3]  # Limit to 3 hashtags
    
    async def analyze_tweet_patterns(self, all_tweets_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Analyze patterns across all competitor tweets"""
        
        # Collect all tweets for analysis
        all_tweets = []
        for username, tweets in all_tweets_data.items():
            for tweet in tweets:
                tweet['competitor'] = username
                all_tweets.append(tweet)
        
        if not all_tweets:
            return {"error": "No tweet data to analyze"}
        
        # Analyze patterns
        patterns = {
            "total_tweets_analyzed": len(all_tweets),
            "avg_engagement_score": sum(t['engagement_score'] for t in all_tweets) / len(all_tweets),
            "top_hashtags": self._get_top_hashtags(all_tweets),
            "hook_patterns": self._analyze_hook_patterns(all_tweets),
            "optimal_length": self._analyze_length_patterns(all_tweets),
            "posting_patterns": self._analyze_posting_patterns(all_tweets),
            "topic_themes": self._analyze_topic_themes(all_tweets),
            "engagement_insights": self._analyze_engagement_patterns(all_tweets)
        }
        
        return patterns
    
    def _get_top_hashtags(self, tweets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get most frequently used hashtags"""
        hashtag_counts = {}
        
        for tweet in tweets:
            for hashtag in tweet.get('hashtags', []):
                hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
        
        # Sort by frequency and return top 15
        top_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)[:15]
        return [{"hashtag": tag, "frequency": count} for tag, count in top_hashtags]
    
    def _analyze_hook_patterns(self, tweets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze opening hook patterns in tweets"""
        hooks = []
        
        for tweet in tweets:
            text = tweet.get('text', '')
            if text:
                # Get first part of tweet as hook (up to first colon or period)
                hook = text.split(':')[0].split('.')[0][:100].strip()
                if hook:
                    hooks.append({
                        "hook": hook,
                        "engagement_score": tweet['engagement_score'],
                        "competitor": tweet['competitor']
                    })
        
        # Sort by engagement
        hooks.sort(key=lambda x: x['engagement_score'], reverse=True)
        
        return {
            "total_hooks_analyzed": len(hooks),
            "top_performing_hooks": hooks[:10],
            "common_hook_starters": self._find_common_hook_starters(hooks)
        }
    
    def _find_common_hook_starters(self, hooks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find common ways hooks start"""
        starters = {}
        
        for hook_data in hooks:
            hook = hook_data['hook'].lower()
            # Get first 2-3 words
            words = hook.split()[:3]
            if len(words) >= 2:
                starter = ' '.join(words)
                
                if starter not in starters:
                    starters[starter] = {"count": 0, "avg_engagement": 0, "examples": []}
                
                starters[starter]["count"] += 1
                starters[starter]["avg_engagement"] += hook_data['engagement_score']
                starters[starter]["examples"].append(hook_data['hook'])
        
        # Calculate averages and sort
        for starter in starters:
            if starters[starter]["count"] > 0:
                starters[starter]["avg_engagement"] /= starters[starter]["count"]
                starters[starter]["examples"] = starters[starter]["examples"][:3]
        
        sorted_starters = sorted(starters.items(), key=lambda x: x[1]['avg_engagement'], reverse=True)
        return [{"starter": starter, **data} for starter, data in sorted_starters[:10] if data["count"] > 1]
    
    def _analyze_length_patterns(self, tweets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze optimal tweet length patterns"""
        length_performance = {}
        
        for tweet in tweets:
            text_length = len(tweet.get('text', ''))
            length_range = self._get_length_range(text_length)
            
            if length_range not in length_performance:
                length_performance[length_range] = {"count": 0, "total_engagement": 0}
            
            length_performance[length_range]["count"] += 1
            length_performance[length_range]["total_engagement"] += tweet['engagement_score']
        
        # Calculate averages
        for range_key in length_performance:
            count = length_performance[range_key]["count"]
            if count > 0:
                length_performance[range_key]["avg_engagement"] = length_performance[range_key]["total_engagement"] / count
        
        return length_performance
    
    def _get_length_range(self, length: int) -> str:
        """Categorize tweet length into ranges"""
        if length <= 50:
            return "0-50 chars"
        elif length <= 100:
            return "51-100 chars"
        elif length <= 200:
            return "101-200 chars"
        else:
            return "200+ chars"
    
    def _analyze_posting_patterns(self, tweets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze when top performing tweets were posted"""
        from collections import defaultdict
        
        day_performance = defaultdict(list)
        hour_performance = defaultdict(list)
        
        for tweet in tweets:
            try:
                date = datetime.fromisoformat(tweet['created_at'].replace('Z', '+00:00'))
                day_name = date.strftime('%A')
                hour = date.hour
                
                day_performance[day_name].append(tweet['engagement_score'])
                hour_performance[hour].append(tweet['engagement_score'])
                
            except Exception as e:
                continue
        
        # Calculate averages
        best_days = {day: sum(scores)/len(scores) for day, scores in day_performance.items() if len(scores) > 0}
        best_hours = {hour: sum(scores)/len(scores) for hour, scores in hour_performance.items() if len(scores) > 0}
        
        return {
            "best_days": sorted(best_days.items(), key=lambda x: x[1], reverse=True),
            "best_hours": sorted(best_hours.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def _analyze_topic_themes(self, tweets: List[Dict[str, Any]]) -> List[str]:
        """Extract common topic themes from tweets"""
        all_text = []
        
        for tweet in tweets:
            text = tweet.get('text', '')
            if text:
                # Clean text (remove hashtags, mentions, emojis, URLs)
                clean_text = re.sub(r'[#@]\w+', '', text)
                clean_text = re.sub(r'http\S+', '', clean_text)
                clean_text = re.sub(r'[^\w\s]', ' ', clean_text)
                all_text.append(clean_text.lower())
        
        # Simple keyword extraction
        combined_text = ' '.join(all_text)
        words = combined_text.split()
        
        # Filter common words and count frequency
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'cant', 'dont', 'wont', 'this', 'that', 'these', 'those', 'a', 'an', 'you', 'your', 'if', 'how', 'why', 'what', 'when', 'where'}
        
        word_freq = {}
        for word in words:
            if len(word) > 3 and word not in common_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top themes
        top_themes = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:15]
        return [word for word, freq in top_themes if freq > 2]
    
    def _analyze_engagement_patterns(self, tweets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze what drives engagement"""
        high_engagement = [t for t in tweets if t['engagement_score'] > 
                          sum(tw['engagement_score'] for tw in tweets) / len(tweets)]
        
        patterns = {
            "avg_likes_to_retweets_ratio": 0,
            "high_engagement_characteristics": [],
            "optimal_tweet_structure": []
        }
        
        if high_engagement:
            # Calculate likes to retweets ratio
            total_likes = sum(t['likes'] for t in high_engagement)
            total_retweets = sum(t['retweets'] for t in high_engagement)
            if total_retweets > 0:
                patterns["avg_likes_to_retweets_ratio"] = total_likes / total_retweets
            
            # Analyze characteristics of high-engagement tweets
            question_tweets = [t for t in high_engagement if '?' in t['text']]
            if question_tweets:
                patterns["high_engagement_characteristics"].append("Questions perform well")
            
            emoji_tweets = [t for t in high_engagement if any(ord(c) > 127 for c in t['text'])]
            if len(emoji_tweets) > len(high_engagement) * 0.3:
                patterns["high_engagement_characteristics"].append("Emojis boost engagement")
            
            thread_tweets = [t for t in high_engagement if 'thread' in t['text'].lower()]
            if thread_tweets:
                patterns["high_engagement_characteristics"].append("Threads generate discussion")
        
        return patterns
    
    async def generate_content_ideas(self, patterns_analysis: Dict[str, Any], competitor_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[str]]:
        """Generate topic and hook ideas based on Twitter competitor analysis"""
        
        # Prepare comprehensive analysis for AI
        analysis_summary = {
            "patterns": patterns_analysis,
            "top_performing_content": self._get_top_performing_content_sample(competitor_data),
            "competitor_count": len(competitor_data)
        }
        
        prompt = f"""
Based on this comprehensive Twitter competitor analysis, generate content ideas:

ANALYSIS SUMMARY:
- Total tweets analyzed: {patterns_analysis.get('total_tweets_analyzed', 0)}
- Average engagement score: {patterns_analysis.get('avg_engagement_score', 0):.1f}
- Top hashtags: {[h['hashtag'] for h in patterns_analysis.get('top_hashtags', [])[:10]]}
- Common topic themes: {patterns_analysis.get('topic_themes', [])}
- Top performing hook starters: {[h['starter'] for h in patterns_analysis.get('hook_patterns', {}).get('common_hook_starters', [])[:5]]}
- Engagement insights: {patterns_analysis.get('engagement_insights', {})}

TOP PERFORMING CONTENT EXAMPLES:
{json.dumps(analysis_summary['top_performing_content'], indent=2)}

Please generate:

1. **TWEET IDEAS** (10 high-engagement tweet concepts):
   - Focus on topics that competitors are succeeding with but could be improved
   - Include various formats: questions, threads, tips, controversial takes
   - Use successful patterns but make them unique

2. **HOOK IDEAS** (15 compelling hook formulas based on top-performing patterns):
   - Use successful hook starters but make them fresh
   - Focus on hooks that generated high engagement
   - Include various hook types (question, statement, story, controversial, etc.)

3. **CONTENT STRATEGY INSIGHTS** (5 key strategic recommendations):
   - Optimal posting patterns and timing
   - Content structure recommendations based on length analysis
   - Engagement strategies based on analysis
   - Hashtag and topic strategies

Format as JSON with keys: "tweet_ideas", "hook_ideas", "strategy_insights"
"""
        
        async with aiohttp.ClientSession() as session:
            try:
                headers = {
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "anthropic/claude-3-haiku",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 2000,
                    "temperature": 0.8
                }
                
                async with session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status != 200:
                        logger.error(f"OpenRouter API error: {response.status}")
                        return self._generate_fallback_ideas(patterns_analysis)
                    
                    result = await response.json()
                    content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                    
                    try:
                        ideas = json.loads(content)
                        return ideas
                    except json.JSONDecodeError:
                        logger.warning("Failed to parse AI response as JSON, using fallback")
                        return self._generate_fallback_ideas(patterns_analysis)
                        
            except Exception as e:
                logger.error(f"Error generating content ideas: {str(e)}")
                return self._generate_fallback_ideas(patterns_analysis)
    
    def _get_top_performing_content_sample(self, competitor_data: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Get sample of top performing content for AI analysis"""
        all_tweets = []
        
        for username, tweets in competitor_data.items():
            for tweet in tweets:
                tweet['competitor'] = username
                all_tweets.append(tweet)
        
        # Sort by engagement and return top 5
        all_tweets.sort(key=lambda x: x['engagement_score'], reverse=True)
        
        return [{
            "competitor": tweet['competitor'],
            "text": tweet['text'][:200] + "..." if len(tweet['text']) > 200 else tweet['text'],
            "engagement_score": tweet['engagement_score'],
            "likes": tweet['likes'],
            "retweets": tweet['retweets'],
            "hashtags": tweet['hashtags']
        } for tweet in all_tweets[:5]]
    
    def _generate_fallback_ideas(self, patterns_analysis: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate basic content ideas if AI fails"""
        top_hashtags = [h['hashtag'] for h in patterns_analysis.get('top_hashtags', [])[:5]]
        themes = patterns_analysis.get('topic_themes', [])[:5]
        
        return {
            "tweet_ideas": [
                f"Thread: {theme} mistakes everyone makes" for theme in themes[:3]
            ] + [
                f"Hot take: {hashtag} is overrated. Here's why..." for hashtag in top_hashtags[:2]
            ] + [
                "What's the worst advice you've received about your career?",
                "Unpopular opinion: Most 'productivity' advice is just procrastination",
                "The skill that changed my life (and why schools don't teach it)",
                "If you're struggling with imposter syndrome, read this",
                "Things I wish I knew before starting my career"
            ],
            "hook_ideas": [
                "Unpopular opinion:",
                "Hot take:",
                "The harsh truth about",
                "What nobody tells you about",
                "I wish someone told me",
                "Stop doing this if you want to",
                "Here's what I learned after",
                "The biggest lie about",
                "Why everyone gets this wrong:",
                "This changed everything for me:",
                "Thread: Why",
                "Controversial take:",
                "The uncomfortable truth:",
                "What I wish I knew:",
                "Stop believing that"
            ],
            "strategy_insights": [
                "Questions and controversial takes drive engagement",
                "Threads perform better than single tweets for complex topics",
                "Personal stories resonate more than generic advice",
                "Timing matters: post when your audience is most active",
                "Engage with replies within the first hour for better reach"
            ]
        }


# Integration with main script
async def main():
    async with Actor:
        # Get input
        actor_input = await Actor.get_input() or {}
        
        # Debug: print the raw input
        logger.info(f"Raw actor input: {actor_input}")
        
        user_username = actor_input.get('user_username', '')
        competitor_usernames = actor_input.get('competitor_usernames', [])
        auto_discover = actor_input.get('auto_discover_competitors', True)
        min_competitors = actor_input.get('min_competitors', 5)
        tweets_per_competitor = actor_input.get('tweets_per_competitor', 20)
        
        logger.info(f"Starting Twitter competitor analysis")
        logger.info(f"User: @{user_username}, Manual competitors: {len(competitor_usernames)}")
        logger.info(f"Parsed values - User: '{user_username}', Competitors: {competitor_usernames}, Auto-discover: {auto_discover}")
        
        analyzer = TwitterCompetitorAnalyzer()
        
        # Build final competitor list
        final_competitors = list(competitor_usernames)  # Start with manual list
        
        # Auto-discover competitors if needed
        if auto_discover and user_username and len(final_competitors) < min_competitors:
            logger.info(f"Auto-discovering competitors for @{user_username}")
            discovered = await analyzer.discover_competitors(user_username, min_competitors - len(final_competitors))
            final_competitors.extend(discovered)
        
        # Remove duplicates and limit
        final_competitors = list(set(final_competitors))[:15]  # Max 15 competitors
        
        if len(final_competitors) < 3:
            error_msg = "Need at least 3 competitors to analyze. Please provide more competitor usernames or ensure your username is valid for auto-discovery."
            logger.error(error_msg)
            await Actor.fail()
            return
        
        logger.info(f"Analyzing {len(final_competitors)} competitors: {final_competitors}")
        
        # Analyze each competitor's tweets
        competitor_tweets_data = {}
        
        for i, username in enumerate(final_competitors):
            logger.info(f"Analyzing tweets from @{username}")
            
            # Add delay between requests to avoid rate limiting (except for first request)
            if i > 0:
                delay = 5 + (i * 2)  # Progressive delay: 5s, 7s, 9s, etc.
                logger.info(f"Waiting {delay} seconds before next request...")
                await asyncio.sleep(delay)
            
            tweets = await analyzer.get_top_performing_tweets(username, tweets_per_competitor)
            
            if tweets:
                competitor_tweets_data[username] = tweets
                avg_engagement = sum(t['engagement_score'] for t in tweets) / len(tweets)
                await Actor.push_data({
                    "type": "competitor_tweets",
                    "competitor": username,
                    "tweets_count": len(tweets),
                    "avg_engagement_score": avg_engagement,
                    "top_tweet": tweets[0] if tweets else None
                })
            else:
                logger.warning(f"No tweets found for @{username}")
        
        if not competitor_tweets_data:
            logger.error("No tweet data could be extracted from any competitors")
            await Actor.fail()
            return
        
        # Analyze patterns across all competitor tweets
        logger.info("Analyzing patterns across all competitor tweets")
        patterns_analysis = await analyzer.analyze_tweet_patterns(competitor_tweets_data)
        
        # Generate content ideas based on analysis
        logger.info("Generating topic and hook ideas based on analysis")
        content_ideas = await analyzer.generate_content_ideas(patterns_analysis, competitor_tweets_data)
        
        # Output final results
        final_results = {
            "analysis_summary": {
                "competitors_analyzed": len(competitor_tweets_data),
                "total_tweets_analyzed": sum(len(tweets) for tweets in competitor_tweets_data.values()),
                "analysis_date": datetime.now().isoformat(),
                "platform": "twitter"
            },
            "competitor_data": {
                username: {
                    "tweets_count": len(tweets),
                    "avg_engagement_score": sum(t['engagement_score'] for t in tweets) / len(tweets) if tweets else 0,
                    "top_performing_tweets": tweets[:5]  # Top 5 for summary
                }
                for username, tweets in competitor_tweets_data.items()
            },
            "patterns_analysis": patterns_analysis,
            "content_ideas": content_ideas
        }
        
        await Actor.push_data(final_results)
        logger.info("Twitter competitor analysis and content idea generation completed!")


if __name__ == "__main__":
    asyncio.run(main())