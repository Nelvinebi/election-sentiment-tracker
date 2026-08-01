#!/usr/bin/env python3
"""
Manual trigger for full pipeline. Use for testing locally.
"""

from src.database import init_db, save_daily_data
from src.collector import collect_all_data
from src.analyzer import run_full_analysis
from src.visualizer import generate_dashboard
from src.publisher import get_writeup, publish_to_x
import json
from src.config import REPORTS_DIR


def main():
    print("=" * 60)
    print("🗳️  ELECTION SENTIMENT TRACKER — FULL RUN")
    print("=" * 60)
    
    # Step 1: Ensure DB exists
    init_db()
    
    # Step 2: Collect data
    print("\\n📥 STEP 1: Data Collection")
    data = collect_all_data()
    save_daily_data(data)
    
    # Step 3: Analyze
    print("\\n📊 STEP 2: Analysis")
    daily, weekly, overall, df = run_full_analysis()
    
    # Step 4: Save reports
    print("\\n💾 STEP 3: Saving Reports")
    with open(f'{REPORTS_DIR}/daily.json', 'w') as f:
        json.dump(daily, f, indent=2)
    with open(f'{REPORTS_DIR}/weekly.json', 'w') as f:
        json.dump(weekly, f, indent=2)
    with open(f'{REPORTS_DIR}/overall.json', 'w') as f:
        json.dump(overall, f, indent=2)
    
    # Step 5: Generate charts
    print("\\n📈 STEP 4: Chart Generation")
    chart_path = generate_dashboard(df, daily, weekly, overall)
    
    # Step 6: Generate write-up
    print("\\n✍️  STEP 5: Write-up")
    writeup = get_writeup(daily, weekly, overall)
    with open(f'{REPORTS_DIR}/writeup.txt', 'w') as f:
        f.write(writeup)
    print(writeup)
    
    # Step 7: Publish (optional — comment out if testing)
    print("\\n🐦 STEP 6: Publishing to X")
    # tweet_url = publish_to_x(chart_path, writeup)
    
    print("\\n" + "=" * 60)
    print("✅ COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()