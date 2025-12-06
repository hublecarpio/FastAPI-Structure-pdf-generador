from pydantic import BaseModel
from datetime import datetime


class APIKeyCreate(BaseModel):
    pass


class APIKeyResponse(BaseModel):
    id: int
    key: str
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class APIKeyListResponse(BaseModel):
    api_keys: list[APIKeyResponse]
    total: int
