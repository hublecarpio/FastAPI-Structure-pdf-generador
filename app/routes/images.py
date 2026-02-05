from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.utils.pdf_to_images import get_image_path

router = APIRouter(prefix="/images", tags=["images"])


@router.get("/{filename}")
async def get_image(filename: str):
    """
    Download a generated image by filename.
    Only allows downloading images with valid naming pattern.
    """
    filepath = get_image_path(filename)
    
    if not filepath:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(
        path=str(filepath),
        media_type="image/png",
        filename=filename
    )
