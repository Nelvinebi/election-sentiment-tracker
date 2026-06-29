"""
Unit tests for NLP sentiment analysis.
"""

import pytest
from src.sentiment import SentimentAnalyzer


def test_analyze_text_proxy_mode():
    """Test when NLP is disabled (proxy mode)."""
    analyzer = SentimentAnalyzer()
    analyzer.classifier = None  # Force proxy mode
    
    result = analyzer.analyze_text("This is a test tweet")
    
    assert result['positive'] == 0.33
    assert result['negative'] == 0.33
    assert result['neutral'] == 0.34


def test_analyze_tweets_empty():
    """Test with empty tweet list."""
    analyzer = SentimentAnalyzer()
    analyzer.classifier = None
    
    result = analyzer.analyze_tweets([])
    
    assert result['positive'] == 0
    assert result['negative'] == 0
    assert result['neutral'] == 0
    assert result['compound'] == 0.5