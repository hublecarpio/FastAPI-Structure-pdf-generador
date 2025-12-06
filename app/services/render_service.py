import uuid
import time
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.template import Template
from app.models.user import User
from app.models.renderlog import RenderLog
from app.core.s3 import get_file
from app.core.config import settings
from app.utils.jinja_engine import render_html
from app.utils.pdf_engine import html_to_pdf


def load_template_html(db: Session, template_id: uuid.UUID, owner: User) -> str:
    template = db.query(Template).filter(
        Template.id == template_id,
        Template.owner_id == owner.id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    html_content = get_file(settings.S3_BUCKET, template.s3_path)
    if html_content is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load template file"
        )
    
    return html_content.decode('utf-8')


def render_template(
    db: Session,
    template_id: uuid.UUID,
    data: dict,
    owner: User
) -> bytes:
    start_time = time.time()
    status_result = "success"
    
    try:
        html_template = load_template_html(db, template_id, owner)
        
        rendered_html = render_html(html_template, data)
        
        pdf_bytes = html_to_pdf(rendered_html)
        
        return pdf_bytes
    except Exception as e:
        status_result = "error"
        raise e
    finally:
        duration_ms = int((time.time() - start_time) * 1000)
        
        log_entry = RenderLog(
            template_id=template_id,
            owner_id=owner.id,
            duration_ms=duration_ms,
            status=status_result
        )
        db.add(log_entry)
        db.commit()
