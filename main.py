"""
Google Cloud Functions entry point.
Trigger: HTTP (for testing) or Cloud Scheduler (for production).
"""

import functions_framework
from src.database import init_db, save_daily_data
from src.collector import collect_all_data
from src.analyzer import run_full_analysis
from src.visualizer import generate_dashboard
from src.publisher import get_writeup, publish_to_x
import json
import os


@functions_framework.http
def run_tracker(request):
    """
    HTTP Cloud Function entry point.
    Call this URL daily via Cloud Scheduler.
    """
    try:
        # Initialize
        init_db()
        
        # Collect
        data = collect_all_data()
        save_daily_data(data)
        
        # Analyze
        daily, weekly, overall, df = run_full_analysis()
        
        # Generate chart
        chart_path = generate_dashboard(df, daily, weekly, overall)
        
        # Generate write-up
        writeup = get_writeup(daily, weekly, overall)
        
        # Publish
        tweet_url = publish_to_x(chart_path, writeup)
        
        return {
            'status': 'success',
            'date': daily['date'],
            'tweet_url': tweet_url,
            'summary': {
                'daily': daily,
                'weekly': weekly
            }
        }, 200
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500