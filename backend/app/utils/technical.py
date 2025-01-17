import pandas as pd
from typing import Dict, Any

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
