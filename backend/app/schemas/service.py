from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict

class StockServiceInput(BaseModel):
    """Input model for stock service operations"""
    company_input: str = Field(..., min_length=1, description="Company name or ticker symbol")
    days: int = Field(default=365, gt=0, description="Number of days of historical data")
    
    @field_validator('company_input')
    @classmethod
    def validate_company_input(cls, v: str) -> str:
        if v.strip() == '':
            raise ValueError('Company input cannot be empty')
        return v.strip()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "company_input": "AAPL",
                "days": 365
            }
        }
    )

class MLPriceData(BaseModel):
    """Price data point for ML analysis"""
    close: float = Field(..., gt=0, description="Closing price")
    high: Optional[float] = Field(None, gt=0, description="High price")
    low: Optional[float] = Field(None, gt=0, description="Low price")
    volume: Optional[int] = Field(None, ge=0, description="Trading volume")
    date: datetime = Field(..., description="Date of the price data")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "close": 150.25,
                "high": 152.00,
                "low": 149.50,
                "volume": 1000000,
                "date": "2025-01-17T14:30:00Z"
            }
        }
    )

class MLServiceInput(BaseModel):
    """Input model for ML service predictions"""
    historical_prices: List[MLPriceData] = Field(
        ..., 
        min_length=30,
        description="List of historical price data points"
    )
    news_texts: List[str] = Field(
        default_factory=list,
        description="List of news article texts for sentiment analysis"
    )
    prediction_days: int = Field(
        default=5, 
        ge=1, 
        le=30,
        description="Number of days to predict into the future"
    )

    @field_validator('historical_prices')
    @classmethod
    def validate_prices(cls, v: List[MLPriceData]) -> List[MLPriceData]:
        if not v:
            raise ValueError("Historical prices cannot be empty")
        return sorted(v, key=lambda x: x.date)

    @field_validator('news_texts')
    @classmethod
    def validate_news(cls, v: List[str]) -> List[str]:
        return [text.strip() for text in v if text.strip()]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "historical_prices": [
                    {
                        "close": 150.25,
                        "high": 152.00,
                        "low": 149.50,
                        "volume": 1000000,
                        "date": "2025-01-17T14:30:00Z"
                    }
                ],
                "news_texts": [
                    "Apple announces new iPhone",
                    "Tech stocks rally on strong earnings"
                ],
                "prediction_days": 5
            }
        }
    )

class NewsServiceInput(BaseModel):
    """Input model for news service operations"""
    company_name: str = Field(..., min_length=1, description="Company name")
    ticker: str = Field(..., min_length=1, max_length=5, description="Stock ticker symbol")
    days: int = Field(default=7, gt=0, description="Number of days of news to fetch")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "company_name": "Apple Inc",
                "ticker": "AAPL",
                "days": 7
            }
        }
    )

class AnalysisServiceInput(BaseModel):
    """Input model for technical analysis service"""
    data: Dict = Field(..., description="DataFrame information for analysis")

    @model_validator(mode='after')
    def validate_data(self) -> 'AnalysisServiceInput':
        required_columns = {'close', 'high', 'low', 'volume'}
        data_columns = set(self.data.keys())
        if not required_columns.issubset(data_columns):
            raise ValueError(f"Missing required columns: {required_columns - data_columns}")
        return self

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "data": {
                    "close": [150.25, 151.50, 149.75],
                    "high": [152.00, 153.25, 151.00],
                    "low": [149.50, 150.75, 148.25],
                    "volume": [1000000, 1200000, 900000]
                }
            }
        }
    )

class AnalysisResult(BaseModel):
    """Result of stock analysis including execution time and output files"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    analysis: Dict  # Assuming StockAnalysis is a dictionary
    execution_time: float
    output_files: Dict[str, str]  # Maps output type to file path
