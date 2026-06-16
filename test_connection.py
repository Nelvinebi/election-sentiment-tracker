"""
Quick test to verify X API connection works.
Run this before the full tracker.
"""

import os
from dotenv import load_dotenv
import tweepy

# Load environment variables
load_dotenv()

# Get credentials
api_key = os.getenv('X_API_KEY')
api_secret = os.getenv('X_API_SECRET')
access_token = os.getenv('X_ACCESS_TOKEN')
access_secret = os.getenv('X_ACCESS_SECRET')
bearer_token = os.getenv('X_BEARER_TOKEN')

print("=" * 50)
print("X API CONNECTION TEST")
print("=" * 50)

# Check if credentials exist
if not all([api_key, api_secret, access_token, access_secret]):
    print("FAILED: One or more credentials are missing from .env")
    print("Make sure all four variables are set.")
    exit(1)

print("All credentials found in .env")

# Try to connect
try:
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret,
        wait_on_rate_limit=True
    )
    
    # Test: Get your own account info
    me = client.get_me()
    print(f"Connected successfully!")
    print(f"   Account: @{me.data.username}")
    print(f"   Name: {me.data.name}")
    print(f"   ID: {me.data.id}")
    
except tweepy.Unauthorized:
    print("FAILED: Invalid credentials")
    print("   Double-check your API keys and tokens")
    exit(1)
    
except Exception as e:
    print(f"FAILED: {e}")
    exit(1)

# Test search with Bearer Token
print("\nTesting tweet search for 'Tinubu'...")

if not bearer_token:
    print("FAILED: X_BEARER_TOKEN not found in .env")
    print("   Add X_BEARER_TOKEN=your_token to your .env file")
    exit(1)

search_client = tweepy.Client(bearer_token=bearer_token)

try:
    tweets = search_client.search_recent_tweets(
        query="Tinubu",
        max_results=10,
        tweet_fields=['created_at', 'public_metrics']
    )
    
    if tweets.data:
        print(f"Search works! Found {len(tweets.data)} tweets")
        print(f"   Latest tweet: {tweets.data[0].text[:80]}...")
    else:
        print("Search returned no tweets (but API connection works)")
    
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED")
    print("=" * 50)
    
except tweepy.Unauthorized:
    print("FAILED: Invalid Bearer Token")
    print("   Regenerate it in X Developer Portal")
    
except tweepy.Forbidden:
    print("FAILED: Your API tier doesn't allow search")
    print("   You need Basic tier ($200/mo) or higher")
    print("   Free tier has NO search access since 2023")
    
except Exception as e:
    print(f"FAILED: {e}")