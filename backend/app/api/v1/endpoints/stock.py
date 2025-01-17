from fastapi import APIRouter, HTTPException, Depends
from typing import Optional

from app.schemas.stock import (
    StockAnalysis,
    AnalysisResult,
    StockSearchResponse
)
from app.schemas.common import HTTPError
from app.services.stock_service import StockService
from app.core.dependencies import get_stock_service

router = APIRouter()

@router.get(
    "/stock/{ticker}",
    response_model=StockAnalysis,
    responses={
        404: {"model": HTTPError},
        400: {"model": HTTPError}
    }
)
async def get_stock_info(
    ticker: str,
    service: StockService = Depends(get_stock_service)
):
    """
    Get basic stock information and current price
    
    Parameters:
        ticker: Stock ticker symbol
        service: Injected StockService instance
        
    Returns:
        StockAnalysis: Current stock information and analysis
        
    Raises:
        404: If stock is not found
        400: For invalid requests
    """
    try:
        return await service.get_stock_info(ticker)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get(
    "/stock/{ticker}/analysis",
    response_model=AnalysisResult,
    responses={
        404: {"model": HTTPError},
        400: {"model": HTTPError}
    }
)
async def analyze_stock(
    ticker: str,
    service: StockService = Depends(get_stock_service)
):
    """
    Get detailed stock analysis including technical indicators
    
    Parameters:
        ticker: Stock ticker symbol
        service: Injected StockService instance
        
    Returns:
        AnalysisResult: Technical analysis results
        
    Raises:
        404: If stock is not found
        400: For invalid requests
    """
    try:
        return await service.analyze_stock(ticker)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get(
    "/stock/search/{query}",
    response_model=StockSearchResponse,
    responses={
        404: {"model": HTTPError},
        400: {"model": HTTPError}
    }
)
async def search_stock(
    query: str,
    service: StockService = Depends(get_stock_service)
):
    """
    Search for a stock by company name or ticker
    
    Parameters:
        query: Company name or ticker to search for
        service: Injected StockService instance
        
    Returns:
        StockSearchResponse: Matched ticker symbol
        
    Raises:
        404: If no matching stock is found
        400: For invalid requests
    """
    try:
        ticker = await service.search_company(query)
        if not ticker:
            raise HTTPException(
                status_code=404,
                detail=f"No stock found matching '{query}'"
            )
        return StockSearchResponse(ticker=ticker)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
