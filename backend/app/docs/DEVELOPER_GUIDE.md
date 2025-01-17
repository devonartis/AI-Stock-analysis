# Stock Analysis API Developer Guide

## Introduction
Welcome to the Stock Analysis API developer guide! This document will help you understand the codebase, common pitfalls, and best practices for development. We'll cover important aspects of the system, including recent fixes and what to watch out for when making changes.

## Project Structure
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/  # API route handlers
│   ├── core/              # Core configurations
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic models for validation
│   ├── services/          # Business logic
│   └── utils/             # Utility functions
├── tests/                 # Test suite
└── requirements.txt       # Project dependencies
```

## Key Components

### 1. Schema Validation
The API uses Pydantic for data validation. Pay special attention to:

- **Schema Definitions**: All schemas are in `app/schemas/`. Make sure to:
  - Define all required fields with proper types
  - Use appropriate Field(...) definitions with descriptions
  - Add example values in Config.json_schema_extra
  - Avoid duplicate schema definitions
  - Keep schemas synchronized with their usage in services

Recent Fix: We had issues with schema validation in the stock analysis endpoint due to:
- Missing required fields (MACD, Bollinger Bands)
- Duplicate schema definitions causing conflicts
- Inconsistent field requirements between schema and implementation

### 2. Technical Indicators
Technical indicators are calculated in `app/utils/technical.py`. Important considerations:

- **Data Requirements**:
  - Most indicators need a minimum amount of data points
  - Always handle cases with insufficient data gracefully
  - Use dynamic windows based on available data length

- **Calculation Accuracy**:
  - Validate input data for NaN/null values
  - Handle edge cases (e.g., division by zero in RSI)
  - Return sensible defaults when calculations aren't possible

Recent Improvements:
- Added MACD calculation with customizable periods
- Implemented Bollinger Bands with additional metrics
- Enhanced SMA calculations with dynamic windows
- Added proper error handling for insufficient data

### 3. Stock Service
The StockService (`app/services/stock_service.py`) handles data retrieval and analysis. Key points:

- **Data Fetching**:
  - Handle network errors gracefully
  - Implement retries for transient failures
  - Validate returned data before processing

- **Analysis Pipeline**:
  - Ensure all required fields are calculated
  - Map technical indicators correctly to schema
  - Handle missing or invalid data appropriately

Recent Fixes:
- Added proper mapping of technical indicators to schema
- Implemented price change calculation
- Added validation for company information
- Enhanced error handling in analysis pipeline

## Common Pitfalls and Solutions

1. **Schema Validation Errors**
   ```python
   # Wrong:
   class TechnicalIndicators(BaseModel):
       rsi: float
       
   # Correct:
   class TechnicalIndicators(BaseModel):
       rsi: float = Field(..., description="Relative Strength Index")
       macd: float = Field(..., description="MACD value")
       bollinger_bands: BollingerBands
   ```

2. **Insufficient Data Handling**
   ```python
   # Wrong:
   def calculate_sma(data, window=20):
       return data.rolling(window=window).mean()
       
   # Correct:
   def calculate_sma(data, window=20):
       min_window = min(len(data), window)
       return data.rolling(window=min_window).mean()
   ```

3. **Error Handling**
   ```python
   # Wrong:
   async def analyze_stock(self, ticker: str):
       data = self.get_stock_data(ticker)
       return self.calculate_indicators(data)
       
   # Correct:
   async def analyze_stock(self, ticker: str):
       try:
           data = self.get_stock_data(ticker)
           if data.empty:
               raise StockDataError(f"No data found for {ticker}")
           return self.calculate_indicators(data)
       except Exception as e:
           logger.error(f"Analysis failed: {str(e)}")
           raise AnalysisError(f"Failed to analyze stock: {str(e)}")
   ```

## Best Practices

1. **Data Validation**
   - Always use Pydantic models for data validation
   - Include comprehensive field descriptions
   - Add example values for documentation
   - Keep schemas DRY (Don't Repeat Yourself)

2. **Error Handling**
   - Use custom exception classes for different error types
   - Include meaningful error messages
   - Log errors with appropriate context
   - Handle edge cases gracefully

3. **Code Organization**
   - Keep related functionality together
   - Use clear and consistent naming
   - Add comprehensive docstrings
   - Follow type hints consistently

4. **Testing**
   - Write tests for edge cases
   - Include both success and failure scenarios
   - Mock external services appropriately
   - Maintain high test coverage

## Development Workflow

1. **Making Changes**
   - Create a new branch for features/fixes
   - Update relevant tests
   - Update documentation
   - Add changelog entries

2. **Testing**
   - Run the full test suite
   - Test with different data scenarios
   - Verify error handling
   - Check schema validation

3. **Documentation**
   - Update API documentation
   - Add code comments for complex logic
   - Update the changelog
   - Update this guide if needed

## Future Improvements

1. **Technical Indicators**
   - Add more indicators (ATR, Stochastic, etc.)
   - Enhance error handling
   - Improve performance
   - Add customizable parameters

2. **Validation**
   - Add more comprehensive input validation
   - Enhance error messages
   - Add request/response logging
   - Implement rate limiting

3. **Testing**
   - Increase test coverage
   - Add performance tests
   - Add integration tests
   - Add load testing

## Getting Help

If you encounter issues:
1. Check the error messages and logs
2. Review this guide's common pitfalls
3. Check the test suite for similar scenarios
4. Consult the API documentation
5. Review recent changes in the changelog

Remember: When in doubt, add more validation and error handling!
