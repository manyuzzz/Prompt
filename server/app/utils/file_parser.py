import io
from typing import Optional


async def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        from pdfminer.high_level import extract_text
        text = extract_text(io.BytesIO(file_bytes))
        return text.strip() if text else ""
    except ImportError:
        return "PDF text extraction requires pdfminer.six. Install with: pip install pdfminer.six"
    except Exception as e:
        return f"Error extracting PDF text: {str(e)}"


async def extract_text_from_docx(file_bytes: bytes) -> str:
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        paragraphs.append(cell.text.strip())
        return "\n".join(paragraphs)
    except Exception as e:
        return f"Error extracting DOCX text: {str(e)}"


def validate_resume_file(filename: str, file_size: int, max_size: int = 10 * 1024 * 1024) -> Optional[str]:
    if file_size > max_size:
        return f"File size exceeds {max_size // (1024*1024)}MB limit"
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext not in ('pdf', 'docx', 'doc'):
        return "Only PDF and DOCX files are supported"
    return None
