import uuid
import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel, HttpUrl
from typing import Literal
from app.utils.docx_engine import docx_to_pdf, docx_to_text, docx_to_images, DOCXConversionError

router = APIRouter(prefix="/docx-convert", tags=["docx-convert"])


class DOCXConvertRequest(BaseModel):
    url: HttpUrl
    output_format: Literal["pdf", "txt", "images"] = "pdf"
    dpi: int = 150


@router.post("")
async def convert_docx(
    docx_request: DOCXConvertRequest,
    request: Request
):
    try:
        async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
            response = await client.get(str(docx_request.url))
            response.raise_for_status()
    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="Timeout downloading DOCX")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=400, detail=f"Failed to download DOCX: {e.response.status_code}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to download DOCX: {str(e)}")

    docx_bytes = response.content

    try:
        if docx_request.output_format == "pdf":
            pdf_bytes = docx_to_pdf(docx_bytes)
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename={uuid.uuid4().hex[:8]}.pdf"}
            )

        elif docx_request.output_format == "txt":
            text = docx_to_text(docx_bytes)
            return {
                "success": True,
                "source_url": str(docx_request.url),
                "text": text
            }

        elif docx_request.output_format == "images":
            filenames = docx_to_images(docx_bytes, dpi=docx_request.dpi)
            base_url = str(request.base_url).rstrip("/")
            image_urls = [f"{base_url}/api/images/{filename}" for filename in filenames]
            return {
                "success": True,
                "source_url": str(docx_request.url),
                "total_pages": len(filenames),
                "images": image_urls
            }

    except DOCXConversionError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
