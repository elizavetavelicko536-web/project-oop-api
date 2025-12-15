from src.annotations.annotator import save_results_to_docx
from docx import Document
import os

def test_save_results_to_docx(tmp_path):
    results = {
        "file1.docx": "Аннотация 1",
        "file2.docx": "Аннотация 2",
    }

    out_dir = tmp_path / "out"
    out_path = save_results_to_docx(results, str(out_dir))

    assert os.path.exists(out_path)

    doc = Document(out_path)
    text = "\n".join(p.text for p in doc.paragraphs)

    assert "file1.docx" in text
    assert "file2.docx" in text
    assert "Аннотация 1" in text
    assert "Аннотация 2" in text