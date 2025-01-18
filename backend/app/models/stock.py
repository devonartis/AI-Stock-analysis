from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class StockPrice(BaseModel):
    """Stock price data for a specific point in time"""
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

class BollingerBands(BaseModel):
    """Bollinger Bands technical indicator"""
    upper: float = Field(..., description="Upper band")
    middle: float = Field(..., description="Middle band (20-day SMA)")
    lower: float = Field(..., description="Lower band")
    bandwidth: float = Field(..., description="Bandwidth")
    percent_b: float = Field(..., description="Percent B")
    
class TechnicalIndicators(BaseModel):
    """Technical analysis indicators"""
    rsi: float = Field(..., description="Relative Strength Index")
    macd: float = Field(..., description="Moving Average Convergence Divergence")
    bollinger_bands: BollingerBands = Field(..., description="Bollinger Bands")
    sma_20: Optional[float] = Field(None, description="20-day Simple Moving Average")
    sma_50: Optional[float] = Field(None, description="50-day Simple Moving Average")
    sma_200: Optional[float] = Field(None, description="200-day Simple Moving Average")

class CompanyInfo(BaseModel):
    """Company information"""
    name: str
    ticker: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    
class StockAnalysis(BaseModel):
    """Complete stock analysis results"""
    company_info: CompanyInfo
    current_price: float
    technical_indicators: TechnicalIndicators
    price_statistics: Dict[str, float] = Field(..., description="Various price statistics like daily change, volume, etc.")
    historical_prices: List[StockPrice]
    analysis_date: datetime = Field(default_factory=datetime.now)
    
class AnalysisResult(BaseModel):
    """Complete analysis result including file outputs"""
    analysis: StockAnalysis
    output_files: Dict[str, str] = Field(description="Mapping of output type to file path")
    execution_time: float = Field(description="Analysis execution time in seconds")

class StockSearchResponse(BaseModel):
    """Response model for stock search endpoint"""
    ticker: str = Field(..., description="Stock ticker symbol")

class HTTPError(BaseModel):
    """Standard error response model"""
    detail: str = Field(..., description="Error message")
