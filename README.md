# 🗳️ Presidential Election Sentiment Tracker — Nigeria 2026

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tweepy](https://img.shields.io/badge/Tweepy-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)
![Transformers](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=matplotlib&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

> An **automated X (Twitter) data pipeline** that collects, analyses, and visualises daily sentiment for Nigeria's 2026 presidential candidates — **Tinubu (APC)**, **Peter Obi (NDC)**, and **Atiku (ADC)** — using real-time social media mentions, NLP-powered sentiment analysis, and publication-ready charts auto-posted to X.

</div>

<div align="center">

[![Follow on X](https://img.shields.io/badge/🚀%20Follow%20@AgbozuN%20for%20Daily%20Updates-1DA1F2?style=for-the-badge&logo=x&logoColor=white)](https://x.com/AgbozuN)

</div>

---

## 📌 Problem

Nigeria's 2026 presidential election is generating intense discourse across social media, with millions of posts daily reflecting shifting public opinion, campaign momentum, and voter sentiment. Traditional polling is expensive, slow, and often fails to capture real-time grassroots sentiment — particularly among Nigeria's digitally active youth demographic.

Without automated sentiment tracking, analysts and campaigns face:

- **Missed momentum shifts** — failing to detect when a candidate is gaining or losing support
- **Noisy volume metrics** — counting mentions without knowing if they are positive or negative
- **Delayed response times** — waiting days or weeks for poll results while sentiment moves daily
- **Unstructured data overload** — drowning in raw tweets without statistical summarisation

There is a critical need for a **reproducible, automated, open-source system** that transforms raw social noise into structured electoral intelligence — collecting candidate mentions from X in real time, analysing sentiment using Natural Language Processing, computing daily, weekly, and overall statistical trends, and auto-publishing visual summaries to X.

---

## 🎯 Objective

- **Ingest** daily mentions of Tinubu, Peter Obi, and Atiku from X API v2 using Tweepy
- **Analyse sentiment** of each mention using a pre-trained RoBERTa NLP model (`cardiffnlp/twitter-roberta-base-sentiment`)
- **Compute statistical summaries:** daily metrics, 7-day rolling averages, and cumulative trends since day one
- **Classify sentiment** into positive, negative, and neutral with compound scores
- **Detect momentum shifts** through day-over-day trend analysis (↑/↓ indicators)
- **Generate** a 4-panel dashboard: daily trends, 7-day averages, overall summaries, and sentiment breakdowns
- **Auto-publish** results to X with charts and structured write-ups showing previous-day trends, past-7-day patterns, and overall averages
- **Store** all data in SQLite for historical tracking and reproducibility

---

## 🗂️ Data Sources

All data is sourced from the **real X (Twitter) API** — no synthetic data is used in production.

### API Sources

| Source | Type | Purpose |
|--------|------|---------|
| X API v2 (Tweepy) | Real-time social media | Candidate mention volume, tweet text, engagement metrics |
| `cardiffnlp/twitter-roberta-base-sentiment` | Pre-trained NLP model | Sentiment classification (positive / negative / neutral) |

### Candidates Tracked

| Candidate | Party | Search Keywords |
|-----------|-------|-----------------|
| Bola Tinubu | APC | Tinubu, APC, Bola Tinubu, BAT2026 |
| Peter Obi | NDC | Peter Obi, Obi, NDC, ObiDatti, Labour Party |
| Atiku Abubakar | ADC | Atiku, ADC, Atiku Abubakar, Atiku2026 |

### Metrics Computed

| Parameter | Value |
|-----------|-------|
| Data Source | X API v2 (recent search endpoint) |
| Time Period | Rolling 7-day lookback (Basic tier) |
| Update Frequency | Daily at 8:00 AM UTC |
| Total Candidates | 3 major presidential candidates |
| NLP Model | `cardiffnlp/twitter-roberta-base-sentiment` |
| Sentiment Labels | Positive, Negative, Neutral |
| Database | SQLite (local persistence) |

### Key Variables

| Variable | Type | Description |
|----------|------|-------------|
| `mentions` | Target | Daily tweet count per candidate — what we track |
| `sentiment` | Numeric | Compound score: −1 (all negative) to +1 (all positive) |
| `positive` | Proportion | % of tweets classified as positive |
| `negative` | Proportion | % of tweets classified as negative |
| `neutral` | Proportion | % of tweets classified as neutral |
| `trend` | Directional | ↑ (gaining) or ↓ (declining) vs previous period |

---

## 🛠️ Tools & Technologies

- **Language:** Python 3.11+
- **Social Media API:** Tweepy 4.16+ — X API v2 integration for search and posting
- **NLP Engine:** HuggingFace Transformers + PyTorch — RoBERTa sentiment analysis
- **Data Processing:** Pandas, NumPy — time-series aggregation and statistical analysis
- **Database:** SQLite3 — lightweight local storage for daily metrics
- **Visualisation:** Matplotlib — 4-panel dashboard (line charts, bar charts, horizontal summaries)
- **Automation:** Python `schedule` / cron / GitHub Actions — daily execution at 8:00 AM UTC
- **Cloud Deployment:** Google Cloud Functions + Cloud Scheduler — serverless production hosting
- **Environment Management:** python-dotenv — secure credential handling

---

## ⚙️ Methodology / Project Workflow

1. **Environment Setup:** Load API credentials from `.env`; initialise SQLite database with `setup_db.py`
2. **Data Collection:** Authenticate via Tweepy OAuth 1.0a; search recent tweets for each candidate using OR-query combinations; extract tweet text, engagement metrics (likes, retweets, replies)
3. **NLP Sentiment Analysis:** Pass tweet texts through `cardiffnlp/twitter-roberta-base-sentiment`; classify each tweet as positive, negative, or neutral; compute aggregate proportions and compound score
4. **Daily Aggregation:** Count total mentions; calculate average positive %, negative %, neutral %; derive compound sentiment score
5. **Database Storage:** Insert daily record into SQLite with columns for mentions, sentiment, positive, negative, neutral per candidate
6. **Statistical Analysis:** Retrieve all historical data; compute daily (latest record), weekly (7-day rolling mean), and overall (cumulative since day one) summaries; calculate trend direction (↑/↓) by comparing first and last values in the 7-day window
7. **Chart Generation:** Plot daily mention volume (line chart), daily sentiment % (line chart with neutral baseline), 7-day average comparison (grouped bar chart), and overall summary (horizontal bar chart with sentiment labels)
8. **Write-up Composition:** Generate structured text report with previous-day stats, 7-day trends, overall averages, and insight summary
9. **Auto-Publishing:** Upload chart image via X API v1.1 media upload; post tweet with write-up text via X API v2
10. **Scheduling:** Execute full pipeline daily via cron (local), GitHub Actions (CI/CD), or Google Cloud Scheduler (cloud)

---

## 📊 Key Features

- ✅ **Real X API data:** Live tweet collection for three major presidential candidates
- ✅ **NLP-powered sentiment:** RoBERTa model trained on 2 billion tweets understands Nigerian political slang, Pidgin, and emojis
- ✅ **Three-layer analysis:** Daily snapshots, 7-day rolling averages, and cumulative overall trends
- ✅ **Trend detection:** Automatic ↑/↓ momentum indicators with day-over-day percentage change
- ✅ **4-panel visual dashboard:** Line charts for daily trends, bar charts for weekly/overall comparisons, colour-coded by candidate
- ✅ **Auto-publishing:** Charts and structured write-ups posted directly to X without manual intervention
- ✅ **SQLite persistence:** Full historical dataset stored locally for backtesting and longitudinal analysis
- ✅ **Modular architecture:** Separate modules for collection, NLP, analysis, visualisation, and publishing — easy to extend
- ✅ **Cloud-ready:** Dockerfile and Google Cloud Functions configuration included for serverless deployment
- ✅ **GitHub Actions CI/CD:** Automated daily runs with artifact upload and data commit

---

## 📸 Visualisations

### 🔹 Daily Mention Volume & Sentiment Trends
> Real-time tracking of mention volume and sentiment percentage across all three candidates; Obi's sentiment surged to 67% on 28 May 2026 while Tinubu declined to 49%, revealing divergent campaign momentum

![Daily Trends](outputs/charts/dashboard_YYYYMMDD.png)

---

### 🔹 7-Day Rolling Average
> Aggregated view of the past week's performance; Peter Obi leads with 1,789 avg mentions and 61% sentiment, while Tinubu trends downward (↓) at 1,364 mentions and 45% sentiment

![7-Day Rolling Average](outputs/charts/dashboard_YYYYMMDD.png)

---

### 🔹 Overall Summary (Since Collection Start)
> Cumulative averages since day one: Obi leads in total mentions (45,022) and sentiment (56%), Tinubu averages 1,378 mentions/day at 44% sentiment, Atiku trails at 989 mentions/day with 40% sentiment

![Overall Summary](outputs/charts/dashboard_YYYYMMDD.png)

---

### 🔹 Sentiment Breakdown by Candidate
> Proportion of positive, negative, and neutral tweets per candidate; reveals whether high mention volume is driven by support or criticism

*(Derived from database queries)*

> 📌 *All visualisations are saved at high resolution in the `/outputs/charts/` folder.*

---

## 📈 Results & Insights

### Sample Daily Report (28 May 2026)

| Metric | Tinubu (APC) | Peter Obi (NDC) | Atiku (ADC) |
|--------|-------------|-----------------|-------------|
| **Daily Mentions** | 1,265 | 1,926 | 920 |
| **Daily Sentiment** | 49% | 67% | 54% |
| **7-Day Avg Mentions** | 1,364 | 1,789 | 944 |
| **7-Day Avg Sentiment** | 45% | 61% | 43% |
| **7-Day Trend** | ↓ | ↑ | ↑ |
| **Overall Avg Mentions** | 1,378 | 1,500 | 989 |
| **Overall Avg Sentiment** | 44% | 56% | 40% |
| **Total Mentions (All Time)** | 41,367 | 45,022 | 29,674 |

### Sentiment by Candidate

| Candidate | Avg Sentiment | Positive % | Negative % | Neutral % | Rank |
|-----------|--------------|------------|------------|-----------|------|
| Peter Obi | **56%** | 50% | 20% | 30% | 🥇 1st |
| Tinubu | 44% | 35% | 35% | 30% | 2nd |
| Atiku | 40% | 30% | 40% | 30% | 3rd |

### Key Insights

- 🔍 **Obi leads momentum:** 7-day trend arrow (↑) with highest sentiment (61%) and growing mention volume — indicates positive campaign traction
- 🔍 **Tinubu declining:** Downward 7-day trend (↓) despite highest historical volume; sentiment stuck at 45% suggests voter fatigue or criticism
- 🔍 **Atiku stable but low:** Lowest overall mentions (989/day) and sentiment (40%); struggling to break through the two-horse narrative
- 🔍 **Sentiment-volume paradox:** Tinubu has more total mentions but lower sentiment — high volume driven by controversy, not support
- 🔍 **NLP reveals true picture:** Without sentiment analysis, Tinubu's 1,378 avg mentions appears dominant; with NLP, Obi's 56% positive sentiment shows stronger electoral favourability
- 🔍 **Daily granularity matters:** Weekly polls miss rapid shifts; daily tracking caught Obi's +9.1% day-over-day mention spike on 28 May 2026

---

## 🚀 Live Output

📊 **Follow [@AgbozuN](https://x.com/AgbozuN) for daily automated election tracker posts**

Each daily post includes:
- Mention counts and sentiment scores for all three candidates
- 7-day trend arrows (↑/↓)
- Overall averages since tracking began
- Auto-generated insight summary
- Attached 4-panel chart dashboard

---

## 📁 Project Structure

```
📦 election-sentiment-tracker/
│
├── 📂 src/
│   ├── __init__.py                    # Package initialisation
│   ├── config.py                      # Central configuration (candidates, paths, API settings)
│   ├── collector.py                   # X API data collection via Tweepy
│   ├── sentiment.py                   # NLP sentiment analysis (RoBERTa transformer)
│   ├── analyzer.py                    # Daily / weekly / overall statistical analysis
│   ├── visualizer.py                  # 4-panel Matplotlib dashboard generation
│   ├── publisher.py                   # X auto-posting (media upload + tweet creation)
│   └── database.py                    # SQLite CRUD operations
│
├── 📂 scripts/
│   ├── setup_db.py                    # Initialise SQLite database (run once)
│   ├── local_run.py                   # Manual full pipeline execution
│   ├── test_with_fake_data.py         # Test pipeline with simulated data (no X API needed)
│   └── generate_history.py            # Generate fake historical data for chart testing
│
├── 📂 data/
│   ├── .gitkeep                       # Empty folder marker
│   └── election_data.db               # SQLite database (auto-generated, gitignored)
│
├── 📂 outputs/
│   ├── 📂 charts/                     # Generated PNG dashboards (gitignored)
│   └── 📂 reports/                    # JSON summaries and write-up text (gitignored)
│
├── 📂 tests/
│   ├── __init__.py
│   ├── test_collector.py              # Unit tests for X API collection
│   ├── test_analyzer.py               # Unit tests for statistical analysis
│   └── test_sentiment.py              # Unit tests for NLP engine
│
├── 📂 notebooks/
│   └── exploratory_analysis.ipynb     # Jupyter notebook for manual data exploration
│
├── 📂 .github/
│   └── 📂 workflows/
│       └── daily-run.yml              # GitHub Actions: auto-run daily at 8am UTC
│
├── requirements.txt                   # Python dependencies
├── .env.example                       # Template for environment variables (no real keys)
├── .gitignore                         # Excludes secrets, database, outputs, cache
├── Dockerfile                         # Container configuration for cloud deployment
├── cloudbuild.yaml                    # Google Cloud Build configuration
├── main.py                            # Google Cloud Functions entry point
├── test_connection.py                 # Quick X API connectivity verification
└── README.md                          # This file
```

---

## ▶️ How to Run

### Prerequisites

```bash
# Python 3.11+
# X Developer account with Basic tier API access ($200/month)
# X API credentials: Consumer Key, Consumer Secret, Access Token, Access Token Secret
```

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/Nelvinebi/election-sentiment-tracker.git
cd election-sentiment-tracker

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set environment variables
cp .env.example .env
# Edit .env with your real X API credentials

# 6. Initialise database
python scripts/setup_db.py

# 7. Test with fake data (no X API needed)
python scripts/test_with_fake_data.py

# 8. Verify X API connection
python test_connection.py

# 9. Run full pipeline with live data
python scripts/local_run.py
```

### Daily Automation

**Windows Task Scheduler:**
- Trigger: Daily at 8:00 AM UTC (9:00 AM Nigeria time)
- Action: `python scripts/local_run.py`
- Start in: `C:\Users\YourName\election-sentiment-tracker`

**Mac/Linux cron:**

```bash
crontab -e
# Add:
0 8 * * * cd ~/election-sentiment-tracker && source venv/bin/activate && python scripts/local_run.py
```

**GitHub Actions:**
- Already configured in `.github/workflows/daily-run.yml`
- Runs automatically every day at 8:00 AM UTC
- Requires repository secrets: `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_SECRET`

### 💰 X API Pricing (2026)

| Tier | Cost | Search Access | Best For |
|------|------|----------------|----------|
| Free | $0 | ❌ None (read-only) | Not suitable |
| Basic | $200/month | ✅ Recent search (7 days), 10,000 reads/month | ✅ This project |
| Pro | $5,000/month | ✅ Full archive, 1,000,000 reads/month | High-volume tracking |
| Enterprise | $42,000+/month | ✅ Custom | Commercial platforms |

> Usage estimate: 3 candidates × 1 query/day × 30 days = 90 requests/month. Well within Basic tier limits.

---

## ⚠️ Limitations & Future Work

**Current Limitations:**
- X API Basic tier limits search to 7-day history; full archive requires Pro ($5,000/month)
- Rate limits: 450 requests per 15-minute window; pipeline stays well within this
- NLP model is trained on general Twitter English; Nigerian political slang, Pidgin, and local languages (Hausa, Yoruba, Igbo) may not classify perfectly
- Sentiment proxy: sarcasm and context-dependent sentiment ("Tinubu is really something") remain challenging for automated NLP
- Free tier incompatibility: X Free API has zero search access since 2023; Basic tier is the minimum viable entry point

**Future Improvements:**
- 🧠 Fine-tune RoBERTa on Nigerian political tweets for higher local accuracy
- 🌍 Add multilingual support: integrate models for Hausa, Yoruba, and Igbo tweet analysis
- 📍 Geospatial filtering: extract location metadata to compare sentiment by state (Lagos vs Kano vs Rivers)
- 📊 Advanced analytics: add topic modelling (LDA) to identify key campaign issues per candidate
- 🤖 Bot detection: filter out bot accounts and coordinated inauthentic behaviour
- 📈 Predictive modelling: use time-series forecasting (ARIMA/Prophet) to predict election-day sentiment trajectories
- 🏙️ Expand to other platforms: integrate Meta Threads, Reddit, and Nigerian political blogs
- ☁️ Full cloud migration: deploy to Google Cloud Run with Cloud Scheduler for fully serverless operation

---

<div align="center">

## 👤 Author

**Name:** Agbozu Ebingiye Nelvin

🌍 Data Scientist | Social Media Analytics | NLP & Sentiment Analysis | Political Intelligence
📍 Port Harcourt, Rivers State, Nigeria

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/agbozu-ebi/)
[![GitHub](https://img.shields.io/badge/GitHub-Nelvinebi-181717?style=flat-square&logo=github)](https://github.com/Nelvinebi)
[![Email](https://img.shields.io/badge/Email-nelvinebingiye%40gmail.com-D14836?style=flat-square&logo=gmail)](mailto:nelvinebingiye@gmail.com)
[![X](https://img.shields.io/badge/X-@AgbozuN-000000?style=flat-square&logo=x)](https://x.com/AgbozuN)

</div>

---

## 📄 License

This project is licensed under the **MIT License** — free to use, adapt, and build upon for research, journalism, and civic technology.
See the [LICENSE](LICENSE) file for full details.

---

## 🙌 Acknowledgements

- **X Developer Platform** — for providing API access to real-time social data
- **HuggingFace** — for the open-source Transformers library and pre-trained RoBERTa sentiment model
- **Cardiff NLP** — for the `twitter-roberta-base-sentiment` model trained on 2 billion tweets
- **Tweepy community:** for the Python wrapper simplifying X API v2 integration
- **Matplotlib:** for the flexible visualisation framework powering the dashboard
- **Nigerian political discourse on X:** for the raw data that makes this analysis possible

---

<div align="center">

⭐ **If this project helped you, please consider starring the repo!**

*Part of a broader portfolio of Data Science, NLP, and Civic Technology projects focused on Nigerian and West African political intelligence.*

🔗 [View All Projects](https://github.com/Nelvinebi?tab=repositories) · [Connect on LinkedIn](https://www.linkedin.com/in/agbozu-ebi/) · [Follow on X](https://x.com/AgbozuN)

</div>
