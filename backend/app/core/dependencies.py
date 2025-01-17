from app.services.stock_service import StockService
from app.services.analysis_service import AnalysisService
from app.services.ml_service import MLService
from app.core.config import settings

def get_stock_service() -> StockService:
    """Dependency for getting StockService instance"""
    return StockService(output_dir=settings.OUTPUT_DIR)

def get_analysis_service() -> AnalysisService:
    """Dependency for getting AnalysisService instance"""
    return AnalysisService()

def get_ml_service() -> MLService:
    """Dependency for getting MLService instance"""
    return MLService()
