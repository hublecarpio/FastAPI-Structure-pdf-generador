from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.apikey import APIKeyResponse, APIKeyListResponse
from app.services.apikey_service import create_api_key, get_api_keys, delete_api_key
from app.models.user import User

router = APIRouter(prefix="/apikeys", tags=["apikeys"])


@router.post("/create", response_model=APIKeyResponse)
async def create_key(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_api_key(db, current_user)


@router.get("", response_model=APIKeyListResponse)
async def list_keys(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    keys = get_api_keys(db, current_user)
    return APIKeyListResponse(api_keys=keys, total=len(keys))


@router.delete("/{api_key_id}")
async def delete_key(
    api_key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_api_key(db, api_key_id, current_user)
    return {"message": "API key deleted successfully"}
