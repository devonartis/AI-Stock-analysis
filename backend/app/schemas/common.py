from pydantic import BaseModel, Field

class HTTPError(BaseModel):
    """Standard error response model"""
    detail: str = Field(..., description="Error message")
