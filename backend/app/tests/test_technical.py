import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from app.utils.technical import (
    calculate_technical_indicators,
    calculate_macd,
    calculate_bollinger_bands,
    calculate_rsi,
    calculate_volume_ema,
    calculate_on_balance_volume,
    calculate_mfi,
    calculate_adx,
    calculate_cci,
    calculate_stochastic,
    calculate_williams_r,
    calculate_atr,
    calculate_volatility_index,
    calculate_advanced_indicators
)

@pytest.fixture
def sample_data():
    """Generate sample price data for testing"""
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)  # For reproducible tests
    
    # Generate realistic price movements
    returns = np.random.normal(0.0001, 0.02, len(dates))
    price = 100 * np.exp(np.cumsum(returns))
    volume = np.random.randint(1000000, 5000000, len(dates))
    
    return pd.DataFrame({
        'Open': price * (1 + np.random.normal(0, 0.002, len(dates))),
        'High': price * (1 + abs(np.random.normal(0, 0.003, len(dates)))),
        'Low': price * (1 - abs(np.random.normal(0, 0.003, len(dates)))),
        'Close': price,
        'Volume': volume
    }, index=dates)

def test_technical_indicators_calculation(sample_data):
    """Test calculation of basic technical indicators"""
    result = calculate_technical_indicators(sample_data)
    
    # Check if all expected columns are present
    expected_columns = [
        'SMA_20', 'SMA_50', 'SMA_200',
        'RSI', 'MACD',
        'BB_upper', 'BB_middle', 'BB_lower',
        'BB_bandwidth', 'BB_percent_b'
    ]
    for col in expected_columns:
        assert col in result.columns
    
    # Check if values are within expected ranges
    assert 0 <= result['RSI'].iloc[-1] <= 100
    assert not result['SMA_20'].isnull().all()
    assert not result['MACD'].isnull().all()

def test_bollinger_bands(sample_data):
    """Test Bollinger Bands calculation"""
    bb = calculate_bollinger_bands(sample_data['Close'])
    
    assert 'upper' in bb
    assert 'middle' in bb
    assert 'lower' in bb
    assert 'bandwidth' in bb
    assert 'percent_b' in bb
    
    # Test relationships
    assert bb['upper'] > bb['middle']
    assert bb['middle'] > bb['lower']
    assert bb['bandwidth'] >= 0

def test_macd_calculation(sample_data):
    """Test MACD calculation"""
    macd = calculate_macd(sample_data['Close'])
    assert isinstance(macd, float)

def test_volume_indicators(sample_data):
    """Test volume-based indicators"""
    volume_ema = calculate_volume_ema(sample_data['Volume'])
    obv = calculate_on_balance_volume(sample_data)
    mfi = calculate_mfi(sample_data)
    
    assert isinstance(volume_ema, float)
    assert isinstance(obv, float)
    assert 0 <= mfi <= 100

def test_momentum_indicators(sample_data):
    """Test momentum indicators"""
    cci = calculate_cci(sample_data)
    stoch = calculate_stochastic(sample_data)
    williams = calculate_williams_r(sample_data)
    
    assert isinstance(cci, float)
    assert 0 <= stoch <= 100
    assert -100 <= williams <= 0

def test_volatility_indicators(sample_data):
    """Test volatility indicators"""
    atr = calculate_atr(sample_data)
    vix = calculate_volatility_index(sample_data)
    adx = calculate_adx(sample_data)
    
    assert isinstance(atr, float)
    assert isinstance(vix, float)
    assert isinstance(adx, float)
    assert atr > 0
    assert vix > 0
    assert 0 <= adx <= 100

def test_advanced_indicators(sample_data):
    """Test calculation of all advanced indicators"""
    result = calculate_advanced_indicators(sample_data)
    
    expected_indicators = {
        'volume_ema',
        'obv',
        'money_flow_index',
        'adx',
        'cci',
        'stochastic',
        'williams_r',
        'atr',
        'vix'
    }
    
    assert set(result.keys()) == expected_indicators
    assert all(isinstance(v, float) for v in result.values())
    assert 0 <= result['money_flow_index'] <= 100
    assert -100 <= result['williams_r'] <= 0

def test_insufficient_data_handling():
    """Test handling of insufficient data"""
    # Create very small dataset
    small_data = pd.DataFrame({
        'Open': [100, 101],
        'High': [102, 103],
        'Low': [98, 99],
        'Close': [101, 102],
        'Volume': [1000, 1100]
    }, index=pd.date_range(start='2023-01-01', periods=2))
    
    # Should not raise exceptions
    result = calculate_technical_indicators(small_data)
    bb = calculate_bollinger_bands(small_data['Close'])
    macd = calculate_macd(small_data['Close'])
    
    # Check if default values are used
    assert not pd.isna(bb['upper'])
    assert not pd.isna(bb['lower'])
    assert not pd.isna(macd)

def test_edge_cases():
    """Test edge cases and error handling"""
    # Test with zero prices
    zero_data = pd.DataFrame({
        'Open': [0, 0],
        'High': [0, 0],
        'Low': [0, 0],
        'Close': [0, 0],
        'Volume': [0, 0]
    }, index=pd.date_range(start='2023-01-01', periods=2))
    
    # Should not raise exceptions
    result = calculate_technical_indicators(zero_data)
    advanced = calculate_advanced_indicators(zero_data)
    
    # Test with NaN values
    nan_data = pd.DataFrame({
        'Open': [np.nan, 100],
        'High': [np.nan, 102],
        'Low': [np.nan, 98],
        'Close': [np.nan, 101],
        'Volume': [np.nan, 1000]
    }, index=pd.date_range(start='2023-01-01', periods=2))
    
    # Should handle NaN values gracefully
    result = calculate_technical_indicators(nan_data)
    advanced = calculate_advanced_indicators(nan_data)
