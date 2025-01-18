from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class FinancialRatios(BaseModel):
    pe_ratio: Optional[float] = Field(None, description="Price to Earnings Ratio")
    pb_ratio: Optional[float] = Field(None, description="Price to Book Ratio")
    peg_ratio: Optional[float] = Field(None, description="Price/Earnings to Growth Ratio")
    profit_margin: Optional[float] = Field(None, description="Profit Margin")
    operating_margin: Optional[float] = Field(None, description="Operating Margin")
    roe: Optional[float] = Field(None, description="Return on Equity")
    debt_to_equity: Optional[float] = Field(None, description="Debt to Equity Ratio")
    current_ratio: Optional[float] = Field(None, description="Current Ratio")
    quick_ratio: Optional[float] = Field(None, description="Quick Ratio")

class AnalystRecommendation(BaseModel):
    firm: str
    rating: str
    price_target: Optional[float]
    date: datetime

class InsiderTrade(BaseModel):
    insider_name: str
    position: str
    transaction_type: str
    shares: int
    price: float
    date: datetime

class InstitutionalOwnership(BaseModel):
    institution_name: str
    shares_held: int
    value: float
    percentage: float
    change: float
    date_reported: datetime

class DetailedCompanyInfo(BaseModel):
    name: str
    ticker: str
    description: Optional[str]
    sector: Optional[str]
    industry: Optional[str]
    employees: Optional[int]
    headquarters: Optional[str]
    founded: Optional[int]
    ceo: Optional[str]
    website: Optional[str]
    market_cap: Optional[float]
    enterprise_value: Optional[float]
    
    # Financial metrics
    revenue_ttm: Optional[float]
    net_income_ttm: Optional[float]
    eps_ttm: Optional[float]
    dividend_yield: Optional[float]
    
    # Trading info
    fifty_two_week_high: Optional[float]
    fifty_two_week_low: Optional[float]
    avg_volume: Optional[int]
    
    # Detailed analysis
    financial_ratios: Optional[FinancialRatios]
    analyst_recommendations: Optional[List[AnalystRecommendation]]
    insider_trades: Optional[List[InsiderTrade]]
    institutional_ownership: Optional[List[InstitutionalOwnership]]
