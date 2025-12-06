from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO
from app.core.database import get_db
from app.core.security import get_current_user_or_api_key
from app.schemas.render import RenderRequest
from app.services.render_service import render_template
from app.models.user import User

router = APIRouter(prefix="/render", tags=["render"])


@router.post("/{template_id}")
async def render_pdf(
    template_id: UUID,
    render_request: RenderRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_or_api_key)
):
    pdf_bytes = render_template(db, template_id, render_request.data, current_user)
    
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=rendered_{template_id}.pdf"
        }
    )
