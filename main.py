import argparse
from fetch_reviews import ReviewsFetcher
from analyze_reviews import TransformerAnalyzer
from visualize_results import ResultsVisualizer
from config import Config
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description='Google Reviews Sentiment Analysis')
    parser.add_argument('--fetch', action='store_true', help='Fetch new reviews from Google')
    parser.add_argument('--analyze', action='store_true', help='Analyze reviews with Transformers')
    parser.add_argument('--visualize', action='store_true', help='Create visualizations')
    parser.add_argument('--all', action='store_true', help='Run complete pipeline')
    
    args = parser.parse_args()
    
    Config.setup_directories()
    
    # Run complete pipeline
    if args.all or (args.fetch and args.analyze and args.visualize):
        print("\n🚀 Running complete analysis pipeline...\n")
        
        # Step 1: Fetch reviews
        fetcher = ReviewsFetcher()
        df = fetcher.fetch_and_save_reviews()
        
        # Step 2: Analyze with Transformers
        analyzer = TransformerAnalyzer()
        df_analyzed = analyzer.analyze_all_reviews(df)
        df_analyzed.to_csv(Config.ANALYZED_REVIEWS_FILE, index=False)
        print(f"\n✓ Analysis complete! Saved to {Config.ANALYZED_REVIEWS_FILE}")
        
        # Step 3: Create visualizations
        visualizer = ResultsVisualizer(df_analyzed)
        visualizer.create_dashboard()
        visualizer.generate_summary_report()
        
        print("\n✅ All done! Check the 'visualizations' folder for results.")
        return
    
    # Individual steps
    if args.fetch:
        fetcher = ReviewsFetcher()
        fetcher.fetch_and_save_reviews()
    
    if args.analyze:
        df = pd.read_csv(Config.RAW_REVIEWS_FILE)
        analyzer = TransformerAnalyzer()
        df_analyzed = analyzer.analyze_all_reviews(df)
        df_analyzed.to_csv(Config.ANALYZED_REVIEWS_FILE, index=False)
        print(f"\n✓ Analysis saved to {Config.ANALYZED_REVIEWS_FILE}")
    
    if args.visualize:
        df = pd.read_csv(Config.ANALYZED_REVIEWS_FILE)
        visualizer = ResultsVisualizer(df)
        visualizer.create_dashboard()
        visualizer.generate_summary_report()
    
    if not any([args.fetch, args.analyze, args.visualize, args.all]):
        parser.print_help()

if __name__ == "__main__":
    main()
