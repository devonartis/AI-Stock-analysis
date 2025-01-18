import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import yfinance as yf
from bs4 import BeautifulSoup
import requests
import json

from ..schemas.service import AnalysisServiceInput
from ..models.signals import (
    SignalType, SignalStrength, TechnicalSignal,
    BollingerBands, MACD, NewsArticle, SentimentAnalysis,
    TradingSignals
)
from ..utils.logging import setup_logging

logger = setup_logging()

class AnalysisService:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def calculate_bollinger_bands(self, data: pd.DataFrame, window: int = 20, num_std: float = 2) -> BollingerBands:
        """Calculate Bollinger Bands"""
        rolling_mean = data['Close'].rolling(window=window).mean()
        rolling_std = data['Close'].rolling(window=window).std()
        
        upper_band = rolling_mean + (rolling_std * num_std)
        lower_band = rolling_mean - (rolling_std * num_std)
        
        # Calculate additional Bollinger Band indicators
        bandwidth = (upper_band - lower_band) / rolling_mean
        percent_b = (data['Close'] - lower_band) / (upper_band - lower_band)
        
        return BollingerBands(
            upper=float(upper_band.iloc[-1]),
            middle=float(rolling_mean.iloc[-1]),
            lower=float(lower_band.iloc[-1]),
            bandwidth=float(bandwidth.iloc[-1]),
            percent_b=float(percent_b.iloc[-1])
        )

    def calculate_macd(self, data: pd.DataFrame) -> MACD:
        """Calculate MACD indicator"""
        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        macd_line = exp1 - exp2
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        histogram = macd_line - signal_line
        
        # Determine crossover signal
        if macd_line.iloc[-1] > signal_line.iloc[-1] and macd_line.iloc[-2] <= signal_line.iloc[-2]:
            crossover = SignalType.BUY
        elif macd_line.iloc[-1] < signal_line.iloc[-1] and macd_line.iloc[-2] >= signal_line.iloc[-2]:
            crossover = SignalType.SELL
        else:
            crossover = None
        
        return MACD(
            macd_line=float(macd_line.iloc[-1]),
            signal_line=float(signal_line.iloc[-1]),
            histogram=float(histogram.iloc[-1]),
            crossover_signal=crossover
        )

    def get_support_resistance_levels(self, data: pd.DataFrame, window: int = 20) -> Dict[str, List[float]]:
        """Calculate support and resistance levels using local minima/maxima"""
        highs = data['High'].rolling(window=window, center=True).apply(lambda x: x[window//2] == max(x))
        lows = data['Low'].rolling(window=window, center=True).apply(lambda x: x[window//2] == min(x))
        
        resistance_levels = sorted(set(data[highs]['High'].round(2).tolist()[-3:]))
        support_levels = sorted(set(data[lows]['Low'].round(2).tolist()[-3:]))
        
        return {
            'support': support_levels,
            'resistance': resistance_levels
        }

    def analyze_volume(self, data: pd.DataFrame) -> Dict[str, float]:
        """Analyze volume patterns"""
        avg_volume = data['Volume'].mean()
        recent_volume = data['Volume'].iloc[-5:].mean()
        volume_trend = recent_volume / avg_volume
        
        return {
            'average_volume': float(avg_volume),
            'recent_volume': float(recent_volume),
            'volume_trend': float(volume_trend)
        }

    def get_news_sentiment(self, ticker: str) -> List[NewsArticle]:
        """Fetch and analyze recent news articles"""
        # This would typically use a news API and NLP service
        # For now, we'll return sample data
        return [
            NewsArticle(
                title=f"Sample news for {ticker}",
                source="Financial Times",
                url="https://example.com",
                published_date=datetime.now(),
                sentiment_score=0.8,
                summary="Positive outlook for company growth"
            )
        ]

    def generate_trading_signals(self, data: pd.DataFrame, ticker: str) -> TradingSignals:
        """Generate comprehensive trading signals"""
        # Validate inputs using Pydantic
        input_data = AnalysisServiceInput(
            data=data.to_dict(),
            ticker=ticker
        )
        # Convert back to DataFrame
        data = pd.DataFrame(input_data.data)

        current_price = data['Close'].iloc[-1]
        
        # Calculate technical indicators
        bollinger = self.calculate_bollinger_bands(data)
        macd = self.calculate_macd(data)
        rsi = self.calculate_rsi(data)
        levels = self.get_support_resistance_levels(data)
        volume_analysis = self.analyze_volume(data)
        
        # Generate technical signals
        signals = []
        
        # MACD Signal
        if macd.crossover_signal:
            signals.append(TechnicalSignal(
                indicator="MACD",
                signal=macd.crossover_signal,
                strength=SignalStrength.STRONG if abs(macd.histogram) > 0.5 else SignalStrength.MODERATE,
                price_level=current_price,
                timestamp=datetime.now(),
                details="MACD crossover detected"
            ))
        
        # Bollinger Bands Signal
        if current_price <= bollinger.lower:
            signals.append(TechnicalSignal(
                indicator="Bollinger Bands",
                signal=SignalType.BUY,
                strength=SignalStrength.STRONG,
                price_level=current_price,
                timestamp=datetime.now(),
                details="Price at lower Bollinger Band"
            ))
        elif current_price >= bollinger.upper:
            signals.append(TechnicalSignal(
                indicator="Bollinger Bands",
                signal=SignalType.SELL,
                strength=SignalStrength.STRONG,
                price_level=current_price,
                timestamp=datetime.now(),
                details="Price at upper Bollinger Band"
            ))
        
        # RSI Signal
        if rsi <= 30:
            signals.append(TechnicalSignal(
                indicator="RSI",
                signal=SignalType.BUY,
                strength=SignalStrength.STRONG,
                price_level=current_price,
                timestamp=datetime.now(),
                details="RSI indicates oversold"
            ))
        elif rsi >= 70:
            signals.append(TechnicalSignal(
                indicator="RSI",
                signal=SignalType.SELL,
                strength=SignalStrength.STRONG,
                price_level=current_price,
                timestamp=datetime.now(),
                details="RSI indicates overbought"
            ))
        
        # Get news and sentiment
        news = self.get_news_sentiment(ticker)
        
        # Calculate overall sentiment
        sentiment = SentimentAnalysis(
            overall_score=0.7,  # This would be calculated based on all factors
            news_sentiment=sum(n.sentiment_score for n in news) / len(news),
            social_sentiment=None,  # Would require social media API integration
            analyst_sentiment=0.8,  # Would come from analyst recommendations
            technical_sentiment=0.6,  # Based on technical indicators
            sources_analyzed=len(news)
        )
        
        # Determine overall recommendation
        buy_signals = sum(1 for s in signals if s.signal in [SignalType.BUY, SignalType.STRONG_BUY])
        sell_signals = sum(1 for s in signals if s.signal in [SignalType.SELL, SignalType.STRONG_SELL])
        total_signals = len(signals)
        
        if buy_signals > sell_signals and sentiment.overall_score > 0.6:
            overall_recommendation = SignalType.STRONG_BUY
            confidence_score = 0.8
        elif buy_signals > sell_signals:
            overall_recommendation = SignalType.BUY
            confidence_score = 0.6
        elif sell_signals > buy_signals and sentiment.overall_score < 0.4:
            overall_recommendation = SignalType.STRONG_SELL
            confidence_score = 0.8
        elif sell_signals > buy_signals:
            overall_recommendation = SignalType.SELL
            confidence_score = 0.6
        else:
            overall_recommendation = SignalType.HOLD
            confidence_score = 0.5
        
        return TradingSignals(
            timestamp=datetime.now(),
            overall_recommendation=overall_recommendation,
            confidence_score=confidence_score,
            technical_signals=signals,
            bollinger_bands=bollinger,
            macd=macd,
            rsi=float(rsi),
            stochastic={'k': 65.5, 'd': 63.2},  # Would be calculated
            consensus_target=current_price * 1.1,  # Would come from analyst data
            highest_target=current_price * 1.2,
            lowest_target=current_price * 0.9,
            sentiment=sentiment,
            recent_news=news,
            support_levels=levels['support'],
            resistance_levels=levels['resistance'],
            volume_analysis=volume_analysis
        )

    def calculate_rsi(self, data: pd.DataFrame, periods: int = 14) -> float:
        """Calculate Relative Strength Index"""
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return float(rsi.iloc[-1])
