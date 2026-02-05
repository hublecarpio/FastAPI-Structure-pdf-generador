import os
import uuid
from pathlib import Path
from pdf2image import convert_from_bytes
from typing import List

IMAGES_DIR = Path("generated_images")
IMAGES_DIR.mkdir(exist_ok=True)


def pdf_to_images(pdf_bytes: bytes, dpi: int = 150, format: str = "PNG") -> List[str]:
    """
    Convert PDF bytes to images and save them to disk.
    Returns list of filenames.
    """
    images = convert_from_bytes(pdf_bytes, dpi=dpi)
    
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
    Returns None if file doesn't exist.
    """
    filepath = IMAGES_DIR / filename
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
