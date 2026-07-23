"""
Auto-publishing to X platform.
Posts the chart image + write-up text.
"""

import tweepy
from src.config import (X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, 
                        X_ACCESS_SECRET, CHARTS_DIR)


def get_writeup(daily, weekly, overall):
    text = (
        f"Election Tracker - {daily['date']}\n\n"
        f"Tinubu: {daily['Tinubu']['mentions']} mentions "
        f"(7d avg sentiment: {weekly['Tinubu']['avg_sentiment']*100:.0f}%) "
        f"trend: {weekly['Tinubu']['trend']}\n"
        f"Obi: {daily['Obi']['mentions']} mentions "
        f"(7d avg sentiment: {weekly['Obi']['avg_sentiment']*100:.0f}%) "
        f"trend: {weekly['Obi']['trend']}\n"
        f"Atiku: {daily['Atiku']['mentions']} mentions "
        f"(7d avg sentiment: {weekly['Atiku']['avg_sentiment']*100:.0f}%) "
        f"trend: {weekly['Atiku']['trend']}\n\n"
        f"Overall leader: Obi ({overall['Obi']['total_mentions']:,} total mentions)\n"
        f"#NigeriaDecides2026 #ElectionTracker"
    )
    return text


def publish_to_x(chart_path: str, text: str) -> str:
    """
    Upload chart and post tweet.
    Returns: tweet URL
    """
    # v1.1 API for media upload
    auth = tweepy.OAuth1UserHandler(X_API_KEY, X_API_SECRET, 
                                    X_ACCESS_TOKEN, X_ACCESS_SECRET)
    api = tweepy.API(auth)
    
    # v2 API for posting
    client = tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_SECRET
    )
    
    # Upload image
    media = api.media_upload(chart_path)
    
    # Post tweet with media
    tweet = client.create_tweet(text=text, media_ids=[media.media_id])
    
    tweet_id = tweet.data['id']
    tweet_url = f"https://x.com/user/status/{tweet_id}"
    
    print(f"✅ Published: {tweet_url}")
    return tweet_url