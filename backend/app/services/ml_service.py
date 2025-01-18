import numpy as np
import pandas as pd
from typing import Dict, List, Any
import logging
from ..utils.logging import setup_logging
from ..schemas.service import MLServiceInput, MLPriceData
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from datetime import datetime

logger = setup_logging()

class MLServiceError(Exception):
    """Base exception for ML Service errors"""
    pass

class InsufficientDataError(MLServiceError):
    """Raised when there is not enough data for analysis"""
    pass

class ModelError(MLServiceError):
    """Raised when there is an error in model execution"""
    pass

class MLService:
    def __init__(self):
        """Initialize ML service."""
        self.logger = logging.getLogger(__name__)
    
    def _calculate_sma(self, data: np.ndarray, window: int) -> np.ndarray:
        """Calculate Simple Moving Average."""
        return pd.Series(data).rolling(window=window).mean().fillna(0).values
    
    def _calculate_rsi(self, data: np.ndarray, window: int = 14) -> float:
        """Calculate Relative Strength Index."""
        delta = pd.Series(data).diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs.iloc[-1])) if loss.iloc[-1] != 0 else 50
    
    def _detect_technical_patterns(self, df: pd.DataFrame) -> Dict[str, float]:
        """Detect technical patterns using price action."""
        try:
            patterns = {}
            
            # Convert numpy arrays to pandas Series
            close = pd.Series(df['close'])
            high = pd.Series(df['high'])
            low = pd.Series(df['low'])
            
            # Double Bottom Pattern
            if len(df) >= 20:
                local_mins = low.rolling(window=5, center=True).min()
                bottoms = (low == local_mins) & (low.shift(10) == local_mins.shift(10))
                patterns['DOUBLE_BOTTOM'] = float(bottoms.sum() / len(df))
            
            # Head and Shoulders Pattern
            if len(df) >= 30:
                peaks = high.rolling(window=5, center=True).max()
                shoulders = (high == peaks) & (high.shift(15) == peaks.shift(15))
                head = high.rolling(window=15, center=True).max()
                head_pattern = (shoulders.sum() > 0) & (head.max() > peaks.max())
                patterns['HEAD_AND_SHOULDERS'] = float(head_pattern)
            
            # Triangle Pattern
            if len(df) >= 20:
                highs = high.rolling(window=5).max()
                lows = low.rolling(window=5).min()
                converging = (highs.std() < highs.shift(10).std()) & (lows.std() < lows.shift(10).std())
                patterns['TRIANGLE'] = float(converging.mean())
            
            # Channel Pattern
            if len(df) >= 20:
                channel_top = high.rolling(window=20).max()
                channel_bottom = low.rolling(window=20).min()
                channel_width = channel_top - channel_bottom
                channel_stability = 1 - (channel_width.std() / channel_width.mean())
                patterns['CHANNEL'] = float(channel_stability)
            
            return patterns
        except Exception as e:
            self.logger.error(f"Error detecting technical patterns: {str(e)}", exc_info=True)
            return {}
    
    def _detect_market_regime(self, df: pd.DataFrame) -> str:
        """Detect market regime using statistical methods."""
        close = df['close'].values
        returns = np.diff(close) / close[:-1]
        volatility = float(np.std(returns))
        trend = float(np.mean(returns))
        
        # Calculate RSI
        rsi = self._calculate_rsi(close)
        
        if volatility > 0.02:
            if trend > 0 and rsi > 70:
                return 'BULLISH_VOLATILE'
            elif trend < 0 and rsi < 30:
                return 'BEARISH_VOLATILE'
            return 'HIGH_VOLATILITY'
        
        if trend > 0 and rsi > 60:
            return 'BULLISH'
        elif trend < 0 and rsi < 40:
            return 'BEARISH'
        
        return 'NEUTRAL'
    
    def _detect_anomalies(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect trading anomalies using Isolation Forest."""
        features = pd.DataFrame({
            'returns': df['close'].pct_change(),
            'volume_change': df['volume'].pct_change(),
            'high_low_range': (df['high'] - df['low']) / df['close'],
        }).fillna(0)
        
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        anomalies = iso_forest.fit_predict(features)
        
        anomaly_list = []
        for i, is_anomaly in enumerate(anomalies):
            if is_anomaly == -1:  # Anomaly detected
                confidence = float(abs(features.iloc[i].mean()))
                if abs(features.iloc[i]['returns']) > 2 * features['returns'].std():
                    anomaly_type = 'PRICE_JUMP'
                elif abs(features.iloc[i]['volume_change']) > 2 * features['volume_change'].std():
                    anomaly_type = 'VOLUME_SPIKE'
                else:
                    anomaly_type = 'PATTERN_BREAK'
                
                anomaly_list.append({
                    'date': df.iloc[i]['date'].isoformat(),
                    'type': anomaly_type,
                    'confidence': min(confidence, 1.0)
                })
        
        return anomaly_list

    def generate_ml_insights(
        self,
        historical_prices: List[Dict[str, Any]],
        news_texts: List[str]
    ) -> Dict[str, Any]:
        """Generate machine learning insights for stock data using real ML models.
        
        Args:
            historical_prices: List of historical price dictionaries
            news_texts: List of news article texts
        
        Returns:
            Dictionary containing ML insights
        """
        try:
            # Validate inputs using Pydantic
            input_data = MLServiceInput(
                historical_prices=historical_prices,
                news_texts=news_texts
            )
            self.logger.info("Generating ML insights")
            
            # Convert historical prices to DataFrame
            df = pd.DataFrame(historical_prices)
            df.columns = [col.lower() for col in df.columns]
            
            # Prepare data for price prediction
            X = np.arange(len(df)).reshape(-1, 1)
            y = df['close'].values
            
            # Fit linear regression model
            model = LinearRegression()
            model.fit(X, y)
            
            # Generate price predictions
            X_future = np.arange(len(df), len(df) + 5).reshape(-1, 1)
            predictions = model.predict(X_future)
            price_predictions = [float(p) for p in predictions]
            
            # Detect technical patterns
            patterns = self._detect_technical_patterns(df)
            
            # Detect market regime
            regime = self._detect_market_regime(df)
            
            # Detect anomalies
            anomalies = self._detect_anomalies(df)
            
            insights = {
                'price_predictions': price_predictions,
                'technical_patterns': patterns,
                'market_regime': regime,
                'trading_anomalies': anomalies
            }
            
            self.logger.info("ML insights generated successfully")
            return insights
            
        except Exception as e:
            self.logger.error(f"Error generating ML insights: {str(e)}", exc_info=True)
            last_price = float(df['close'].iloc[-1]) if 'df' in locals() else 0.0
            return {
                'price_predictions': [last_price] * 5,
                'technical_patterns': {},
                'market_regime': 'UNKNOWN',
                'trading_anomalies': []
            }
