from __future__ import annotations
from typing import overload
import pdfplumber
from docx import Document


@overload
def read_file(path: str) -> str:
    ...


@overload
def read_file(path: bytes) -> str:
    ...


def read_file(path):
    p = str(path)

    if p.lower().endswith(".pdf"):
        with pdfplumber.open(p) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        return "\n\n".join(pages)

    elif p.lower().endswith(".docx"):
        doc = Document(p)
        paras = [p.text for p in doc.paragraphs]
        return "\n".join(paras)

    else:
        raise ValueError("Unsupported file type: " + p)
