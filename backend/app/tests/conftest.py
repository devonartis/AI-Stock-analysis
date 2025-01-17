import pytest
import pandas as pd
from datetime import datetime, timedelta
from app.services.stock_service import StockService

@pytest.fixture(scope="session")
def test_output_dir(tmp_path_factory):
    """Create temporary directory for test outputs"""
    return tmp_path_factory.mktemp("test_output")

@pytest.fixture
def sample_stock_data():
    """Generate sample stock data for testing"""
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    return pd.DataFrame({
        'Open': [100] * len(dates),
        'High': [105] * len(dates),
        'Low': [95] * len(dates),
        'Close': [102] * len(dates),
        'Volume': [1000000] * len(dates)
    }, index=dates)

@pytest.fixture
def mock_company_info():
    """Sample company information"""
    return {
        'longName': 'Test Company',
        'sector': 'Technology',
        'industry': 'Software',
        'marketCap': 1000000000,
        'symbol': 'TEST'
    }
