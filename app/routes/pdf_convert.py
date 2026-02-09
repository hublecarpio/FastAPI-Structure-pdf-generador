import httpx
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, HttpUrl
from app.utils.pdf_to_images import pdf_to_images, PDFConversionError

router = APIRouter(prefix="/pdf-to-images", tags=["pdf-convert"])


class PDFConvertRequest(BaseModel):
    url: HttpUrl
    dpi: int = 150


@router.post("")
async def convert_pdf_to_images(
    pdf_request: PDFConvertRequest,
    request: Request
):
    """
    Download a PDF from URL and convert each page to PNG images.
    Returns URLs to download each page.
    
    Request body:
    - url: URL of the PDF to convert
    - dpi: Resolution for images (default: 150)
    """
    try:
        async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
            response = await client.get(str(pdf_request.url))
            response.raise_for_status()
    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="Timeout downloading PDF")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=400, detail=f"Failed to download PDF: {e.response.status_code}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to download PDF: {str(e)}")
    
    content_type = response.headers.get("content-type", "")
    url_path = pdf_request.url.path or ""
    if "application/pdf" not in content_type and not url_path.endswith(".pdf"):
        if not response.content[:4] == b"%PDF":
            raise HTTPException(status_code=400, detail="URL does not point to a valid PDF file")
    
    pdf_bytes = response.content
    
    try:
        filenames = pdf_to_images(pdf_bytes, dpi=pdf_request.dpi)
    except PDFConversionError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    base_url = str(request.base_url).rstrip("/")
    image_urls = [f"{base_url}/api/images/{filename}" for filename in filenames]
    
    return {
        "success": True,
        "source_url": str(pdf_request.url),
        "total_pages": len(filenames),
        "images": image_urls
    }
