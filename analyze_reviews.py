import pandas as pd
import torch
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification
)
from tqdm import tqdm
from config import Config
import warnings
warnings.filterwarnings('ignore')

class TransformerAnalyzer:
    def __init__(self):
        print("Loading Transformer models...")
        print("This may take a few minutes on first run...")
        
        # Sentiment Analysis (BERT-based)
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model=Config.SENTIMENT_MODEL,
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Emotion Detection
        self.emotion_analyzer = pipeline(
            "text-classification",
            model=Config.EMOTION_MODEL,
            top_k=None,
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Zero-shot Classification for category detection
        self.category_classifier = pipeline(
            "zero-shot-classification",
            model=Config.ZERO_SHOT_MODEL,
            device=0 if torch.cuda.is_available() else -1
        )
        
        print("✓ All models loaded successfully!\n")
    
    def analyze_sentiment(self, text):
        """Analyze sentiment using DistilBERT"""
        try:
            result = self.sentiment_analyzer(text[:512])[0]  # Truncate to 512 tokens
            return {
                'sentiment_label': result['label'],
                'sentiment_score': result['score']
            }
        except Exception as e:
            return {'sentiment_label': 'ERROR', 'sentiment_score': 0}
    
    def analyze_emotion(self, text):
        """Detect emotions using RoBERTa"""
        try:
            results = self.emotion_analyzer(text[:512])[0]
            # Get top 3 emotions
            sorted_emotions = sorted(results, key=lambda x: x['score'], reverse=True)[:3]
            return {
                'primary_emotion': sorted_emotions[0]['label'],
                'primary_emotion_score': sorted_emotions[0]['score'],
                'secondary_emotion': sorted_emotions[1]['label'] if len(sorted_emotions) > 1 else None,
                'secondary_emotion_score': sorted_emotions[1]['score'] if len(sorted_emotions) > 1 else 0,
                'all_emotions': {e['label']: e['score'] for e in results}
            }
        except Exception as e:
            return {
                'primary_emotion': 'ERROR',
                'primary_emotion_score': 0,
                'secondary_emotion': None,
                'secondary_emotion_score': 0,
                'all_emotions': {}
            }
    
    def classify_categories(self, text):
        """Classify review into multiple categories using zero-shot"""
        try:
            result = self.category_classifier(
                text[:512],
                Config.CATEGORIES,
                multi_label=True
            )
            
            # Get categories with score > 0.5
            relevant_categories = [
                label for label, score in zip(result['labels'], result['scores'])
                if score > 0.5
            ]
            
            return {
                'categories': relevant_categories[:3],  # Top 3 categories
                'category_scores': dict(zip(result['labels'][:3], result['scores'][:3]))
            }
        except Exception as e:
            return {'categories': [], 'category_scores': {}}
    
    def extract_key_phrases(self, text):
        """Simple keyword extraction (can be enhanced with NER)"""
        # Common positive/negative indicators
        positive_keywords = ['great', 'excellent', 'amazing', 'love', 'best', 'wonderful',
                           'friendly', 'helpful', 'clean', 'quality', 'recommend']
        negative_keywords = ['bad', 'terrible', 'worst', 'hate', 'poor', 'rude',
                           'dirty', 'expensive', 'slow', 'disappointed', 'avoid']
        
        text_lower = text.lower()
        found_positive = [word for word in positive_keywords if word in text_lower]
        found_negative = [word for word in negative_keywords if word in text_lower]
        
        return {
            'positive_keywords': found_positive[:5],
            'negative_keywords': found_negative[:5]
        }
    
    def analyze_review(self, text):
        """Complete analysis of a single review"""
        if not text or len(text.strip()) < 10:
            return None
        
        analysis = {}
        
        # Sentiment
        sentiment_result = self.analyze_sentiment(text)
        analysis.update(sentiment_result)
        
        # Emotion
        emotion_result = self.analyze_emotion(text)
        analysis.update(emotion_result)
        
        # Categories
        category_result = self.classify_categories(text)
        analysis.update(category_result)
        
        # Keywords
        keywords = self.extract_key_phrases(text)
        analysis.update(keywords)
        
        return analysis
    
    def analyze_all_reviews(self, df):
        """Analyze all reviews in the dataframe"""
        print("Analyzing reviews with Transformers...")
        print("This will take a few minutes...\n")
        
        results = []
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            analysis = self.analyze_review(row['text'])
            if analysis:
                results.append(analysis)
            else:
                results.append({})
        
        # Create new columns for analysis results
        for key in results[0].keys():
            if key not in ['categories', 'category_scores', 'all_emotions', 
                          'positive_keywords', 'negative_keywords']:
                df[key] = [r.get(key) for r in results]
            else:
                df[key] = [str(r.get(key, {})) for r in results]
        
        return df
