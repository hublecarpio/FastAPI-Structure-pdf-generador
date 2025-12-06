from sqlalchemy.orm import Session
from app.models.renderlog import RenderLog
from app.models.user import User


def get_render_logs(db: Session, owner: User, limit: int = 100) -> list[RenderLog]:
    return db.query(RenderLog).filter(
        RenderLog.owner_id == owner.id
    ).order_by(RenderLog.created_at.desc()).limit(limit).all()


def get_template_logs(db: Session, template_id, owner: User, limit: int = 100) -> list[RenderLog]:
    return db.query(RenderLog).filter(
        RenderLog.template_id == template_id,
        RenderLog.owner_id == owner.id
    ).order_by(RenderLog.created_at.desc()).limit(limit).all()
