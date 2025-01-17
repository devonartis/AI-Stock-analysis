from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_app_settings():
    """Test if the application settings are correct"""
    assert app.title == settings.APP_NAME
    assert app.openapi_url == f"{settings.API_V1_STR}/openapi.json"
    assert app.docs_url == f"{settings.API_V1_STR}/docs"
    assert app.redoc_url == f"{settings.API_V1_STR}/redoc"
