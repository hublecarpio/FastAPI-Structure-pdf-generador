from weasyprint import HTML
from io import BytesIO


def html_to_pdf(html_content: str) -> bytes:
    html = HTML(string=html_content)
    pdf_buffer = BytesIO()
    html.write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer.read()
