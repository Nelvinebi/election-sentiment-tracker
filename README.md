# 🇳🇬 Nigeria 2026 Election Sentiment Tracker

> Automated daily statistical analysis of presidential candidates on X (Twitter). Tracks mention volume, sentiment trends, and publishes visual reports.

![Dashboard](outputs/charts/dashboard_sample.png)

## 📊 What It Does

Every day at 8:00 AM UTC, this system automatically:

1. **Collects** mentions of Tinubu (APC), Peter Obi (NDC), and Atiku (ADC) from X
2. **Analyzes** daily stats, 7-day rolling averages, and overall trends
3. **Generates** a 4-panel chart dashboard
4. **Publishes** results to X with auto-generated write-up

## 🏗️ Architecture
┌─────────┐    ┌──────────┐    ┌─────────┐    ┌─────────┐
│  X API  │───▶│ Collector│───▶│ SQLite  │───▶│Analyzer │
└─────────┘    └──────────┘    └─────────┘    └────┬────┘
│
┌─────────────────────┘
▼
┌──────────┐    ┌─────────┐
│Visualizer│───▶│Publisher│───▶ X
└──────────┘    └─────────┘
plain
Copy

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/election-sentiment-tracker.git
cd election-sentiment-tracker
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
2. Configure Environment
bash
Copy
cp .env.example .env
# Edit .env with your X API credentials
3. Initialize Database
bash
Copy
python scripts/setup_db.py
4. Run Locally
bash
Copy
python scripts/local_run.py
🔧 Configuration
All settings are in src/config.py and overridden by environment variables:
Table
Variable	Description
X_API_KEY	X API Key
X_API_SECRET	X API Secret
X_ACCESS_TOKEN	X Access Token
X_ACCESS_SECRET	X Access Secret
DB_PATH	SQLite database location
SENTIMENT_MODEL	HuggingFace model name
🧠 NLP Upgrade
The default uses a proxy sentiment score. To enable real NLP:
Uncomment the transformer code in src/sentiment.py
Install NLP dependencies: pip install transformers torch
Update collector.py to pass tweet texts to the analyzer
Model used: cardiffnlp/twitter-roberta-base-sentiment (trained on Twitter data)
☁️ Google Cloud Deployment
See DEPLOYMENT.md for Google Cloud Functions setup.
💰 X API Costs
Table
Tier	Price	Reads/Month	Best For
Basic	$200	10,000	✅ This project
Pro	$5,000	1,000,000	High volume
📁 Project Structure
plain
Copy
├── src/           # Core modules
├── scripts/       # Runnable scripts
├── tests/         # Unit tests
├── .github/       # GitHub Actions CI
├── data/          # SQLite database
└── outputs/       # Charts & reports
🤝 Contributing
Fork the repository
Create a feature branch: git checkout -b feature-name
Commit changes: git commit -am 'Add feature'
Push: git push origin feature-name
Submit a Pull Request
📜 License
MIT License — see LICENSE
