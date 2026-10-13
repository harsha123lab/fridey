"""Text extraction for supported document types."""
from pathlib import Path

def extract_text(filename: str, data: bytes) -> str:
    ext = Path(filename or "").suffix.lower()
    if len(data) > 10 * 1024 * 1024: raise ValueError("Please upload a file smaller than 10 MB.")
    if ext in {".txt",".md",".csv",".json",".log"}: return data.decode("utf-8-sig",errors="replace")[:100000]
    if ext == ".pdf":
        from io import BytesIO
        from pypdf import PdfReader
        return "\n".join(p.extract_text() or "" for p in PdfReader(BytesIO(data)).pages)[:100000]
    if ext == ".docx":
        from io import BytesIO
        from docx import Document
        return "\n".join(p.text for p in Document(BytesIO(data)).paragraphs)[:100000]
    raise ValueError("Supported types: TXT, MD, CSV, JSON, LOG, PDF and DOCX.")
