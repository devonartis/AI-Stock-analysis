from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class SignalType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    STRONG_BUY = "STRONG_BUY"
    STRONG_SELL = "STRONG_SELL"

class SignalStrength(str, Enum):
    WEAK = "WEAK"
    MODERATE = "MODERATE"
    STRONG = "STRONG"

class TechnicalSignal(BaseModel):
    indicator: str = Field(..., min_length=1)
    signal: SignalType
    strength: SignalStrength
    price_level: float = Field(..., gt=0)
    timestamp: datetime
    details: Optional[str] = Field(None, max_length=1000)

    @validator('timestamp')
    def validate_timestamp(cls, v):
        if v > datetime.now():
            raise ValueError("Timestamp cannot be in the future")
        return v

class BollingerBands(BaseModel):
    upper: float
    middle: float
    lower: float
    bandwidth: float
    percent_b: float

class MACD(BaseModel):
    macd_line: float
    signal_line: float
    histogram: float
    crossover_signal: Optional[SignalType]

class NewsArticle(BaseModel):
    title: str
    source: str
    url: str
    published_date: datetime
    description: Optional[str] = None
    sentiment_score: float  # -1 to 1
    subjectivity_score: Optional[float] = None
    summary: str

class SentimentAnalysis(BaseModel):
    overall_score: float = Field(..., ge=-1, le=1)
    news_sentiment: float = Field(..., ge=-1, le=1)
    social_sentiment: Optional[float] = Field(None, ge=-1, le=1)
    analyst_sentiment: float = Field(..., ge=-1, le=1)
    technical_sentiment: float = Field(..., ge=-1, le=1)
    sources_analyzed: int = Field(..., gt=0)

    @validator('social_sentiment')
    def validate_social_sentiment(cls, v):
        if v is not None and not -1 <= v <= 1:
            raise ValueError("Social sentiment must be between -1 and 1")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "overall_score": 0.75,
                "news_sentiment": 0.8,
                "social_sentiment": 0.7,
                "analyst_sentiment": 0.9,
                "technical_sentiment": 0.6,
                "sources_analyzed": 125
            }
        }

class TradingSignals(BaseModel):
    timestamp: datetime
    overall_recommendation: SignalType
    confidence_score: float  # 0 to 1
    
    # Technical Analysis
    technical_signals: List[TechnicalSignal]
    bollinger_bands: BollingerBands
    macd: MACD
    rsi: float
    stochastic: Dict[str, float]
    
    # Price Targets
    consensus_target: Optional[float]
    highest_target: Optional[float]
    lowest_target: Optional[float]
    
    # Sentiment
    sentiment: SentimentAnalysis
    recent_news: List[NewsArticle]
    
    # Support and Resistance
    support_levels: List[float]
    resistance_levels: List[float]
    
    # Volume Analysis
    volume_analysis: Dict[str, float]
    
    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2025-01-16T19:17:58-05:00",
                "overall_recommendation": "BUY",
                "confidence_score": 0.85,
                "technical_signals": [
                    {
                        "indicator": "MACD",
                        "signal": "BUY",
                        "strength": "STRONG",
                        "price_level": 150.25,
                        "timestamp": "2025-01-16T19:17:58-05:00",
                        "details": "MACD line crossed above signal line"
                    }
                ]
            }
        }
