"""
Unit tests for the analyzer module.
"""

import pytest
import pandas as pd
from src.analyzer import compute_daily, compute_weekly, compute_overall


def test_compute_daily():
    df = pd.DataFrame({
        'date': ['2026-05-27', '2026-05-28'],
        'Tinubu_mentions': [1000, 1200],
        'Tinubu_sentiment': [0.4, 0.5],
        'Obi_mentions': [1500, 1600],
        'Obi_sentiment': [0.6, 0.7],
        'Atiku_mentions': [800, 900],
        'Atiku_sentiment': [0.3, 0.4]
    })
    
    result = compute_daily(df)
    assert result['date'] == '2026-05-28'
    assert result['Tinubu']['mentions'] == 1200
    assert result['Obi']['sentiment'] == 0.7


def test_compute_weekly_trend():
    df = pd.DataFrame({
        'date': [f'2026-05-{22+i}' for i in range(7)],
        'Tinubu_mentions': [1000, 1100, 1200, 1300, 1400, 1500, 1600],
        'Tinubu_sentiment': [0.4] * 7,
        'Obi_mentions': [1000] * 7,
        'Obi_sentiment': [0.6] * 7,
        'Atiku_mentions': [1000] * 7,
        'Atiku_sentiment': [0.3] * 7
    })
    
    result = compute_weekly(df)
    assert result['Tinubu']['trend'] == '↑'  # 1600 > 1000
    assert result['Obi']['trend'] == '→'     # Flat (you may want to handle this)
