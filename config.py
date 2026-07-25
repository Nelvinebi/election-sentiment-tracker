"""
Central configuration. All settings loaded from environment variables.
Never hardcode secrets — use .env file locally, GitHub Secrets in CI.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# X API Credentials
X_API_KEY = os.getenv('X_API_KEY')
X_API_SECRET = os.getenv('X_API_SECRET')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_SECRET = os.getenv('X_ACCESS_SECRET')
X_BEARER_TOKEN = os.getenv('X_BEARER_TOKEN')

# Candidate search queries
CANDIDATES = {
    'Tinubu': ['Tinubu', 'APC', 'Bola Tinubu', 'BAT2026'],
    'Obi': ['Peter Obi', 'Obi', 'NDC', 'ObiDatti', 'Labour Party'],
    'Atiku': ['Atiku', 'ADC', 'Atiku Abubakar', 'Atiku2026']
}

# Paths
DB_PATH = os.getenv('DB_PATH', 'data/election_data.db')
CHARTS_DIR = os.getenv('CHARTS_DIR', 'outputs/charts')
REPORTS_DIR = os.getenv('REPORTS_DIR', 'outputs/reports')

# Analysis settings
DAYS_FOR_WEEKLY = 7
SENTIMENT_MODEL = 'cardiffnlp/twitter-roberta-base-sentiment'  # NLP model

# Ensure directories exist
os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)