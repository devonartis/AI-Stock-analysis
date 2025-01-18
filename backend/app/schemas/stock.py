from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict
from datetime import datetime
from .company import CompanyInfo

class StockPrice(BaseModel):
    """Stock price data for a specific point in time"""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "date": "2025-01-17T14:30:00Z",
            "open": 173.85,
            "high": 175.10,
            "low": 173.15,
            "close": 174.50,
            "volume": 12500000
        }
    })
    
    date: datetime = Field(description="Date and time of the price point")
    open: float = Field(description="Opening price")
    high: float = Field(description="Highest price during the period")
    low: float = Field(description="Lowest price during the period")
    close: float = Field(description="Closing price")
    volume: int = Field(description="Trading volume")

class BollingerBands(BaseModel):
    """Bollinger Bands technical indicator"""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "upper": 180.50,
            "middle": 175.00,
            "lower": 169.50,
            "bandwidth": 0.0628,
            "percent_b": 0.5
        }
    })
    
    upper: float = Field(description="Upper band")
    middle: float = Field(description="Middle band (20-day SMA)")
    lower: float = Field(description="Lower band")
    bandwidth: float = Field(description="Bandwidth")
    percent_b: float = Field(description="Percent B")

class TechnicalIndicators(BaseModel):
    """Technical analysis indicators"""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "rsi": 65.5,
            "macd": 2.35,
            "sma_20": 175.50,
            "sma_50": 172.25,
            "sma_200": 168.75,
            "bollinger_bands": {
                "upper": 180.50,
                "middle": 175.00,
                "lower": 169.50,
                "bandwidth": 0.0628,
                "percent_b": 0.5
            }
        }
    })
    
    rsi: float = Field(description="Relative Strength Index")
    macd: float = Field(description="Moving Average Convergence Divergence")
    sma_20: float = Field(description="20-day Simple Moving Average")
    sma_50: float = Field(description="50-day Simple Moving Average")
    sma_200: float = Field(description="200-day Simple Moving Average")
    bollinger_bands: BollingerBands = Field(description="Bollinger Bands indicators")

class StockAnalysis(BaseModel):
    """Complete stock analysis results"""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "company_info": {
                "name": "Apple Inc.",
                "ticker": "AAPL",
                "sector": "Technology",
                "industry": "Consumer Electronics",
                "market_cap": 2850000000000
            },
            "current_price": 174.50,
            "technical_indicators": {
                "rsi": 65.5,
                "macd": 2.35,
                "sma_20": 175.50,
                "sma_50": 172.25,
                "sma_200": 168.75,
                "bollinger_bands": {
                    "upper": 180.50,
                    "middle": 175.00,
                    "lower": 169.50,
                    "bandwidth": 0.0628,
                    "percent_b": 0.5
                }
            },
            "price_statistics": {
                "daily_change": 0.65,
                "daily_change_percent": 0.37,
                "average_volume": 12500000
            }
        }
    })
    
    company_info: CompanyInfo = Field(description="Company information")
    current_price: float = Field(description="Current stock price")
    technical_indicators: TechnicalIndicators = Field(description="Technical analysis indicators")
    price_statistics: Dict[str, float] = Field(description="Various price statistics like daily change, volume, etc.")
    historical_prices: List[StockPrice] = Field(description="Historical price data")
    analysis_date: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")
    ticker: str = Field(description="Stock ticker symbol")
    company_name: str = Field(description="Company name")
    change_percent: float = Field(description="24-hour price change percentage")
    volume: int = Field(description="Trading volume")

class AnalysisResult(BaseModel):
    """Complete analysis result including file outputs"""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "analysis": {
                "company_info": {
                    "name": "Apple Inc.",
                    "ticker": "AAPL",
                    "sector": "Technology",
                    "industry": "Consumer Electronics",
                    "market_cap": 2850000000000
                },
                "current_price": 174.50,
                "technical_indicators": {
                    "rsi": 65.5,
                    "macd": 2.35,
                    "sma_20": 175.50,
                    "sma_50": 172.25,
                    "sma_200": 168.75,
                    "bollinger_bands": {
                        "upper": 180.50,
                        "middle": 175.00,
                        "lower": 169.50,
                        "bandwidth": 0.0628,
                        "percent_b": 0.5
                    }
                },
                "price_statistics": {
                    "daily_change": 0.65,
                    "daily_change_percent": 0.37,
                    "average_volume": 12500000
                }
            },
            "output_files": {
                "chart": "/output/AAPL_chart_20250117.png",
                "summary": "/output/AAPL_summary_20250117.txt",
                "technical": "/output/AAPL_technical_20250117.json"
            },
            "execution_time": 1.25
        }
    })
    
    analysis: StockAnalysis = Field(description="Stock analysis results")
    output_files: Dict[str, str] = Field(description="Mapping of output type to file path")
    execution_time: float = Field(description="Analysis execution time in seconds")

class StockSearchResponse(BaseModel):
    """Response model for stock search endpoint"""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "ticker": "AAPL"
        }
    })
    
    ticker: str = Field(description="Stock ticker symbol")
