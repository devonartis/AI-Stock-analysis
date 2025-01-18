# Stock Analysis API Documentation

## Base URL
All endpoints are prefixed with `/api/v1`

## OpenAPI Documentation
- Swagger UI: `/api/v1/docs`
- ReDoc: `/api/v1/redoc`
- OpenAPI JSON: `/api/v1/openapi.json`

## Models

### CompanyInfo
```python
class CompanyInfo(BaseModel):
    name: str
    ticker: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
```

### TechnicalIndicators
```python
class TechnicalIndicators(BaseModel):
    rsi: float
    macd: float
    bollinger_bands: Dict[str, float] = Field(description="Mapping of bollinger band type to value")
```

### StockPrice
```python
class StockPrice(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float
```

### StockAnalysis
```python
class StockAnalysis(BaseModel):
    company_info: CompanyInfo
    current_price: float
    technical_indicators: TechnicalIndicators
    price_statistics: Dict[str, float]
    historical_prices: List[StockPrice]
    analysis_date: datetime = Field(default_factory=datetime.now)
```

### AnalysisResult
```python
class AnalysisResult(BaseModel):
    analysis: StockAnalysis
    output_files: Dict[str, str] = Field(description="Mapping of output type to file path")
    execution_time: float = Field(description="Analysis execution time in seconds")
```

### StockSearchResponse
```python
class StockSearchResponse(BaseModel):
    ticker: str
```

### HTTPError
```python
class HTTPError(BaseModel):
    detail: str
```

## Endpoints

### Get Stock Information
```http
GET /api/v1/stocks/{ticker}
```
Get basic stock information and current price for a given ticker.

**Parameters:**
- `ticker` (path): Stock ticker symbol

**Response Schema:** `StockAnalysis`

### Analyze Stock
```http
GET /api/v1/stocks/{ticker}/analysis
```
Perform comprehensive stock analysis including technical indicators, price statistics, and historical data.

**Parameters:**
- `ticker` (path): Stock ticker symbol
- `days` (query, optional): Number of days of historical data to analyze (default: 365)

**Response Schema:** `AnalysisResult`

### Search Stock
```http
GET /api/v1/stocks/search/{query}
```
Search for a stock by company name or ticker symbol.

**Parameters:**
- `query` (path): Company name or ticker to search for

**Response Schema:** `StockSearchResponse`

## Error Responses

All error responses follow this schema:
```python
HTTPError
```

### 404 Not Found
```python
HTTPError(detail="Company not found")
```

### 400 Bad Request
```python
HTTPError(detail="Error message describing the issue")
```

### 500 Internal Server Error
```python
HTTPError(detail="Internal server error")
```

## Rate Limiting
- Default rate: 100 requests per minute
- Burst rate: 200 requests
- Headers returned:
  - `X-RateLimit-Limit`: Maximum requests per minute
  - `X-RateLimit-Remaining`: Remaining requests in current window
  - `X-RateLimit-Reset`: Time until rate limit resets (seconds)
