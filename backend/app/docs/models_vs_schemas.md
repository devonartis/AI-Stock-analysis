# Understanding Models vs Schemas in FastAPI

## Overview

In a FastAPI application, we distinguish between two types of data structures: Models and Schemas. While both use Pydantic for data validation, they serve different purposes and are used in different parts of the application.

## Quick Reference

| Aspect           | Models                                | Schemas                               |
|-----------------|---------------------------------------|---------------------------------------|
| Purpose         | Internal business logic               | API communication (DTOs)              |
| Location        | `/app/models/`                        | `/app/schemas/`                       |
| Usage           | Services, Database                    | Request/Response validation           |
| Complexity      | Can be complex                        | Should be simple and focused          |
| Dependencies    | Can have business logic               | Should be pure data structures        |
| Persistence     | May include ORM fields               | No ORM-specific fields                |
| Validation      | Business rules                        | API contract rules                    |

## Detailed Explanation

### Models (`/app/models/`)

Models represent your domain entities and business logic. They are the internal representation of your data and business rules.

#### Characteristics:
1. **Business Logic**
   ```python
   class StockPosition(BaseModel):
       ticker: str
       shares: int
       cost_basis: float

       @property
       def current_value(self) -> float:
           # Business logic to calculate current value
           return self.shares * self.get_current_price()

       def calculate_profit_loss(self) -> float:
           # Complex business logic
           return self.current_value - (self.shares * self.cost_basis)
   ```

2. **Internal Dependencies**
   ```python
   class Portfolio(BaseModel):
       positions: List[StockPosition]
       owner_id: UUID

       def rebalance(self):
           # Complex portfolio rebalancing logic
           pass

       def calculate_total_value(self) -> float:
           return sum(pos.current_value for pos in self.positions)
   ```

3. **Database Integration**
   ```python
   class StockTransaction(BaseModel):
       id: UUID = Field(default_factory=uuid4)
       created_at: datetime = Field(default_factory=datetime.now)
       updated_at: datetime = Field(default_factory=datetime.now)
       
       class Config:
           orm_mode = True
           extra = "allow"
   ```

### Schemas (`/app/schemas/`)

Schemas define how data should be structured for API communication. They are also known as DTOs (Data Transfer Objects).

#### Characteristics:
1. **Pure Data Structures**
   ```python
   class StockPositionResponse(BaseModel):
       ticker: str
       shares: int
       current_value: float
       profit_loss: float

       class Config:
           json_schema_extra = {
               "example": {
                   "ticker": "AAPL",
                   "shares": 100,
                   "current_value": 17500.00,
                   "profit_loss": 2500.00
               }
           }
   ```

2. **Input Validation**
   ```python
   class CreateStockPositionRequest(BaseModel):
       ticker: str = Field(..., min_length=1, max_length=5)
       shares: int = Field(..., gt=0)
       price_per_share: float = Field(..., gt=0)

       class Config:
           json_schema_extra = {
               "example": {
                   "ticker": "AAPL",
                   "shares": 100,
                   "price_per_share": 150.00
               }
           }
   ```

3. **API Documentation**
   ```python
   class PortfolioSummaryResponse(BaseModel):
       total_value: float
       positions: List[StockPositionResponse]
       last_updated: datetime

       class Config:
           json_schema_extra = {
               "example": {
                   "total_value": 100000.00,
                   "positions": [
                       {
                           "ticker": "AAPL",
                           "shares": 100,
                           "current_value": 17500.00,
                           "profit_loss": 2500.00
                       }
                   ],
                   "last_updated": "2025-01-17T17:58:37-05:00"
               }
           }
   ```

## Usage in Practice

### Models in Services
```python
class PortfolioService:
    def __init__(self):
        self.db = Database()

    async def rebalance_portfolio(self, portfolio: Portfolio):
        # Use model's business logic
        portfolio.rebalance()
        await self.db.save(portfolio)
```

### Schemas in API Endpoints
```python
@router.post("/portfolio/positions")
async def add_position(
    position: CreateStockPositionRequest,  # Schema for input validation
    service: PortfolioService = Depends(get_portfolio_service)
) -> StockPositionResponse:  # Schema for response
    # Convert schema to model
    position_model = StockPosition(
        ticker=position.ticker,
        shares=position.shares,
        cost_basis=position.price_per_share
    )
    
    # Use model in service
    result = await service.add_position(position_model)
    
    # Convert model back to schema for response
    return StockPositionResponse(
        ticker=result.ticker,
        shares=result.shares,
        current_value=result.current_value,
        profit_loss=result.calculate_profit_loss()
    )
```

## Best Practices

1. **Keep Schemas Simple**
   - Schemas should only contain data needed for API communication
   - Avoid business logic in schemas
   - Include examples for documentation

2. **Models for Business Logic**
   - Put complex calculations in models
   - Include validation related to business rules
   - Can have dependencies on other models

3. **Clear Separation**
   - Don't expose models directly in API
   - Convert between models and schemas in endpoints
   - Keep database-specific logic in models

4. **Documentation**
   - Use schemas to generate OpenAPI documentation
   - Include examples in schema Config
   - Document validation rules clearly

## Common Pitfalls

1. **Mixing Concerns**
   ```python
   # Bad: Schema with business logic
   class StockPositionSchema(BaseModel):
       def calculate_profit_loss(self):  # Business logic shouldn't be here
           pass

   # Good: Keep schema pure
   class StockPositionSchema(BaseModel):
       profit_loss: float  # Just the data
   ```

2. **Exposing Internal Details**
   ```python
   # Bad: Exposing database fields in schema
   class UserSchema(BaseModel):
       id: UUID
       password_hash: str  # Should not expose this!

   # Good: Only expose what's needed
   class UserResponse(BaseModel):
       id: UUID
       username: str
   ```

3. **Duplicating Logic**
   ```python
   # Bad: Duplicating validation
   class StockPositionSchema(BaseModel):
       def validate_shares(self):  # Don't duplicate model logic
           pass

   # Good: Use model for validation
   class StockPosition(BaseModel):
       def validate_shares(self):  # Keep validation in model
           pass
   ```

## When to Use Which

Use **Models** when:
- Implementing business logic
- Working with databases
- Performing complex calculations
- Handling internal state

Use **Schemas** when:
- Validating API inputs
- Formatting API responses
- Generating API documentation
- Converting between API and internal representations
