from pydantic import BaseModel, Field
from typing import Optional

class CompanyInfo(BaseModel):
    """Company information"""
    name: str = Field(..., description="Company name")
    ticker: str = Field(..., description="Stock ticker symbol")
    sector: Optional[str] = Field(None, description="Company sector")
    industry: Optional[str] = Field(None, description="Company industry")
    market_cap: Optional[float] = Field(None, description="Market capitalization")
    fifty_two_week_high: Optional[float] = Field(None, description="52-week high price")
    fifty_two_week_low: Optional[float] = Field(None, description="52-week low price")

    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "name": "Apple Inc.",
                "ticker": "AAPL",
                "sector": "Technology",
                "industry": "Consumer Electronics",
                "market_cap": 3000000000000,
                "fifty_two_week_high": 182.94,
                "fifty_two_week_low": 124.17
            }
        }
