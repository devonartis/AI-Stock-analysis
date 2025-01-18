import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import os
from newsapi import NewsApiClient
import pandas as pd
import numpy as np
from textblob import TextBlob
import yfinance as yf
from pydantic import BaseModel

from ..schemas.service import NewsServiceInput
from ..utils.logging import setup_logging

logger = setup_logging()

class NewsArticle(BaseModel):
    title: str
    source: str
    url: str
    published_date: str
    description: Optional[str]
    sentiment_score: float
    subjectivity_score: float
    summary: str

class NewsService:
    """
    Service for fetching and analyzing news articles related to stocks.
    
    This service provides functionality to:
    1. Fetch company-specific news using NewsAPI
    2. Filter news for relevance using a two-layer approach
    3. Perform sentiment analysis on news content
    4. Generate sentiment summaries and trends
    
    The service ensures news relevance by:
    - Using exact phrase matching for company names and tickers
    - Including financial context keywords
    - Validating article content for company mentions
    - Calculating sentiment scores and trends
    """
    
    def __init__(self):
        """Initialize the NewsService with NewsAPI client."""
        self.news_api = NewsApiClient(api_key=os.getenv('NEWS_API_KEY', 'your-api-key'))
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def get_company_news(self, company_name: str, ticker: str, days: int = 7) -> List[Dict]:
        """
        Fetch and filter news articles about the company.
        
        Uses a two-layer filtering approach:
        1. First layer: NewsAPI query with company name, ticker, and financial terms
        2. Second layer: Content validation to ensure company relevance
        
        Args:
            company_name: Full company name (e.g., "Alphabet Inc.")
            ticker: Stock ticker symbol (e.g., "GOOG")
            days: Number of days of news to fetch (default: 7)
            
        Returns:
            List of processed news articles with sentiment analysis
        """
        # Validate inputs using Pydantic
        input_data = NewsServiceInput(
            company_name=company_name,
            ticker=ticker,
            days=days
        )
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Create a more specific search query with financial context
        search_terms = [
            f'"{company_name}"',  # Exact company name match
            f'"{ticker}"',        # Exact ticker match
            'earnings',           # Financial terms for context
            'stock',
            'financial results',
            'market',
            'shares'
        ]
        
        # First layer: Fetch from NewsAPI with strict filtering
        articles = self.news_api.get_everything(
            q=f'({" OR ".join(search_terms)}) AND ({company_name} OR {ticker})',
            from_param=from_date,
            language='en',
            sort_by='relevancy'
        )
        
        # Second layer: Process and validate article content
        processed_articles = []
        for article in articles['articles']:
            # Validate that article actually mentions company
            text = f"{article['title']} {article.get('description', '')}"
            if company_name.lower() in text.lower() or ticker.lower() in text.lower():
                # Perform sentiment analysis on combined text
                sentiment = TextBlob(text).sentiment
                
                # Create structured news article object
                processed_article = NewsArticle(
                    title=article['title'],
                    source=article['source']['name'],
                    url=article['url'],
                    published_date=article['publishedAt'],
                    description=article.get('description'),
                    sentiment_score=sentiment.polarity,
                    subjectivity_score=sentiment.subjectivity,
                    summary=text[:200] + '...' if len(text) > 200 else text
                )
                processed_articles.append(processed_article.dict())
        
        return processed_articles

    def get_market_news(self) -> List[Dict]:
        """Fetch general market news"""
        articles = self.news_api.get_top_headlines(
            category='business',
            language='en'
        )
        
        processed_articles = []
        for article in articles['articles']:
            sentiment = TextBlob(article['title'] + ' ' + (article['description'] or '')).sentiment
            
            processed_articles.append({
                'title': article['title'],
                'source': article['source']['name'],
                'url': article['url'],
                'published_date': article['publishedAt'],
                'description': article['description'],
                'sentiment_score': sentiment.polarity,
                'subjectivity_score': sentiment.subjectivity
            })
        
        return processed_articles

    def get_sec_filings(self, ticker: str) -> List[Dict]:
        """Fetch recent SEC filings"""
        # This would typically use the SEC EDGAR API
        # For now, returning sample data
        return [{
            'type': '10-K',
            'date': datetime.now() - timedelta(days=30),
            'description': 'Annual Report',
            'url': f'https://www.sec.gov/edgar/searchedgar/companysearch.html'
        }]

    def analyze_news_impact(self, news_articles: List[Dict]) -> Dict:
        """
        Analyze the potential market impact of news.
        
        This method calculates sentiment metrics, trends, and impact scores.
        
        Args:
            news_articles: List of news articles with sentiment analysis
        
        Returns:
            Dictionary with overall sentiment, sentiment trend, key topics, and impact score
        """
        if not news_articles:
            return {
                'overall_sentiment': 0,
                'sentiment_trend': 'neutral',
                'key_topics': [],
                'impact_score': 0
            }
        
        # Calculate sentiment metrics
        sentiments = [article['sentiment_score'] for article in news_articles]
        
        # Analyze sentiment trend
        sentiment_trend = 'neutral'
        if len(sentiments) >= 3:
            recent_sentiment = np.mean(sentiments[:3])
            older_sentiment = np.mean(sentiments[3:]) if len(sentiments) > 3 else 0
            if recent_sentiment > older_sentiment + 0.1:
                sentiment_trend = 'improving'
            elif recent_sentiment < older_sentiment - 0.1:
                sentiment_trend = 'deteriorating'
        
        # Calculate impact score (0-100)
        impact_score = min(100, max(0, (
            abs(np.mean(sentiments)) * 50 +  # Sentiment strength
            min(50, len(news_articles) * 5)   # News volume
        )))
        
        return {
            'overall_sentiment': float(np.mean(sentiments)),
            'sentiment_trend': sentiment_trend,
            'key_topics': self._extract_key_topics(news_articles),
            'impact_score': float(impact_score)
        }

    def _extract_key_topics(self, articles: List[Dict]) -> List[str]:
        """Extract key topics from news articles"""
        # This would typically use NLP topic modeling
        # For now, returning sample topics
        return ['earnings', 'growth', 'market share']

    def get_social_media_sentiment(self, ticker: str) -> Dict:
        """Get sentiment from social media platforms"""
        # This would integrate with Twitter/Reddit APIs
        return {
            'reddit_sentiment': 0.65,
            'twitter_sentiment': 0.72,
            'total_mentions': 1500,
            'trending_score': 85
        }

    def generate_news_summary(self, company_name: str, ticker: str) -> Dict:
        """
        Generate comprehensive news analysis.
        
        This method fetches company news, market news, SEC filings, and social media sentiment.
        It then analyzes the news impact and generates a summary.
        
        Args:
            company_name: Full company name (e.g., "Alphabet Inc.")
            ticker: Stock ticker symbol (e.g., "GOOG")
        
        Returns:
            Dictionary with news summary, sentiment analysis, and impact scores
        """
        # Fetch all news data
        company_news = self.get_company_news(company_name, ticker)
        market_news = self.get_market_news()
        sec_filings = self.get_sec_filings(ticker)
        social_sentiment = self.get_social_media_sentiment(ticker)
        
        # Analyze news impact
        company_impact = self.analyze_news_impact(company_news)
        market_impact = self.analyze_news_impact(market_news)
        
        return {
            'company_news': company_news[:10],  # Latest 10 articles
            'market_news': market_news[:5],     # Latest 5 market news
            'sec_filings': sec_filings,
            'social_sentiment': social_sentiment,
            'company_impact': company_impact,
            'market_impact': market_impact,
            'analysis_timestamp': datetime.now().isoformat()
        }
