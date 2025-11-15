# Automated Review Analysis Setup

## GitHub Actions Workflows

This project includes 3 automated workflows:

### 1. Daily Review Analysis (`daily-review-analysis.yml`)
- **Runs**: Every day at 2 AM UTC
- **Does**: Fetches reviews, analyzes with Transformers, saves results
- **Cost**: ~$0.017/day = ~$1.53 over 90 days

### 2. Weekly Comprehensive Report (`weekly-comprehensive-report.yml`)
- **Runs**: Every Sunday at 3 AM UTC
- **Does**: Full analysis + email report
- **Cost**: ~$0.017/week

### 3. Cost Tracker (`cost-tracker.yml`)
- **Runs**: Daily at midnight
- **Does**: Tracks API usage and costs
- **Cost**: $0 (no API calls)

## Setup Instructions

### 1. Add GitHub Secrets

Go to your repository → Settings → Secrets → Actions → New repository secret

Add these secrets:
- `GOOGLE_PLACES_API_KEY` - Your Google Places API key
- `PLACE_ID` - Your store's Place ID
- `EMAIL_USERNAME` - Gmail for sending reports (optional)
- `EMAIL_PASSWORD` - Gmail app password (optional)
- `EMAIL_TO` - Email to receive reports (optional)

### 2. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Enable workflows
4. Workflows will run automatically on schedule

### 3. Manual Trigger

To run manually:
1. Go to Actions tab
2. Select a workflow
3. Click "Run workflow"

## Cost Analysis

**Current Configuration:**
- 1 API request per day = $0.017/day
- 90 days = ~$1.53 total
- **Remaining budget: $448.47**

**To Use More Budget:**

### Option A: Multiple Locations (Recommended)
If you have multiple stores:
```yaml
strategy:
  matrix:
    place_id: 
      - 'ChIJ...' # Store 1
      - 'ChIJ...' # Store 2
      - 'ChIJ...' # Store 3
```
Cost: $1.53 × 3 = $4.59 over 90 days

### Option B: Increase Frequency
Change cron to run multiple times per day:
```yaml
- cron: '0 */6 * * *'  # Every 6 hours = 4x/day
```
Cost: $1.53 × 4 = $6.12 over 90 days

### Option C: Add More Google APIs
- Geocoding API
- Distance Matrix API
- Places Nearby Search
- Text Search

### Option D: Historical Analysis
Fetch and analyze competitor reviews:
```python
# Add to fetch_reviews.py
competitor_place_ids = ['ChIJ...', 'ChIJ...', 'ChIJ...']
```

**Recommended for $450 budget:**
Combine all options to analyze 20-30 locations daily = ~$30-50/month

## Monitoring

Check usage:
1. View `usage_tracking/usage_summary.txt` in repository
2. Check GitHub Actions logs
3. Review Google Cloud Console billing

## Email Reports

To enable email reports, set up Gmail:

1. Create app password: Google Account → Security → 2FA → App passwords
2. Add secrets: `EMAIL_USERNAME`, `EMAIL_PASSWORD`, `EMAIL_TO`
3. Weekly reports will be sent automatically

## Data Storage

All results are:
- Committed to repository (historical tracking)
- Available as artifacts (90-day retention)
- Viewable in `data/` and `visualizations/` folders

## Troubleshooting

**Workflow not running?**
- Check Actions tab for errors
- Verify secrets are set correctly
- Ensure workflows are enabled

**API errors?**
- Check API key is valid
- Verify Places API is enabled in Google Cloud
- Check billing is enabled

**Want to stop?**
- Go to Actions → Select workflow → Disable workflow
