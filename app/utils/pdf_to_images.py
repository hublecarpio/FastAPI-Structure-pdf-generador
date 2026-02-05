import re
import uuid
import logging
from pathlib import Path
from pdf2image import convert_from_bytes
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError
from typing import List

logger = logging.getLogger(__name__)

IMAGES_DIR = Path("generated_images")
IMAGES_DIR.mkdir(exist_ok=True)

VALID_FILENAME_PATTERN = re.compile(r'^[a-f0-9]{8}_page_\d+\.png$')


class PDFConversionError(Exception):
    """Exception raised when PDF conversion fails."""
    pass


def pdf_to_images(pdf_bytes: bytes, dpi: int = 150, format: str = "PNG") -> List[str]:
    """
    Convert PDF bytes to images and save them to disk.
    Returns list of filenames.
    
    Raises:
        PDFConversionError: If conversion fails
    """
    try:
        images = convert_from_bytes(pdf_bytes, dpi=dpi)
    except PDFInfoNotInstalledError:
        logger.error("Poppler is not installed or not in PATH")
        raise PDFConversionError("PDF conversion tool not available")
    except PDFPageCountError:
        logger.error("Could not get page count from PDF")
        raise PDFConversionError("Invalid or corrupted PDF")
    except PDFSyntaxError:
        logger.error("PDF syntax error")
        raise PDFConversionError("Invalid PDF format")
    except Exception as e:
        logger.error(f"PDF conversion failed: {str(e)}")
        raise PDFConversionError(f"PDF conversion failed: {str(e)}")
    
    batch_id = str(uuid.uuid4())[:8]
    filenames = []
    
    for i, image in enumerate(images):
        filename = f"{batch_id}_page_{i + 1}.png"
        filepath = IMAGES_DIR / filename
        image.save(str(filepath), format)
        filenames.append(filename)
    
    return filenames


def get_image_path(filename: str) -> Path | None:
    """
    Get the full path for an image file.
    Returns None if file doesn't exist or filename is invalid.
    
    Security: Validates filename pattern to prevent path traversal.
    """
    if not VALID_FILENAME_PATTERN.match(filename):
        return None
    
    filepath = (IMAGES_DIR / filename).resolve()
    
    if not filepath.is_relative_to(IMAGES_DIR.resolve()):
        return None
    
    if filepath.exists():
        return filepath
    return None


def cleanup_old_images(max_age_hours: int = 24):
    """
    Remove images older than max_age_hours.
    """
    import time
    
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    
    for filepath in IMAGES_DIR.glob("*.png"):
        file_age = current_time - filepath.stat().st_mtime
        if file_age > max_age_seconds:
            filepath.unlink()
