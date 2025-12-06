from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base


class RenderLog(Base):
    __tablename__ = "renderlogs"
    
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(UUID(as_uuid=True), ForeignKey("templates.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    duration_ms = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
