import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    GOOGLE_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
    PLACE_ID = os.getenv('PLACE_ID')
    
    # File paths
    DATA_DIR = 'data'
    RAW_REVIEWS_FILE = os.path.join(DATA_DIR, 'raw_reviews.csv')
    ANALYZED_REVIEWS_FILE = os.path.join(DATA_DIR, 'analyzed_reviews.csv')
    VISUALIZATIONS_DIR = 'visualizations'
    
    # Model configuration
    SENTIMENT_MODEL = 'distilbert-base-uncased-finetuned-sst-2-english'
    EMOTION_MODEL = 'j-hartmann/emotion-english-distilroberta-base'
    ZERO_SHOT_MODEL = 'facebook/bart-large-mnli'
    
    # Categories for zero-shot classification
    CATEGORIES = [
        'product quality',
        'customer service',
        'pricing and value',
        'store cleanliness',
        'staff friendliness',
        'wait time',
        'location and parking',
        'product variety',
        'return policy',
        'online ordering'
    ]
    
    # Create directories if they don't exist
    @staticmethod
    def setup_directories():
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        os.makedirs(Config.VISUALIZATIONS_DIR, exist_ok=True)
