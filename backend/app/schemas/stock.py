from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from .company import CompanyInfo

class StockPrice(BaseModel):
    """Stock price data for a specific point in time"""
    date: datetime = Field(..., description="Date and time of the price point")
    open: float = Field(..., description="Opening price")
    high: float = Field(..., description="Highest price during the period")
    low: float = Field(..., description="Lowest price during the period")
    close: float = Field(..., description="Closing price")
    volume: int = Field(..., description="Trading volume")

    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "date": "2025-01-17T14:30:00Z",
                "open": 173.85,
                "high": 175.10,
                "low": 173.15,
                "close": 174.50,
                "volume": 12500000
            }
        }

class BollingerBands(BaseModel):
    """Bollinger Bands technical indicator"""
    upper: float = Field(..., description="Upper band")
    middle: float = Field(..., description="Middle band (20-day SMA)")
    lower: float = Field(..., description="Lower band")
    bandwidth: float = Field(..., description="Bandwidth")
    percent_b: float = Field(..., description="Percent B")

    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "upper": 180.50,
                "middle": 175.00,
                "lower": 169.50,
                "bandwidth": 0.0628,
                "percent_b": 0.5
            }
        }

class TechnicalIndicators(BaseModel):
    """Technical analysis indicators"""
    rsi: float = Field(..., description="Relative Strength Index")
    macd: float = Field(..., description="Moving Average Convergence Divergence")
    bollinger_bands: BollingerBands = Field(..., description="Bollinger Bands")
    sma_20: Optional[float] = Field(None, description="20-day Simple Moving Average")
    sma_50: Optional[float] = Field(None, description="50-day Simple Moving Average")
    sma_200: Optional[float] = Field(None, description="200-day Simple Moving Average")

    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "rsi": 65.5,
                "macd": 2.35,
                "bollinger_bands": {
                    "upper": 180.50,
                    "middle": 175.00,
                    "lower": 169.50,
                    "bandwidth": 0.0628,
                    "percent_b": 0.5
                },
                "sma_20": 174.50,
                "sma_50": 170.25,
                "sma_200": 165.75
            }
        }

class StockAnalysis(BaseModel):
    """Complete stock analysis results"""
    company_info: CompanyInfo
    current_price: float = Field(..., description="Current stock price")
    technical_indicators: TechnicalIndicators
    price_statistics: Dict[str, float] = Field(
        ...,
        description="Various price statistics like daily change, volume, etc."
    )
    historical_prices: List[StockPrice]
    analysis_date: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")
    ticker: str = Field(..., description="Stock ticker symbol")
    company_name: str = Field(..., description="Company name")
    change_percent: float = Field(..., description="24-hour price change percentage")
    volume: int = Field(..., description="Trading volume")

    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "current_price": 174.50,
                "price_statistics": {
                    "daily_change": 0.65,
                    "daily_change_percent": 0.37,
                    "average_volume": 12500000
                }
            }
        }

class AnalysisResult(BaseModel):
    """Complete analysis result including file outputs"""
    analysis: StockAnalysis
    output_files: Dict[str, str] = Field(
        ...,
        description="Mapping of output type to file path",
        example={
            "chart": "/output/AAPL_chart_20250117.png",
            "summary": "/output/AAPL_summary_20250117.txt",
            "technical": "/output/AAPL_technical_20250117.json"
        }
    )
    execution_time: float = Field(
        ...,
        description="Analysis execution time in seconds",
        example=1.25
    )

class StockSearchResponse(BaseModel):
    """Response model for stock search endpoint"""
    ticker: str = Field(..., description="Stock ticker symbol", example="AAPL")
