import pandas as pd
from datetime import datetime, timedelta
import os

def generate_weekly_report():
    # Load all analyzed data
    df = pd.read_csv('data/analyzed_reviews.csv')
    df['fetched_at'] = pd.to_datetime(df['fetched_at'])
    
    # Filter last 7 days
    week_ago = datetime.now() - timedelta(days=7)
    df_week = df[df['fetched_at'] > week_ago]
    
    report = []
    report.append("="*70)
    report.append(f"WEEKLY REVIEW ANALYSIS REPORT")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("="*70)
    
    report.append(f"\\nTotal Reviews This Week: {len(df_week)}")
    report.append(f"Total Reviews Overall: {len(df)}")
    
    # Week over week comparison
    two_weeks_ago = datetime.now() - timedelta(days=14)
    df_prev_week = df[(df['fetched_at'] > two_weeks_ago) & (df['fetched_at'] <= week_ago)]
    
    if len(df_prev_week) > 0:
        sentiment_change = (
            df_week['sentiment_label'].value_counts(normalize=True).get('POSITIVE', 0) -
            df_prev_week['sentiment_label'].value_counts(normalize=True).get('POSITIVE', 0)
        ) * 100
        report.append(f"\\nSentiment Change: {sentiment_change:+.1f}%")
    
    # Top issues this week
    report.append("\\n--- TOP CONCERNS THIS WEEK ---")
    if len(df_week[df_week['sentiment_label'] == 'NEGATIVE']) > 0:
        negative_week = df_week[df_week['sentiment_label'] == 'NEGATIVE']
        report.append(f"Negative reviews: {len(negative_week)}")
        
        # Extract keywords from negative reviews
        import ast
        from collections import Counter
        all_keywords = []
        for keywords in negative_week['negative_keywords'].dropna():
            try:
                keywords = ast.literal_eval(keywords) if isinstance(keywords, str) else keywords
                all_keywords.extend(keywords)
            except:
                continue
        
        if all_keywords:
            for keyword, count in Counter(all_keywords).most_common(5):
                report.append(f"  - {keyword}: {count} mentions")
    
    # Save report
    report_text = "\\n".join(report)
    os.makedirs('visualizations', exist_ok=True)
    with open('visualizations/weekly_report.txt', 'w') as f:
        f.write(report_text)
    
    print(report_text)
    return report_text

if __name__ == "__main__":
    generate_weekly_report()
