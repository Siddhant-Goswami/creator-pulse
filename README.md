# Instagram Competitor Reel Analyzer

An Apify actor that analyzes Instagram competitors' top-performing reels to extract insights about hooks, topics, delivery styles, and generates personalized content ideas using AI.

## Features

- 🔍 **Auto-Competitor Discovery**: Automatically finds competitors based on your Instagram username and niche
- 📱 **Instagram Reel Analysis**: Analyzes top-performing reels from competitor accounts
- 🎯 **Hook Pattern Analysis**: Identifies successful hook formulas and opening strategies
- 📊 **Content Performance Insights**: Extracts patterns about optimal timing, duration, and hashtags
- 💡 **AI-Powered Content Ideas**: Generates topic and hook ideas based on competitive analysis
- 🚀 **Scalable**: Built on Apify platform for reliable, scalable execution

## Setup

### 1. Environment Variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Required environment variables:
- `APIFY_TOKEN`: Your Apify API token (get from [Apify Console](https://console.apify.com/account/integrations))
- `OPENROUTER_API_KEY`: Your OpenRouter API key (get from [OpenRouter](https://openrouter.ai/keys))

### 2. Dependencies

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Input Format

The actor supports flexible input options:

```json
{
  "user_username": "your_instagram_username",
  "competitor_usernames": ["competitor1", "competitor2"],
  "auto_discover_competitors": true,
  "min_competitors": 5,
  "reels_per_competitor": 20
}
```

**Input Parameters:**
- `user_username` (optional): Your Instagram username for auto-discovery
- `competitor_usernames` (optional): Manual list of competitor usernames  
- `auto_discover_competitors` (default: true): Auto-find competitors
- `min_competitors` (default: 5): Minimum competitors to analyze
- `reels_per_competitor` (default: 20): Number of top reels per competitor

### Running Locally

```bash
# Set environment variables
export OPENROUTER_API_KEY="your_key_here"
export APIFY_TOKEN="your_token_here"

# Run the integration test
python test_integration.py

# Or run the main script directly with input
python main.py
```

### Output

The actor provides comprehensive analysis results:

```json
{
  "analysis_summary": {
    "competitors_analyzed": 5,
    "total_reels_analyzed": 100,
    "analysis_date": "2024-01-15T10:30:00"
  },
  "competitor_data": {
    "competitor1": {
      "reels_count": 20,
      "avg_engagement_rate": 4.5,
      "top_performing_reels": [...]
    }
  },
  "patterns_analysis": {
    "avg_engagement_rate": 3.8,
    "top_hashtags": [...],
    "hook_patterns": {
      "top_performing_hooks": [...],
      "common_hook_starters": [...]
    },
    "optimal_duration": {...},
    "posting_patterns": {...},
    "topic_themes": [...]
  },
  "content_ideas": {
    "topic_ideas": [...],
    "hook_ideas": [...],
    "strategy_insights": [...]
  }
}
```

## Key Analysis Features

### 🎯 Hook Pattern Analysis
- Extracts successful hook formulas from top-performing reels
- Identifies common opening phrases and structures
- Correlates hook types with engagement rates

### 📊 Performance Insights
- **Optimal Duration**: Analyzes which video lengths perform best
- **Posting Patterns**: Identifies best days/times for posting
- **Hashtag Analysis**: Finds most effective hashtags in your niche
- **Topic Themes**: Extracts trending topics and themes

### 💡 AI-Generated Content Ideas
- **Topic Ideas**: Fresh content topics based on successful patterns
- **Hook Ideas**: Compelling opening hooks tailored to your niche
- **Strategy Insights**: Data-driven recommendations for content strategy

## Testing

Run the integration test with real Instagram data:

```bash
python test_integration.py
```

This will:
1. Analyze 3 popular Instagram accounts (Gary Vee, MrBeast, HubSpot)
2. Extract reel performance data and patterns
3. Generate content ideas based on analysis
4. Save comprehensive results to `instagram_test_results.json`

## Deployment

Deploy to Apify platform:

```bash
# Install Apify CLI
npm install -g apify-cli

# Login to Apify
apify login

# Deploy the actor
apify push
```

## Configuration

The actor can be configured through `apify.json`:
- Memory allocation (default: 2048MB)
- Timeout (default: 2 hours)
- Environment variables

## Use Cases

- **Content Creators**: Discover what's working in your niche
- **Marketing Agencies**: Analyze clients' competitors for strategy insights
- **Brand Managers**: Understand competitor content strategies
- **Growth Hackers**: Find content gaps and opportunities

## Limitations & Considerations

- Analyzes public Instagram accounts only
- Rate limited by Instagram's API constraints
- Requires valid OPENROUTER_API_KEY for AI content generation
- Analysis covers last 90 days of content
- Maximum 15 competitors per run to manage processing time

## Ethical Usage

- Only analyzes publicly available content
- Respects Instagram's terms of service
- Does not download or store media files
- Provides insights for competitive analysis, not content copying

## Support

For issues or feature requests, please check the Apify Console logs or contact support through the Apify platform.