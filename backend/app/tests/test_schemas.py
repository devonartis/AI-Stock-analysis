import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas.service import (
    StockServiceInput,
    MLPriceData,
    MLServiceInput,
    NewsServiceInput,
    AnalysisServiceInput
)

def test_stock_service_input_validation():
    """Test StockServiceInput validation"""
    # Test valid input
    valid_input = StockServiceInput(company_input="AAPL", days=365)
    assert valid_input.company_input == "AAPL"
    assert valid_input.days == 365

    # Test input stripping
    space_input = StockServiceInput(company_input=" AAPL ", days=365)
    assert space_input.company_input == "AAPL"

    # Test invalid inputs
    with pytest.raises(ValidationError) as exc_info:
        StockServiceInput(company_input="", days=365)
    assert "company_input" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        StockServiceInput(company_input="AAPL", days=0)
    assert "days" in str(exc_info.value)

def test_ml_price_data_validation():
    """Test MLPriceData validation"""
    # Test valid input
    valid_data = MLPriceData(
        close=150.25,
        high=152.00,
        low=149.50,
        volume=1000000,
        date=datetime.now()
    )
    assert valid_data.close == 150.25
    assert valid_data.high == 152.00

    # Test optional fields
    minimal_data = MLPriceData(
        close=150.25,
        date=datetime.now()
    )
    assert minimal_data.high is None
    assert minimal_data.volume is None

    # Test invalid inputs
    with pytest.raises(ValidationError) as exc_info:
        MLPriceData(close=-1, date=datetime.now())
    assert "close" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        MLPriceData(close=150.25, high=-1, date=datetime.now())
    assert "high" in str(exc_info.value)

def test_ml_service_input_validation():
    """Test MLServiceInput validation"""
    # Create sample price data
    price_data = [
        MLPriceData(
            close=150.25,
            high=152.00,
            low=149.50,
            volume=1000000,
            date=datetime(2025, 1, i)
        ) for i in range(1, 32)
    ]

    # Test valid input
    valid_input = MLServiceInput(
        historical_prices=price_data,
        news_texts=["Good news", "Bad news"],
        prediction_days=5
    )
    assert len(valid_input.historical_prices) == 31
    assert len(valid_input.news_texts) == 2

    # Test news text stripping
    space_input = MLServiceInput(
        historical_prices=price_data,
        news_texts=[" News 1 ", "  News 2  "],
        prediction_days=5
    )
    assert space_input.news_texts == ["News 1", "News 2"]

    # Test invalid inputs
    with pytest.raises(ValidationError) as exc_info:
        MLServiceInput(
            historical_prices=price_data[:29],  # Less than 30 days
            prediction_days=5
        )
    assert "historical_prices" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        MLServiceInput(
            historical_prices=price_data,
            prediction_days=31  # More than 30 days
        )
    assert "prediction_days" in str(exc_info.value)

def test_news_service_input_validation():
    """Test NewsServiceInput validation"""
    # Test valid input
    valid_input = NewsServiceInput(
        company_name="Apple Inc",
        ticker="AAPL",
        days=7
    )
    assert valid_input.company_name == "Apple Inc"
    assert valid_input.ticker == "AAPL"

    # Test invalid inputs
    with pytest.raises(ValidationError) as exc_info:
        NewsServiceInput(
            company_name="",
            ticker="AAPL",
            days=7
        )
    assert "company_name" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        NewsServiceInput(
            company_name="Apple Inc",
            ticker="TOOLONG",  # More than 5 chars
            days=7
        )
    assert "ticker" in str(exc_info.value)

def test_analysis_service_input_validation():
    """Test AnalysisServiceInput validation"""
    # Test valid input
    valid_data = {
        "close": [150.25, 151.50, 149.75],
        "high": [152.00, 153.25, 151.00],
        "low": [149.50, 150.75, 148.25],
        "volume": [1000000, 1200000, 900000]
    }
    valid_input = AnalysisServiceInput(data=valid_data)
    assert valid_input.data == valid_data

    # Test missing columns
    invalid_data = {
        "close": [150.25, 151.50, 149.75],
        "high": [152.00, 153.25, 151.00]
        # Missing low and volume
    }
    with pytest.raises(ValidationError) as exc_info:
        AnalysisServiceInput(data=invalid_data)
    assert "Missing required columns" in str(exc_info.value)
