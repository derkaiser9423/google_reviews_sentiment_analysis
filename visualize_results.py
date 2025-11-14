import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from config import Config
from collections import Counter
import ast

class ResultsVisualizer:
    def __init__(self, df):
        self.df = df
    
    def create_dashboard(self):
        """Create comprehensive visualization dashboard"""
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Sentiment Distribution',
                'Rating Distribution',
                'Top Emotions Detected',
                'Category Mentions',
                'Sentiment vs Rating',
                'Timeline Analysis'
            ),
            specs=[
                [{'type': 'pie'}, {'type': 'bar'}],
                [{'type': 'bar'}, {'type': 'bar'}],
                [{'type': 'scatter'}, {'type': 'scatter'}]
            ]
        )
        
        # 1. Sentiment Distribution
        sentiment_counts = self.df['sentiment_label'].value_counts()
        fig.add_trace(
            go.Pie(labels=sentiment_counts.index, values=sentiment_counts.values,
                   marker=dict(colors=['#2ecc71', '#e74c3c'])),
            row=1, col=1
        )
        
        # 2. Rating Distribution
        rating_counts = self.df['rating'].value_counts().sort_index()
        fig.add_trace(
            go.Bar(x=rating_counts.index, y=rating_counts.values,
                   marker_color='lightblue'),
            row=1, col=2
        )
        
        # 3. Top Emotions
        emotions = []
        for emotion_dict in self.df['all_emotions'].dropna():
            try:
                emotion_dict = ast.literal_eval(emotion_dict) if isinstance(emotion_dict, str) else emotion_dict
                emotions.extend(emotion_dict.keys())
            except:
                continue
        emotion_counts = Counter(emotions).most_common(5)
        if emotion_counts:
            fig.add_trace(
                go.Bar(x=[e[0] for e in emotion_counts], 
                       y=[e[1] for e in emotion_counts],
                       marker_color='coral'),
                row=2, col=1
            )
        
        # 4. Category Mentions
        categories = []
        for cat_list in self.df['categories'].dropna():
            try:
                cat_list = ast.literal_eval(cat_list) if isinstance(cat_list, str) else cat_list
                categories.extend(cat_list)
            except:
                continue
        category_counts = Counter(categories).most_common(8)
        if category_counts:
            fig.add_trace(
                go.Bar(y=[c[0] for c in category_counts],
                       x=[c[1] for c in category_counts],
                       orientation='h',
                       marker_color='mediumpurple'),
                row=2, col=2
            )
        
        # 5. Sentiment vs Rating
        sentiment_map = {'POSITIVE': 1, 'NEGATIVE': 0}
        fig.add_trace(
            go.Scatter(
                x=self.df['rating'],
                y=self.df['sentiment_label'].map(sentiment_map),
                mode='markers',
                marker=dict(size=10, color=self.df['sentiment_score'], 
                          colorscale='RdYlGn', showscale=True),
                text=self.df['text'].str[:100]
            ),
            row=3, col=1
        )
        
        # 6. Timeline
        if 'time' in self.df.columns:
            df_time = self.df.sort_values('time')
            fig.add_trace(
                go.Scatter(x=df_time['time'], y=df_time['rating'],
                          mode='lines+markers',
                          marker=dict(color=df_time['sentiment_label'].map(
                              {'POSITIVE': 'green', 'NEGATIVE': 'red'})),
                          name='Rating over time'),
                row=3, col=2
            )
        
        fig.update_layout(height=1200, showlegend=False,
                         title_text="Google Reviews Analysis Dashboard")
        
        output_file = f"{Config.VISUALIZATIONS_DIR}/sentiment_report.html"
        fig.write_html(output_file)
        print(f"✓ Dashboard saved to {output_file}")
        
        return fig
    
    def generate_summary_report(self):
        """Generate text summary of findings"""
        report = []
        report.append("=" * 60)
        report.append("GOOGLE REVIEWS ANALYSIS SUMMARY")
        report.append("=" * 60)
        report.append(f"\nTotal Reviews Analyzed: {len(self.df)}")
        report.append(f"Average Rating: {self.df['rating'].mean():.2f}/5.0")
        
        # Sentiment breakdown
        sentiment_pct = self.df['sentiment_label'].value_counts(normalize=True) * 100
        report.append("\n--- SENTIMENT ANALYSIS ---")
        for sentiment, pct in sentiment_pct.items():
            report.append(f"{sentiment}: {pct:.1f}%")
        
        # Top emotions
        report.append("\n--- PRIMARY EMOTIONS ---")
        top_emotions = self.df['primary_emotion'].value_counts().head(5)
        for emotion, count in top_emotions.items():
            report.append(f"{emotion}: {count} reviews")
        
        # Most mentioned categories
        report.append("\n--- TOP CATEGORIES ---")
        all_categories = []
        for cats in self.df['categories'].dropna():
            try:
                cats = ast.literal_eval(cats) if isinstance(cats, str) else cats
                all_categories.extend(cats)
            except:
                continue
        for cat, count in Counter(all_categories).most_common(5):
            report.append(f"{cat}: {count} mentions")
        
        # Key insights
        report.append("\n--- KEY INSIGHTS ---")
        negative_reviews = self.df[self.df['sentiment_label'] == 'NEGATIVE']
        if len(negative_reviews) > 0:
            report.append(f"\n⚠ {len(negative_reviews)} negative reviews need attention")
            report.append("\nMost common issues in negative reviews:")
            neg_keywords = []
            for keywords in negative_reviews['negative_keywords'].dropna():
                try:
                    keywords = ast.literal_eval(keywords) if isinstance(keywords, str) else keywords
                    neg_keywords.extend(keywords)
                except:
                    continue
            for keyword, count in Counter(neg_keywords).most_common(5):
                report.append(f"  - {keyword}: {count} times")
        
        report.append("\n" + "=" * 60)
        
        summary_text = "\n".join(report)
        print(summary_text)
        
        # Save to file
        with open(f"{Config.VISUALIZATIONS_DIR}/summary_report.txt", 'w') as f:
            f.write(summary_text)
        
        return summary_text
