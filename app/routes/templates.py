from uuid import UUID
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.template import TemplateResponse, TemplateListResponse
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
async def create(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    html_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_template(db, name, description, html_file, current_user)


@router.get("", response_model=TemplateListResponse)
async def list_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    templates = get_templates(db, current_user)
    return TemplateListResponse(templates=templates, total=len(templates))


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_one(
    template_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_template(db, template_id, current_user)


@router.put("/{template_id}", response_model=TemplateResponse)
async def update(
    template_id: UUID,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    html_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await update_template(db, template_id, current_user, name, description, html_file)


@router.delete("/{template_id}")
async def delete(
    template_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_template(db, template_id, current_user)
    return {"message": "Template deleted successfully"}
