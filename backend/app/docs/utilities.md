# Utilities Guide

The `/utils` directory contains helper functions and classes that provide common functionality across the application. These utilities are designed to be reusable, stateless, and focused on specific tasks.

## Overview

```
utils/
├── logging.py      # Logging configuration and setup
├── output.py       # Output file management and generation
└── technical.py    # Technical analysis calculations
```

## Logging (`logging.py`)

The logging utility provides a centralized logging configuration for the entire application.

### Features:
- Creates a `logs` directory if it doesn't exist
- Configures both file and console logging
- Uses standardized log format with timestamps
- Supports different log levels (INFO, ERROR, etc.)

### Usage:
```python
from app.utils.logging import setup_logging

logger = setup_logging()
logger.info("Starting analysis...")
logger.error("Error occurred", exc_info=True)
```

## Output Management (`output.py`)

The `OutputManager` class handles all file output operations for analysis results.

### Features:
- Manages output directory creation
- Generates timestamped filenames
- Supports multiple output formats:
  - CSV (raw data)
  - PNG (charts)
  - JSON (analysis summaries)
  - Text (human-readable reports)

### Usage:
```python
from app.utils.output import OutputManager

output_mgr = OutputManager(output_dir="analysis_results")
output_files = output_mgr.save_analysis(
    analysis=stock_analysis,
    technical_data=dataframe
)
```

### Output Types:
1. **CSV Files**
   - Raw technical analysis data
   - Historical price information
   - Indicator values

2. **Charts (PNG)**
   - Price charts with indicators
   - Technical analysis visualizations
   - Custom chart configurations

3. **JSON Summaries**
   - Complete analysis results
   - Technical indicators
   - Company information

4. **Text Reports**
   - Human-readable analysis summaries
   - Key findings and recommendations
   - Technical indicator interpretations

## Technical Analysis (`technical.py`)

Contains functions for calculating various technical indicators and performing market analysis.

### Features:
- RSI (Relative Strength Index) calculation
- Moving averages (SMA)
- Dynamic window size handling
- Null value management

### Available Indicators:
1. **RSI (Relative Strength Index)**
   ```python
   rsi = calculate_rsi(data, periods=14)
   ```

2. **Moving Averages**
   - 20-day SMA
   - 50-day SMA
   - 200-day SMA

### Usage:
```python
from app.utils.technical import calculate_technical_indicators

df = calculate_technical_indicators(price_data)
```

## Best Practices

1. **Logging**
   - Use appropriate log levels
   - Include context in log messages
   - Handle exceptions with proper logging

2. **Output Management**
   - Clean up old files periodically
   - Use consistent naming conventions
   - Handle file system errors gracefully

3. **Technical Analysis**
   - Validate input data
   - Handle edge cases (insufficient data)
   - Document assumptions and limitations

## Error Handling

All utilities include proper error handling:

1. **Logging**
   - Creates missing directories
   - Falls back to console logging if file logging fails

2. **Output Management**
   - Creates missing directories
   - Handles file write permissions
   - Manages file naming conflicts

3. **Technical Analysis**
   - Handles insufficient data gracefully
   - Provides null values when calculations aren't possible
   - Validates input data

## Future Improvements

1. **Logging**
   - Add log rotation
   - Configure different log levels per environment
   - Add structured logging support

2. **Output Management**
   - Add support for more output formats
   - Implement file compression
   - Add output file cleanup policies

3. **Technical Analysis**
   - Add more technical indicators
   - Optimize calculations for large datasets
   - Add backtesting utilities

## Contributing

When adding new utilities:
1. Keep functions focused and stateless
2. Add proper documentation and type hints
3. Include error handling
4. Write unit tests
5. Update this documentation
