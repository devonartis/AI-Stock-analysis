# Endpoint Data Utilization Mapping

## `/api/v1/stock/{ticker}/analysis` Endpoint

### Company Information
| Data Field | Type | Current Usage | Status |
|------------|------|---------------|---------|
| company_name | string | StockCard component | ✅ Used |
| ticker | string | StockCard component | ✅ Used |
| sector | string | StockCard component | ✅ Used |
| industry | string | StockCard component | ✅ Used |
| market_cap | number | StockCard component | ✅ Used |
| fifty_two_week_high | number | StockCard component | ✅ Used |
| fifty_two_week_low | number | StockCard component | ✅ Used |

### Price Data
| Data Field | Type | Current Usage | Status |
|------------|------|---------------|---------|
| current_price | number | StockCard component | ✅ Used |
| volume | number | StockCard component | ✅ Used |

### Technical Indicators
| Data Field | Type | Current Usage | Status |
|------------|------|---------------|---------|
| rsi | number | Not displayed | ❌ Unused |
| macd | number | Not displayed | ❌ Unused |
| sma_20 | number | Not displayed | ❌ Unused |
| sma_50 | number | Not displayed | ❌ Unused |
| sma_200 | number | Not displayed | ❌ Unused |
| bollinger_bands.upper | number | Not displayed | ❌ Unused |
| bollinger_bands.middle | number | Not displayed | ❌ Unused |
| bollinger_bands.lower | number | Not displayed | ❌ Unused |
| bollinger_bands.bandwidth | number | Not displayed | ❌ Unused |
| bollinger_bands.percent_b | number | Not displayed | ❌ Unused |

### Price Statistics
| Data Field | Type | Current Usage | Status |
|------------|------|---------------|---------|
| mean | number | Not displayed | ❌ Unused |
| std | number | Not displayed | ❌ Unused |
| min | number | Not displayed | ❌ Unused |
| max | number | Not displayed | ❌ Unused |
| median | number | Not displayed | ❌ Unused |

### Historical Prices
| Data Field | Type | Current Usage | Status |
|------------|------|---------------|---------|
| date | string | Used only for change calculation | ⚠️ Partial |
| open | number | Not displayed | ❌ Unused |
| high | number | Not displayed | ❌ Unused |
| low | number | Not displayed | ❌ Unused |
| close | number | Used only for change calculation | ⚠️ Partial |
| volume | number | Used for average volume | ⚠️ Partial |

### Output Files
| Data Field | Type | Current Usage | Status |
|------------|------|---------------|---------|
| csv | string | Not used | ❌ Unused |
| chart | string | Not used | ❌ Unused |
| json | string | Not used | ❌ Unused |
| text | string | Not used | ❌ Unused |

## Summary of Gaps

### Critical Gaps
1. Technical Indicators
   - None of the technical indicators are displayed
   - Missing visualization for RSI, MACD, SMAs
   - Bollinger Bands data not utilized

2. Price Statistics
   - Statistical analysis data not shown
   - No summary statistics display

3. Historical Data
   - Price history only used for basic calculations
   - No chart visualization
   - Limited use of OHLC data

4. Output Files
   - No export functionality
   - Pre-generated charts not displayed
   - Data export options not implemented

## Next Steps

### Phase 1: Technical Analysis Display
1. Create TechnicalIndicators component
2. Implement indicator visualizations
3. Add Bollinger Bands display

### Phase 2: Historical Data
1. Implement price history chart
2. Add volume visualization
3. Include technical overlays

### Phase 3: Statistics & Export
1. Add statistical summary component
2. Implement export functionality
3. Enable chart downloads
