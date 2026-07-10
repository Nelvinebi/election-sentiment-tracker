"""
Chart generation. Creates the 4-panel dashboard.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime
from src.config import CHARTS_DIR


def generate_dashboard(df: pd.DataFrame, daily: dict, weekly: dict, overall: dict) -> str:
    """
    Generate the full 4-panel chart.
    Returns: path to saved PNG file
    """
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    fig.suptitle(
        'Nigeria 2026 Presidential Election - Sentiment Tracker',
        fontsize=20, fontweight='bold', y=0.98
    )
    
    # Convert date strings to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Color scheme
    colors = {'Tinubu': '#FF4444', 'Obi': '#44AA44', 'Atiku': '#4444FF'}
    
    # --- PANEL 1: Daily Mention Volume ---
    ax1 = axes[0, 0]
    for candidate in ['Tinubu', 'Obi', 'Atiku']:
        ax1.plot(df['date'], df[f'{candidate}_mentions'], 
                marker='o', linewidth=2.5, label=candidate, 
                color=colors[candidate], markersize=6)
    ax1.set_title('Daily Mention Volume', fontsize=14, fontweight='bold', pad=10)
    ax1.set_xlabel('Date', fontsize=11)
    ax1.set_ylabel('Number of Mentions', fontsize=11)
    ax1.legend(loc='upper left', frameon=True)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # --- PANEL 2: Daily Sentiment Trends ---
    ax2 = axes[0, 1]
    for candidate in ['Tinubu', 'Obi', 'Atiku']:
        ax2.plot(df['date'], df[f'{candidate}_sentiment'] * 100,
                marker='s', linewidth=2.5, label=candidate,
                color=colors[candidate], markersize=6)
    ax2.axhline(y=50, color='gray', linestyle='--', alpha=0.5, label='Neutral (50%)')
    ax2.set_title('Daily Sentiment Score (%)', fontsize=14, fontweight='bold', pad=10)
    ax2.set_xlabel('Date', fontsize=11)
    ax2.set_ylabel('Sentiment %', fontsize=11)
    ax2.legend(loc='upper left', frameon=True)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_ylim(0, 100)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # --- PANEL 3: 7-Day Rolling Average ---
    ax3 = axes[1, 0]
    candidates = ['Tinubu', 'Obi', 'Atiku']
    x_pos = range(len(candidates))
    
    weekly_mentions = [weekly[c]['avg_mentions'] for c in candidates]
    weekly_sentiment = [weekly[c]['avg_sentiment'] * 100 for c in candidates]
    
    bars = ax3.bar(x_pos, weekly_mentions, color=[colors[c] for c in candidates], 
                   alpha=0.8, edgecolor='black', linewidth=1.5)
    ax3.set_title(f'7-Day Average ({weekly["period"]})', fontsize=14, fontweight='bold', pad=10)
    ax3.set_xlabel('Candidate', fontsize=11)
    ax3.set_ylabel('Average Mentions', fontsize=11)
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(candidates)
    ax3.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    # Add sentiment labels on bars
    for bar, sent in zip(bars, weekly_sentiment):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 20,
                f'Sentiment: {sent:.0f}%',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # --- PANEL 4: Overall Summary ---
    ax4 = axes[1, 1]
    overall_mentions = [overall[c]['avg_mentions'] for c in candidates]
    overall_sentiment = [overall[c]['avg_sentiment'] * 100 for c in candidates]
    
    bars = ax4.barh(candidates, overall_mentions, 
                    color=[colors[c] for c in candidates],
                    alpha=0.8, edgecolor='black', linewidth=1.5)
    ax4.set_title(f'Overall Average (Since {overall["start_date"]})', 
                  fontsize=14, fontweight='bold', pad=10)
    ax4.set_xlabel('Average Daily Mentions', fontsize=11)
    ax4.grid(True, alpha=0.3, axis='x', linestyle='--')
    
    # Add sentiment and total labels
    for i, (bar, sent, total) in enumerate(zip(bars, overall_sentiment, 
                                                [overall[c]['total_mentions'] for c in candidates])):
        width = bar.get_width()
        ax4.text(width + 30, bar.get_y() + bar.get_height()/2.,
                f'Sentiment: {sent:.0f}% | Total: {total:,}',
                ha='left', va='center', fontweight='bold', fontsize=10)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = f'{CHARTS_DIR}/dashboard_{timestamp}.png'
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ Chart saved: {filepath}")
    return filepath
