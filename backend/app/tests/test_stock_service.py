import pytest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from app.services.stock_service import StockService, StockDataError
from app.schemas.stock import StockAnalysis, AnalysisResult

@pytest.fixture
def stock_service():
    """Fixture for stock service instance"""
    return StockService(output_dir="test_output")

@pytest.fixture
def mock_stock_data():
    """Fixture for mock stock data"""
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    return pd.DataFrame({
        'Open': [100] * len(dates),
        'High': [105] * len(dates),
        'Low': [95] * len(dates),
        'Close': [102] * len(dates),
        'Volume': [1000000] * len(dates)
    }, index=dates)

@pytest.mark.asyncio
async def test_analyze_stock_success(stock_service, mock_stock_data):
    """Test successful stock analysis"""
    with patch('yfinance.Ticker') as mock_yf:
        # Configure mock
        mock_yf.return_value.history.return_value = mock_stock_data
        mock_yf.return_value.info = {
            'longName': 'Test Company',
            'sector': 'Technology',
            'industry': 'Software',
            'marketCap': 1000000000
        }
        
        # Execute analysis
        result = await stock_service.analyze_stock('TEST')
        
        # Verify result structure
        assert isinstance(result, AnalysisResult)
        assert result.analysis.ticker == 'TEST'
        assert result.analysis.company_name == 'Test Company'
        assert isinstance(result.execution_time, float)
        assert all(key in result.output_files for key in ['chart', 'summary', 'technical'])

@pytest.mark.asyncio
async def test_analyze_stock_invalid_ticker(stock_service):
    """Test analysis with invalid ticker"""
    with pytest.raises(StockDataError):
        await stock_service.analyze_stock('')

@pytest.mark.asyncio
async def test_technical_indicators(stock_service, mock_stock_data):
    """Test technical indicator calculations"""
    with patch('yfinance.Ticker') as mock_yf:
        mock_yf.return_value.history.return_value = mock_stock_data
        mock_yf.return_value.info = {
            'longName': 'Test Company',
            'sector': 'Technology'
        }
        
        result = await stock_service.analyze_stock('TEST')
        
        # Verify technical indicators
        indicators = result.analysis.technical_indicators
        assert isinstance(indicators.rsi, float)
        assert isinstance(indicators.macd, float)
        assert isinstance(indicators.bollinger_bands.upper, float)
        assert isinstance(indicators.bollinger_bands.lower, float)

@pytest.mark.asyncio
async def test_search_company(stock_service):
    """Test company search functionality"""
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json = lambda: {
            'quotes': [{'symbol': 'AAPL'}]
        }
        
        result = await stock_service.search_company('Apple')
        assert result == 'AAPL'

@pytest.mark.asyncio
async def test_rate_limit_handling(stock_service):
    """Test handling of rate limit errors"""
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 429
        
        with pytest.raises(StockDataError):
            await stock_service.search_company('Apple')

def test_output_file_generation(stock_service, mock_stock_data):
    """Test generation of output files"""
    with patch('yfinance.Ticker') as mock_yf:
        mock_yf.return_value.history.return_value = mock_stock_data
        mock_yf.return_value.info = {'longName': 'Test Company'}
        
        analysis = StockAnalysis(
            company_info={
                'name': 'Test Company',
                'ticker': 'TEST'
            },
            current_price=100.0,
            technical_indicators={
                'rsi': 50.0,
                'macd': 0.5,
                'bollinger_bands': {
                    'upper': 105.0,
                    'middle': 100.0,
                    'lower': 95.0
                }
            },
            historical_prices=[],
            ticker='TEST',
            company_name='Test Company',
            change_percent=1.0,
            volume=1000000
        )
        
        output_files = stock_service.output_manager.save_analysis(analysis, mock_stock_data)
        assert all(key in output_files for key in ['chart', 'summary', 'technical'])
        assert all(isinstance(path, str) for path in output_files.values())

@pytest.mark.asyncio
async def test_comprehensive_analysis(stock_service, mock_stock_data):
    """Test comprehensive analysis including new features"""
    with patch('yfinance.Ticker') as mock_yf:
        mock_yf.return_value.history.return_value = mock_stock_data
        mock_yf.return_value.info = {
            'longName': 'Test Company',
            'sector': 'Technology'
        }
        
        result = await stock_service.analyze_stock('TEST')
        
        # Verify advanced indicators
        advanced = result.analysis.technical_indicators
        assert isinstance(advanced.sma_20, float)
        assert isinstance(advanced.sma_50, float)
        assert isinstance(advanced.sma_200, float)
        
        # Verify price statistics
        stats = result.analysis.price_statistics
        assert isinstance(stats['mean'], float)
        assert isinstance(stats['std'], float)
        assert isinstance(stats['min'], float)
        assert isinstance(stats['max'], float)

def test_error_handling(stock_service):
    """Test error handling for various scenarios"""
    # Test invalid days parameter
    with pytest.raises(ValueError):
        stock_service.get_stock_data('AAPL', days=-1)
    
    # Test empty ticker
    with pytest.raises(ValueError):
        stock_service.get_stock_data('')
    
    # Test malformed data
    with patch('yfinance.Ticker') as mock_yf:
        mock_yf.return_value.history.return_value = pd.DataFrame()
        with pytest.raises(StockDataError):
            stock_service.get_stock_data('AAPL')
