from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.core.s3 import get_file
from app.core.config import settings
from app.schemas.template import TemplateCreate, TemplateUpdate, TemplateResponse, TemplateListResponse
from app.services.template_service import (
    create_template,
    get_template,
    get_templates,
    update_template,
    delete_template
)
from app.models.user import User

router = APIRouter(prefix="/templates", tags=["templates"])


@router.post("", response_model=TemplateResponse)
def create(
    data: TemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_template(db, data.name, data.content, data.description, current_user)


@router.get("")
def list_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    templates = get_templates(db, current_user)
    return templates


@router.get("/{template_id}")
def get_one(
    template_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    template = get_template(db, template_id, current_user)
    content = get_file(settings.S3_BUCKET, template.s3_path)
    return {
        "id": template.id,
        "name": template.name,
        "description": template.description,
        "s3_path": template.s3_path,
        "owner_id": template.owner_id,
        "created_at": template.created_at,
        "content": content.decode('utf-8') if content else None
    }


@router.put("/{template_id}", response_model=TemplateResponse)
def update(
    template_id: UUID,
    data: TemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_template(db, template_id, current_user, data.name, data.description, data.content)


@router.delete("/{template_id}")
def delete(
    template_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_template(db, template_id, current_user)
    return {"message": "Template deleted successfully"}
