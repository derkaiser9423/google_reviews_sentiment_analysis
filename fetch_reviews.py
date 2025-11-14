import requests
import pandas as pd
import time
from datetime import datetime
from config import Config

class ReviewsFetcher:
    def __init__(self):
        self.api_key = Config.GOOGLE_API_KEY
        self.place_id = Config.PLACE_ID
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
    def get_place_details(self):
        """Fetch place details including reviews"""
        url = f"{self.base_url}/details/json"
        params = {
            'place_id': self.place_id,
            'fields': 'name,rating,reviews,user_ratings_total',
            'key': self.api_key,
            'reviews_sort': 'newest'  # or 'most_relevant'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK':
            return data['result']
        else:
            raise Exception(f"API Error: {data['status']}")
    
    def fetch_and_save_reviews(self):
        """
        Fetch reviews and save to CSV
        Note: Google Places API returns max 5 reviews per request
        To get more, you'd need to use pagination or scraping
        """
        print("Fetching reviews from Google Places API...")
        result = self.get_place_details()
        
        reviews = result.get('reviews', [])
        place_name = result.get('name')
        overall_rating = result.get('rating')
        total_reviews = result.get('user_ratings_total')
        
        print(f"\nPlace: {place_name}")
        print(f"Overall Rating: {overall_rating}")
        print(f"Total Reviews on Google: {total_reviews}")
        print(f"Reviews fetched: {len(reviews)}")
        
        # Convert to DataFrame
        reviews_data = []
        for review in reviews:
            reviews_data.append({
                'author_name': review.get('author_name'),
                'rating': review.get('rating'),
                'text': review.get('text'),
                'time': datetime.fromtimestamp(review.get('time')),
                'relative_time': review.get('relative_time_description'),
                'language': review.get('language', 'en'),
                'profile_photo_url': review.get('profile_photo_url'),
                'fetched_at': datetime.now()
            })
        
        df = pd.DataFrame(reviews_data)
        
        # Save to CSV
        Config.setup_directories()
        df.to_csv(Config.RAW_REVIEWS_FILE, index=False)
        print(f"\n✓ Reviews saved to {Config.RAW_REVIEWS_FILE}")
        
        return df
