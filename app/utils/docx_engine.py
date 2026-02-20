import uuid
import logging
import subprocess
import tempfile
from pathlib import Path
from typing import List
from docx import Document

from app.utils.pdf_to_images import pdf_to_images

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("generated_images")
OUTPUT_DIR.mkdir(exist_ok=True)


class DOCXConversionError(Exception):
    pass


def docx_to_text(docx_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=True) as tmp:
        tmp.write(docx_bytes)
        tmp.flush()
        doc = Document(tmp.name)

    paragraphs = [p.text for p in doc.paragraphs]
    return "\n".join(paragraphs)


def docx_to_pdf(docx_bytes: bytes) -> bytes:
    with tempfile.TemporaryDirectory() as tmp_dir:
        input_path = Path(tmp_dir) / "input.docx"
        input_path.write_bytes(docx_bytes)

        try:
            result = subprocess.run(
                [
                    "libreoffice",
                    "--headless",
                    "--convert-to", "pdf",
                    "--outdir", tmp_dir,
                    str(input_path)
                ],
                capture_output=True,
                text=True,
                timeout=120
            )
        except subprocess.TimeoutExpired:
            raise DOCXConversionError("Conversion timed out after 120 seconds")
        except FileNotFoundError:
            raise DOCXConversionError("LibreOffice is not installed")

        if result.returncode != 0:
            logger.error(f"LibreOffice error: {result.stderr}")
            raise DOCXConversionError(f"Conversion failed: {result.stderr}")

        output_path = Path(tmp_dir) / "input.pdf"
        if not output_path.exists():
            raise DOCXConversionError("PDF output file was not created")

        return output_path.read_bytes()


def docx_to_images(docx_bytes: bytes, dpi: int = 150) -> List[str]:
    pdf_bytes = docx_to_pdf(docx_bytes)
    return pdf_to_images(pdf_bytes, dpi=dpi)
