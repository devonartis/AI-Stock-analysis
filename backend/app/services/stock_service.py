import yfinance as yf
import pandas as pd
import mplfinance as mpf
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import time
from aiohttp import ClientSession

from ..schemas.service import StockServiceInput
from ..utils.output import OutputManager
from ..schemas.stock import StockAnalysis, AnalysisResult, CompanyInfo, StockPrice, TechnicalIndicators
from ..utils.technical import calculate_technical_indicators

logger = logging.getLogger(__name__)

class StockDataError(Exception):
    """Raised when there is an error fetching stock data"""
    pass

class AnalysisError(Exception):
    """Raised when there is an error during stock analysis"""
    pass

class NetworkError(StockDataError):
    """Raised when there are network connectivity issues"""
    pass

class InvalidTickerError(StockDataError):
    """Raised when an invalid ticker symbol is provided"""
    pass

class RateLimitError(StockDataError):
    """Raised when API rate limits are exceeded"""
    pass

class StockService:
    def __init__(self, output_dir: Optional[str] = None):
        self.output_manager = OutputManager(output_dir or 'output')
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        
    def get_stock_data(self, ticker: str, days: int = 365) -> pd.DataFrame:
        """
        Fetch historical stock data from Yahoo Finance
        
        Args:
            ticker: Stock ticker symbol
            days: Number of days of historical data to fetch
            
        Returns:
            pd.DataFrame: Historical stock data
            
        Raises:
            StockDataError: If data fetch fails
        """
        try:
            stock = yf.Ticker(ticker)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            data = stock.history(start=start_date, end=end_date)
            if data.empty:
                raise StockDataError(f"No data found for ticker {ticker}")
            return data
        except Exception as e:
            raise StockDataError(f"Failed to fetch stock data: {str(e)}")
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry_error_callback=lambda retry_state: None
    )
    async def search_company(self, query: str) -> Optional[str]:
        """
        Search for a company and return its ticker symbol
        
        Args:
            query: Company name or ticker symbol
            
        Returns:
            Optional[str]: Ticker symbol if found, None otherwise
            
        Raises:
            NetworkError: If there are connection issues
            RateLimitError: If API rate limit is exceeded
            StockDataError: For other API errors
        """
        try:
            # First try exact ticker match
            ticker = query.upper()
            stock = yf.Ticker(ticker)
            info = stock.info
            if info and 'symbol' in info:
                return info['symbol']

            # Then try searching by name
            search_url = f"https://query2.finance.yahoo.com/v1/finance/search"
            params = {
                'q': query,
                'quotesCount': 1,
                'newsCount': 0,
                'listsCount': 0
            }
            
            async with ClientSession() as session:
                async with session.get(search_url, headers=self.headers, params=params) as response:
                    if response.status == 429:
                        raise RateLimitError("Yahoo Finance API rate limit exceeded")
                    elif response.status != 200:
                        raise NetworkError(f"Failed to search company: {response.status}")
                        
                    data = await response.json()
                    if data.get('quotes') and len(data['quotes']) > 0:
                        return data['quotes'][0]['symbol']
                        
                    return None
                    
        except Exception as e:
            raise NetworkError(f"Network error during company search: {str(e)}")
        except Exception as e:
            raise StockDataError(f"Error searching for company: {str(e)}")

    def get_company_info(self, ticker: str) -> CompanyInfo:
        """Get company information"""
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return CompanyInfo(
            name=info.get('longName', ticker),
            ticker=ticker,
            sector=info.get('sector'),
            industry=info.get('industry'),
            market_cap=info.get('marketCap'),
            fifty_two_week_high=info.get('fiftyTwoWeekHigh'),
            fifty_two_week_low=info.get('fiftyTwoWeekLow')
        )
    
    async def get_stock_info(self, ticker: str) -> dict:
        """
        Get basic stock information and current price
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            dict: Stock information including current price and basic metrics
            
        Raises:
            NetworkError: If there are connection issues
            StockDataError: For other API errors
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            if not info:
                raise StockDataError(f"No data found for ticker {ticker}")
                
            # Get the most relevant information
            return {
                "symbol": info.get("symbol"),
                "name": info.get("longName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "current_price": info.get("currentPrice"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("forwardPE"),
                "dividend_yield": info.get("dividendYield"),
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
                "volume": info.get("volume"),
                "avg_volume": info.get("averageVolume")
            }
            
        except Exception as e:
            raise StockDataError(f"Error fetching stock info: {str(e)}")

    async def analyze_stock(self, company_input: str, days: int = 365) -> AnalysisResult:
        """
        Perform comprehensive stock analysis
        
        Args:
            company_input: Company name or ticker symbol
            days: Number of days of historical data to analyze
            
        Returns:
            AnalysisResult object containing analysis and file paths
            
        Raises:
            ValueError: If company/ticker cannot be found or parameters invalid
            StockDataError: If there is an error fetching stock data
            AnalysisError: If there is an error during analysis
            ValidationError: If data fails model validation
        """
        # Validate inputs using Pydantic
        input_data = StockServiceInput(
            company_input=company_input,
            days=days
        )
        # Validate input parameters
        if not isinstance(company_input, str) or not company_input.strip():
            raise ValueError("Company input must be a non-empty string")
        if not isinstance(days, int) or days <= 0:
            raise ValueError("Days must be a positive integer")

        start_time = time.time()
        
        try:
            logger.info(f"Starting analysis for {company_input}")
            # Get ticker symbol
            ticker = company_input if company_input.isupper() and len(company_input) <= 5 else await self.search_company(company_input)
            if not ticker:
                raise ValueError(f"Could not find ticker symbol for {company_input}")
            
            # Get stock data
            try:
                stock_data = self.get_stock_data(ticker, days)
                if stock_data.empty:
                    raise StockDataError(f"No data found for {ticker}")
            except Exception as e:
                raise StockDataError(f"Error fetching data for {ticker}: {str(e)}")
            
            # Calculate technical indicators
            technical_data = calculate_technical_indicators(stock_data)
            
            # Get company information
            company_info = self.get_company_info(ticker)
            
            # Create StockAnalysis object
            analysis = StockAnalysis(
                company_info=company_info,
                current_price=stock_data['Close'].iloc[-1],
                technical_indicators=TechnicalIndicators(
                    sma_20=technical_data['SMA_20'].iloc[-1],
                    sma_50=technical_data['SMA_50'].iloc[-1],
                    sma_200=technical_data['SMA_200'].iloc[-1],
                    rsi=technical_data['RSI'].iloc[-1]
                ),
                price_statistics={
                    'mean': float(stock_data['Close'].mean()),
                    'std': float(stock_data['Close'].std()),
                    'min': float(stock_data['Close'].min()),
                    'max': float(stock_data['Close'].max()),
                    'median': float(stock_data['Close'].median())
                },
                historical_prices=[
                    StockPrice(
                        date=index,
                        open=row['Open'],
                        high=row['High'],
                        low=row['Low'],
                        close=row['Close'],
                        volume=row['Volume']
                    )
                    for index, row in stock_data.iterrows()
                ]
            )
            
            # Save outputs
            output_files = self.output_manager.save_analysis(analysis, technical_data)
            
            return AnalysisResult(
                analysis=analysis,
                output_files=output_files,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"Error analyzing stock: {str(e)}", exc_info=True)
            raise AnalysisError(f"Failed to analyze stock: {str(e)}")
from app.schemas.stock import StockAnalysis, AnalysisResult

class StockService:
    """Service for handling stock-related operations"""
    
    async def get_stock_info(self, ticker: str) -> StockAnalysis:
        """
        Get basic stock information and current price
        
        Parameters:
            ticker: Stock ticker symbol
            
        Returns:
            StockAnalysis: Current stock information and analysis
            
        Raises:
            Exception: If stock is not found or request fails
        """
        # TODO: Implement actual stock data fetching
        # This is a placeholder implementation
        return StockAnalysis(
            ticker=ticker,
            company_name="Example Company",
            current_price=100.00,
            change_percent=1.5,
            volume=1000000
        )

    async def analyze_stock(self, ticker: str) -> AnalysisResult:
        """
        Get detailed stock analysis including technical indicators
        
        Parameters:
            ticker: Stock ticker symbol
            
        Returns:
            AnalysisResult: Technical analysis results
            
        Raises:
            Exception: If analysis fails
        """
        try:
            # Get historical data
            stock_data = self.get_stock_data(ticker)
            if stock_data.empty:
                raise StockDataError(f"No data found for {ticker}")

            # Calculate technical indicators
            close_prices = stock_data['Close']
            
            # Calculate RSI
            delta = close_prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # Calculate Moving Averages
            sma_20 = close_prices.rolling(window=20).mean()
            sma_50 = close_prices.rolling(window=50).mean()
            sma_200 = close_prices.rolling(window=200).mean()
            
            # Calculate MACD
            exp1 = close_prices.ewm(span=12, adjust=False).mean()
            exp2 = close_prices.ewm(span=26, adjust=False).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9, adjust=False).mean()
            
            # Calculate Bollinger Bands
            middle_band = sma_20
            std_dev = close_prices.rolling(window=20).std()
            upper_band = middle_band + (std_dev * 2)
            lower_band = middle_band - (std_dev * 2)
            
            # Get latest values
            current_price = close_prices.iloc[-1]
            current_rsi = rsi.iloc[-1]
            current_macd = macd.iloc[-1]
            current_signal = signal.iloc[-1]
            
            # Generate recommendation
            recommendation = "HOLD"
            if current_rsi > 70:
                recommendation = "SELL"
            elif current_rsi < 30:
                recommendation = "BUY"
            elif current_price > upper_band.iloc[-1]:
                recommendation = "SELL"
            elif current_price < lower_band.iloc[-1]:
                recommendation = "BUY"
            
            return AnalysisResult(
                ticker=ticker,
                recommendation=recommendation,
                indicators={
                    "rsi": float(current_rsi),
                    "sma_20": float(sma_20.iloc[-1]),
                    "sma_50": float(sma_50.iloc[-1]),
                    "sma_200": float(sma_200.iloc[-1]),
                    "macd": float(current_macd),
                    "macd_signal": float(current_signal),
                    "macd_histogram": float(current_macd - current_signal),
                    "bollinger_upper": float(upper_band.iloc[-1]),
                    "bollinger_middle": float(middle_band.iloc[-1]),
                    "bollinger_lower": float(lower_band.iloc[-1])
                }
            )
            
        except Exception as e:
            raise AnalysisError(f"Failed to analyze stock: {str(e)}")

    async def search_company(self, query: str) -> str:
        """
        Search for a company and return its ticker
        
        Parameters:
            query: Search query string
            
        Returns:
            str: Matching ticker symbol
            
        Raises:
            Exception: If search fails
        """
        raise NotImplementedError("Company search not implemented yet")
