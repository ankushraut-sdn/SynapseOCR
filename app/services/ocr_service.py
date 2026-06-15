import os
import tempfile
import shutil
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from docx import Document

from app.config import TESSERACT_PATH, POPPLER_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text_from_file(file, filename: str) -> str:
    filename = filename.lower()
    text = ''

    if filename.endswith('.pdf'):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
            shutil.copyfileobj(file, tmp_pdf)
            tmp_pdf_path = tmp_pdf.name
        try:
            images = convert_from_path(tmp_pdf_path, poppler_path=POPPLER_PATH)
            for image in images:
                text += pytesseract.image_to_string(image)
        finally:
            if os.path.exists(tmp_pdf_path):
                os.remove(tmp_pdf_path)

    elif filename.endswith(('.png', '.jpg', '.jpeg')):
        image = Image.open(file)
        text = pytesseract.image_to_string(image)

    elif filename.endswith('.docx'):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_docx:
            shutil.copyfileobj(file, tmp_docx)
            tmp_docx_path = tmp_docx.name
        try:
            doc = Document(tmp_docx_path)
            text = '\n'.join([para.text for para in doc.paragraphs])
        finally:
            if os.path.exists(tmp_docx_path):
                os.remove(tmp_docx_path)

    else:
        raise ValueError("Unsupported file format")

    return text
