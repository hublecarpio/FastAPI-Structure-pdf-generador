from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class TemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None


class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TemplateResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    s3_path: str
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class TemplateListResponse(BaseModel):
    templates: list[TemplateResponse]
    total: int
