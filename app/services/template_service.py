import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from app.models.template import Template
from app.models.user import User
from app.core.s3 import upload_file, get_file, delete_file
from app.core.config import settings


async def create_template(
    db: Session,
    name: str,
    description: str | None,
    html_file: UploadFile,
    owner: User
) -> Template:
    template_id = uuid.uuid4()
    s3_key = f"templates/{owner.id}/{template_id}.html"
    
    html_content = await html_file.read()
    
    success = upload_file(settings.S3_BUCKET, s3_key, html_content)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload template file"
        )
    
    template = Template(
        id=template_id,
        name=name,
        description=description,
        s3_path=s3_key,
        owner_id=owner.id
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    return template


def get_template(db: Session, template_id: uuid.UUID, owner: User) -> Template:
    template = db.query(Template).filter(
        Template.id == template_id,
        Template.owner_id == owner.id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    return template


def get_templates(db: Session, owner: User) -> list[Template]:
    return db.query(Template).filter(Template.owner_id == owner.id).all()


async def update_template(
    db: Session,
    template_id: uuid.UUID,
    owner: User,
    name: str | None = None,
    description: str | None = None,
    html_file: UploadFile | None = None
) -> Template:
    template = get_template(db, template_id, owner)
    
    if name is not None:
        template.name = name
    if description is not None:
        template.description = description
    
    if html_file:
        html_content = await html_file.read()
        success = upload_file(settings.S3_BUCKET, template.s3_path, html_content)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update template file"
            )
    
    db.commit()
    db.refresh(template)
    return template


def delete_template(db: Session, template_id: uuid.UUID, owner: User) -> bool:
    template = get_template(db, template_id, owner)
    
    delete_file(settings.S3_BUCKET, template.s3_path)
    
    db.delete(template)
    db.commit()
    return True
