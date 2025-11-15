import os
import json
from datetime import datetime
import pandas as pd

def track_usage():
    usage_file = 'usage_tracking/api_usage.json'
    os.makedirs('usage_tracking', exist_ok=True)
    
    # Load existing usage data
    if os.path.exists(usage_file):
        with open(usage_file, 'r') as f:
            usage_data = json.load(f)
    else:
        usage_data = {
            'start_date': datetime.now().isoformat(),
            'budget': 450,
            'days_total': 90,
            'daily_calls': []
        }
    
    # Calculate current usage
    # Places API Details with reviews: $17 per 1000 requests
    # We make 1 request per day = $0.017/day
    # Over 90 days = $1.53 total (very conservative)
    
    # To use more of the budget, we could:
    # - Make multiple requests for different place IDs
    # - Use other Google APIs (Geocoding, etc.)
    # - Increase frequency
    
    daily_cost = 0.017  # Cost per request
    
    usage_data['daily_calls'].append({
        'date': datetime.now().isoformat(),
        'requests': 1,
        'estimated_cost': daily_cost
    })
    
    # Calculate totals
    total_cost = sum(d['estimated_cost'] for d in usage_data['daily_calls'])
    days_elapsed = len(usage_data['daily_calls'])
    remaining_budget = usage_data['budget'] - total_cost
    days_remaining = usage_data['days_total'] - days_elapsed
    
    # Save updated usage
    with open(usage_file, 'w') as f:
        json.dump(usage_data, f, indent=2)
    
    # Generate summary
    summary = f'''
API USAGE SUMMARY
=================
Start Date: {usage_data['start_date'][:10]}
Days Elapsed: {days_elapsed} / {usage_data['days_total']}
Total Cost: ${total_cost:.2f} / ${usage_data['budget']:.2f}
Remaining Budget: ${remaining_budget:.2f}
Days Remaining: {days_remaining}

Average Daily Cost: ${total_cost/max(days_elapsed,1):.2f}
Projected Total Cost: ${(total_cost/max(days_elapsed,1)) * usage_data['days_total']:.2f}

NOTE: Current usage rate is very conservative. 
To utilize more budget, consider:
- Adding multiple store locations
- Increasing fetch frequency
- Adding other Google APIs
'''
    
    print(summary)
    with open('usage_tracking/usage_summary.txt', 'w') as f:
        f.write(summary)
    
    return usage_data

if __name__ == "__main__":
    track_usage()
