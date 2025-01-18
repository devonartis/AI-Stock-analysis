import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

def calculate_rsi(data: pd.DataFrame, periods: int = 14) -> pd.Series:
    """Calculate Relative Strength Index"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data: pd.Series, fast_period: int = 12, slow_period: int = 26) -> float:
    """Calculate Moving Average Convergence Divergence"""
    min_period = min(len(data), max(fast_period, slow_period))
    if min_period < fast_period:
        return 0.0
    exp1 = data.ewm(span=fast_period, adjust=False).mean()
    exp2 = data.ewm(span=slow_period, adjust=False).mean()
    macd = exp1 - exp2
    return macd.iloc[-1]

def calculate_bollinger_bands(data: pd.Series, window: int = 20, num_std: float = 2) -> Dict[str, float]:
    """Calculate Bollinger Bands"""
    min_window = min(len(data), window)
    if min_window < 2:  # Need at least 2 points for standard deviation
        return {
            "upper": data.iloc[-1],
            "middle": data.iloc[-1],
            "lower": data.iloc[-1],
            "bandwidth": 0.0,
            "percent_b": 0.5
        }
    
    middle = data.rolling(window=min_window).mean()
    std = data.rolling(window=min_window).std()
    upper = middle + (std * num_std)
    lower = middle - (std * num_std)
    
    # Calculate additional Bollinger Band metrics
    bandwidth = (upper - lower) / middle
    percent_b = (data - lower) / (upper - lower)
    
    return {
        "upper": float(upper.iloc[-1]),
        "middle": float(middle.iloc[-1]),
        "lower": float(lower.iloc[-1]),
        "bandwidth": float(bandwidth.iloc[-1]),
        "percent_b": float(percent_b.iloc[-1])
    }

def calculate_volume_ema(volume: pd.Series, period: int = 20) -> float:
    """Calculate Volume Exponential Moving Average"""
    return float(volume.ewm(span=period, adjust=False).mean().iloc[-1])

def calculate_on_balance_volume(data: pd.DataFrame) -> float:
    """Calculate On Balance Volume"""
    obv = (np.sign(data['Close'].diff()) * data['Volume']).cumsum()
    return float(obv.iloc[-1])

def calculate_mfi(data: pd.DataFrame, period: int = 14) -> float:
    """Calculate Money Flow Index"""
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    money_flow = typical_price * data['Volume']
    positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0).rolling(period).sum()
    negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0).rolling(period).sum()
    money_ratio = positive_flow / negative_flow
    return float(100 - (100 / (1 + money_ratio.iloc[-1])))

def calculate_adx(data: pd.DataFrame, period: int = 14) -> float:
    """Calculate Average Directional Index"""
    tr1 = data['High'] - data['Low']
    tr2 = abs(data['High'] - data['Close'].shift(1))
    tr3 = abs(data['Low'] - data['Close'].shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()
    return float(atr.iloc[-1])

def calculate_cci(data: pd.DataFrame, period: int = 20) -> float:
    """Calculate Commodity Channel Index"""
    tp = (data['High'] + data['Low'] + data['Close']) / 3
    sma_tp = tp.rolling(period).mean()
    # Use abs().mean() instead of mad() since mad() is not available in newer pandas versions
    mad = tp.rolling(period).apply(lambda x: abs(x - x.mean()).mean())
    cci = (tp - sma_tp) / (0.015 * mad)
    return float(cci.iloc[-1])

def calculate_stochastic(data: pd.DataFrame, period: int = 14) -> float:
    """Calculate Stochastic Oscillator"""
    low_min = data['Low'].rolling(period).min()
    high_max = data['High'].rolling(period).max()
    k = 100 * (data['Close'] - low_min) / (high_max - low_min)
    return float(k.iloc[-1])

def calculate_williams_r(data: pd.DataFrame, period: int = 14) -> float:
    """Calculate Williams %R"""
    high = data['High'].rolling(period).max()
    low = data['Low'].rolling(period).min()
    wr = -100 * (high - data['Close']) / (high - low)
    return float(wr.iloc[-1])

def calculate_atr(data: pd.DataFrame, period: int = 14) -> float:
    """Calculate Average True Range"""
    high_low = data['High'] - data['Low']
    high_close = abs(data['High'] - data['Close'].shift(1))
    low_close = abs(data['Low'] - data['Close'].shift(1))
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    return float(true_range.rolling(period).mean().iloc[-1])

def calculate_volatility_index(data: pd.DataFrame, period: int = 20) -> float:
    """Calculate Volatility Index (simplified)"""
    log_return = np.log(data['Close'] / data['Close'].shift(1))
    return float(log_return.std() * np.sqrt(252) * 100)

def calculate_advanced_indicators(data: pd.DataFrame) -> Dict[str, float]:
    """Calculate additional technical indicators"""
    return {
        'volume_ema': calculate_volume_ema(data['Volume']),
        'obv': calculate_on_balance_volume(data),
        'money_flow_index': calculate_mfi(data),
        'adx': calculate_adx(data),
        'cci': calculate_cci(data),
        'stochastic': calculate_stochastic(data),
        'williams_r': calculate_williams_r(data),
        'atr': calculate_atr(data),
        'vix': calculate_volatility_index(data)
    }

def calculate_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate all technical indicators"""
    df = data.copy()
    
    # Calculate moving averages with dynamic windows
    windows = [20, 50, 200]
    for window in windows:
        min_window = min(len(df), window)  # Use available data length if less than window size
        df[f'SMA_{window}'] = df['Close'].rolling(window=min_window).mean()
    
    # Calculate RSI with minimum window
    min_rsi_window = min(len(df)-1, 14)  # Need at least 2 points for RSI
    if min_rsi_window > 1:  # Only calculate if we have enough data
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=min_rsi_window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=min_rsi_window).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
    else:
        df['RSI'] = None
    
    # Calculate MACD
    df['MACD'] = calculate_macd(df['Close'])
    
    # Calculate Bollinger Bands
    bb = calculate_bollinger_bands(df['Close'])
    df['BB_upper'] = bb['upper']
    df['BB_middle'] = bb['middle']
    df['BB_lower'] = bb['lower']
    df['BB_bandwidth'] = bb['bandwidth']
    df['BB_percent_b'] = bb['percent_b']
    
    return df
