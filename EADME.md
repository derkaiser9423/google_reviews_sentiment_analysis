"""
# Google Reviews Sentiment Analysis with Transformers

Advanced sentiment analysis system using state-of-the-art Transformer models to analyze Google Maps reviews.

## Features

- 🤖 **Multi-Model Transformer Analysis**
  - Sentiment Analysis (DistilBERT)
  - Emotion Detection (RoBERTa)
  - Category Classification (BART Zero-Shot)

- 📊 **Comprehensive Insights**
  - Sentiment distribution and scoring
  - Emotion detection (joy, anger, sadness, etc.)
  - Automatic category classification
  - Keyword extraction
  - Interactive visualizations

- 💾 **Data Management**
  - CSV export of raw and analyzed data
  - Organized file structure
  - Easy to integrate with other tools

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/google-reviews-sentiment-analysis.git
cd google-reviews-sentiment-analysis
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your Google Places API key and Place ID
```

## Usage

Run complete analysis:
```bash
python main.py --all
```

Or run individual steps:
```bash
python main.py --fetch      # Fetch reviews from Google
python main.py --analyze    # Analyze with Transformers
python main.py --visualize  # Generate visualizations
```

## Output

- `data/raw_reviews.csv` - Raw reviews from Google
- `data/analyzed_reviews.csv` - Reviews with sentiment analysis
- `visualizations/sentiment_report.html` - Interactive dashboard
- `visualizations/summary_report.txt` - Text summary

## Models Used

- **Sentiment**: distilbert-base-uncased-finetuned-sst-2-english
- **Emotion**: j-hartmann/emotion-english-distilroberta-base
- **Categories**: facebook/bart-large-mnli (zero-shot)

## Project Structure

```
├── config.py              # Configuration
├── fetch_reviews.py       # Google Places API integration
├── analyze_reviews.py     # Transformer analysis
├── visualize_results.py   # Visualization generation
├── main.py               # Main pipeline
├── data/                 # CSV storage
└── visualizations/       # Output reports
```

## Requirements

- Python 3.8+
- Google Places API key
- GPU recommended (but works on CPU)

## License

MIT License
"""
