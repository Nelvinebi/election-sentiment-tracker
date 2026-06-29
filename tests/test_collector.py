"""
Unit tests for data collection.
"""

import pytest
from unittest.mock import Mock, patch
from src.collector import collect_candidate_data


def test_collect_candidate_data_no_tweets():
    """Test when API returns no tweets."""
    mock_client = Mock()
    mock_client.search_recent_tweets.return_value = Mock(data=None)
    
    result = collect_candidate_data(mock_client, 'Tinubu', ['Tinubu'])
    
    assert result['mentions'] == 0
    assert result['sentiment'] == 0.5


def test_collect_candidate_data_with_tweets():
    """Test successful collection with tweets."""
    mock_tweet = Mock()
    mock_tweet.text = "Tinubu is doing great work"
    mock_tweet.public_metrics = {'like_count': 50, 'retweet_count': 20, 'reply_count': 10}
    
    mock_client = Mock()
    mock_client.search_recent_tweets.return_value = Mock(data=[mock_tweet])
    
    with patch('src.collector.get_analyzer') as mock_analyzer:
        mock_analyzer.return_value.analyze_tweets.return_value = {
            'positive': 0.8, 'negative': 0.1, 'neutral': 0.1, 'compound': 0.7
        }
        
        result = collect_candidate_data(mock_client, 'Tinubu', ['Tinubu'])
        
        assert result['mentions'] == 1
        assert result['sentiment'] == 0.7
        assert result['positive'] == 0.8