import secrets
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.apikey import APIKey
from app.models.user import User


def create_api_key(db: Session, owner: User) -> APIKey:
    key = secrets.token_hex(32)
    
    api_key = APIKey(key=key, owner_id=owner.id)
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return api_key


def get_api_keys(db: Session, owner: User) -> list[APIKey]:
    return db.query(APIKey).filter(APIKey.owner_id == owner.id).all()


def validate_api_key(db: Session, key: str) -> APIKey | None:
    return db.query(APIKey).filter(APIKey.key == key).first()


def delete_api_key(db: Session, api_key_id: int, owner: User) -> bool:
    api_key = db.query(APIKey).filter(
        APIKey.id == api_key_id,
        APIKey.owner_id == owner.id
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    db.delete(api_key)
    db.commit()
    return True
