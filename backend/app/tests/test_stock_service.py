import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime, timedelta
import os

from app.services.stock_service import StockService, StockDataError, AnalysisError
from app.schemas.service import AnalysisResult
from app.schemas.stock import (
    StockAnalysis,
    CompanyInfo,
    TechnicalIndicators,
    BollingerBands,
    StockPrice
)

@pytest.fixture
def stock_service():
    """Fixture for stock service instance"""
    service = StockService(output_dir="test_output")
    # Ensure test output directory exists
    if not os.path.exists("test_output"):
        os.makedirs("test_output")
    return service

@pytest.fixture
def mock_stock_data():
    """Create mock stock data for testing"""
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    data = pd.DataFrame(index=dates)
    # Create price data with some variation for RSI calculation
    data['Close'] = [102 + (i % 4) for i in range(len(dates))]  # Values will oscillate between 102-105
    data['Open'] = data['Close'] - 2
    data['High'] = data['Close'] + 3
    data['Low'] = data['Close'] - 3
    data['Volume'] = 1000000
    return data

@pytest.fixture
def mock_company_info():
    """Create mock company info for testing"""
    return {
        'longName': 'Test Company',
        'industry': 'Software',
        'sector': 'Technology',
        'marketCap': 1000000000,
        'fiftyTwoWeekHigh': 120.0,
        'fiftyTwoWeekLow': 80.0
    }

@pytest.mark.asyncio
async def test_analyze_stock_success(stock_service, mock_stock_data, mock_company_info):
    """Test successful stock analysis"""
    with patch('yfinance.Ticker') as mock_yf:
        # Configure mock
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = mock_stock_data
        mock_ticker.info = mock_company_info
        mock_yf.return_value = mock_ticker

        # Execute analysis
        result = await stock_service.analyze_stock('TEST')

        # Verify result structure
        assert result is not None
        assert hasattr(result, 'analysis')
        assert hasattr(result, 'output_files')
        assert hasattr(result, 'execution_time')
        
        # Verify analysis data
        analysis = result.analysis
        assert isinstance(analysis, StockAnalysis)
        assert analysis.ticker == 'TEST'
        assert analysis.company_name == 'Test Company'
        assert analysis.current_price > 0
        assert isinstance(analysis.technical_indicators, TechnicalIndicators)
        assert isinstance(analysis.technical_indicators.bollinger_bands, BollingerBands)

        # Verify output files
        assert isinstance(result.output_files, dict)
        assert all(key in result.output_files for key in ['csv', 'chart', 'json', 'text'])
        assert all(isinstance(path, str) for path in result.output_files.values())

@pytest.mark.asyncio
async def test_analyze_stock_invalid_ticker(stock_service):
    """Test analysis with invalid ticker"""
    with patch('yfinance.Ticker') as mock_yf:
        mock_yf.return_value.history.return_value = pd.DataFrame()
        with pytest.raises(StockDataError):
            await stock_service.analyze_stock('INVALID')

@pytest.mark.asyncio
async def test_technical_indicators(stock_service, mock_stock_data, mock_company_info):
    """Test technical indicator calculations"""
    with patch('yfinance.Ticker') as mock_yf:
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = mock_stock_data
        mock_ticker.info = mock_company_info
        mock_yf.return_value = mock_ticker
        
        result = await stock_service.analyze_stock('TEST')
        
        ti = result.analysis.technical_indicators
        assert isinstance(ti, TechnicalIndicators)
        assert isinstance(ti.bollinger_bands, BollingerBands)
        
        # Verify technical indicators are within reasonable ranges
        assert 0 <= ti.rsi <= 100  # RSI should be between 0 and 100
        assert -10 <= ti.macd <= 10  # MACD should be within reasonable range
        assert ti.sma_20 > 0  # Moving averages should be positive
        assert ti.sma_50 > 0
        assert ti.sma_200 > 0
        
        # Verify Bollinger Bands
        bb = ti.bollinger_bands
        assert bb.upper > bb.middle > bb.lower  # Upper > Middle > Lower
        assert 0 <= bb.bandwidth <= 1  # Bandwidth should be between 0 and 1
        assert 0 <= bb.percent_b <= 1  # Percent B should be between 0 and 1

@pytest.mark.asyncio
async def test_search_company(stock_service):
    """Test company search functionality"""
    with patch('yfinance.Ticker') as mock_yf:
        mock_yf.return_value.info = {'symbol': 'TEST'}
        result = await stock_service.search_company('Test Company')
        assert result == 'TEST'

@pytest.mark.asyncio
async def test_rate_limit_handling(stock_service):
    """Test handling of rate limit errors"""
    with patch('yfinance.Ticker') as mock_yf:
        mock_yf.return_value.history.side_effect = Exception('Rate limit exceeded')
        with pytest.raises(StockDataError, match='Rate limit exceeded'):
            await stock_service.analyze_stock('TEST')

@pytest.mark.asyncio
async def test_output_file_generation(stock_service, mock_stock_data, mock_company_info):
    """Test generation of output files"""
    with patch('yfinance.Ticker') as mock_yf:
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = mock_stock_data
        mock_ticker.info = mock_company_info
        mock_yf.return_value = mock_ticker
        
        result = await stock_service.analyze_stock('TEST')
        
        # Check output files
        assert os.path.exists(result.output_files['csv'])
        assert os.path.exists(result.output_files['chart'])
        assert os.path.exists(result.output_files['json'])
        assert os.path.exists(result.output_files['text'])
        
        # Clean up test files
        for filepath in result.output_files.values():
            if os.path.exists(filepath):
                os.remove(filepath)

@pytest.mark.asyncio
async def test_comprehensive_analysis(stock_service, mock_stock_data, mock_company_info):
    """Test comprehensive analysis including new features"""
    with patch('yfinance.Ticker') as mock_yf:
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = mock_stock_data
        mock_ticker.info = mock_company_info
        mock_yf.return_value = mock_ticker
        
        result = await stock_service.analyze_stock('TEST')
        
        # Verify comprehensive analysis
        assert isinstance(result.analysis, StockAnalysis)
        assert isinstance(result.analysis.company_info, CompanyInfo)
        assert isinstance(result.analysis.technical_indicators, TechnicalIndicators)
        assert len(result.analysis.historical_prices) > 0
        assert result.analysis.price_statistics['mean'] > 0

@pytest.mark.asyncio
async def test_error_handling(stock_service):
    """Test error handling for various scenarios"""
    # Test invalid days parameter
    with pytest.raises(ValueError, match='Days must be a positive integer'):
        await stock_service.analyze_stock('TEST', days=-1)

    # Test invalid ticker
    with pytest.raises(StockDataError, match='Could not find ticker symbol'):
        await stock_service.analyze_stock('INVALID_TICKER_123')

    # Test empty company input
    with pytest.raises(ValueError, match='Company input must be a non-empty string'):
        await stock_service.analyze_stock('')
