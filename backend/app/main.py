from fastapi import FastAPI
from app.api.v1.endpoints import company, stock, analysis

app = FastAPI(
    title="Your Stock Analysis API",
    description="API for stock analysis and company information",
    version="1.0.0"
)

# Include routers
app.include_router(company.router, prefix="/api/v1", tags=["companies"])
app.include_router(stock.router, prefix="/api/v1", tags=["stocks"])
app.include_router(analysis.router, prefix="/api/v1", tags=["analysis"])
