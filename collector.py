"""
X API data collection. Fetches tweets and sends text to NLP analyzer.
"""

import tweepy
from datetime import datetime
from src.config import X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET, CANDIDATES
from src.sentiment import get_analyzer


def get_x_client():
    """Initialize and return authenticated X API client."""
    return tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_SECRET,
        wait_on_rate_limit=True
    )


def collect_candidate_data(client, candidate_name: str, keywords: list) -> dict:
    """
    Fetch tweets for a candidate, analyze sentiment via NLP, return metrics.
    
    Returns: {
        'mentions': int,
        'sentiment': float,      # compound score (-1 to 1)
        'positive': float,       # % positive
        'negative': float,       # % negative
        'neutral': float         # % neutral
    }
    """
    query = ' OR '.join(keywords)
    
    try:
        tweets = client.search_recent_tweets(
            query=query,
            max_results=100,
            tweet_fields=['created_at', 'public_metrics', 'lang']
        )
        
        if not tweets.data:
            return {
                'mentions': 0,
                'sentiment': 0.5,
                'positive': 0,
                'negative': 0,
                'neutral': 0
            }
        
        mentions = len(tweets.data)
        
        # ============================================
        # NLP SENTIMENT ANALYSIS (The Key Integration)
        # ============================================
        # Extract tweet texts
        tweet_texts = [tweet.text for tweet in tweets.data]
        
        # Send texts to NLP analyzer
        analyzer = get_analyzer()
        nlp_result = analyzer.analyze_tweets(tweet_texts)
        
        # NLP returns: {
        #     'positive': 0.45, 
        #     'negative': 0.30, 
        #     'neutral': 0.25, 
        #     'compound': 0.15    # positive - negative
        # }
        
        return {
            'mentions': mentions,
            'sentiment': round(nlp_result['compound'], 4),
            'positive': round(nlp_result['positive'], 4),
            'negative': round(nlp_result['negative'], 4),
            'neutral': round(nlp_result['neutral'], 4)
        }
        
    except tweepy.TooManyRequests:
        print(f"⚠️ Rate limit hit for {candidate_name}")
        return None
    except Exception as e:
        print(f"❌ Error collecting {candidate_name}: {e}")
        return None


def collect_all_data() -> dict:
    """
    Collect data for all candidates.
    Returns a dict ready for database insertion.
    """
    client = get_x_client()
    today = datetime.now().strftime('%Y-%m-%d')
    
    data = {'date': today}
    
    for candidate, keywords in CANDIDATES.items():
        print(f"🔍 Collecting + analyzing NLP sentiment for {candidate}...")
        result = collect_candidate_data(client, candidate, keywords)
        
        if result:
            data[f'{candidate}_mentions'] = result['mentions']
            data[f'{candidate}_sentiment'] = result['sentiment']
            data[f'{candidate}_positive'] = result['positive']
            data[f'{candidate}_negative'] = result['negative']
            data[f'{candidate}_neutral'] = result['neutral']
        else:
            # Fallback: use neutral scores if collection fails
            data[f'{candidate}_mentions'] = 0
            data[f'{candidate}_sentiment'] = 0.0
            data[f'{candidate}_positive'] = 0.33
            data[f'{candidate}_negative'] = 0.33
            data[f'{candidate}_neutral'] = 0.34
    
    print(f"✅ Data collected for {today}")
    return data