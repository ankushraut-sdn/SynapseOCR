import os
import tempfile
from fastapi import APIRouter, Request, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates

from app.services.ocr_service import extract_text_from_file
from app.services.gemini_service import organize_text

router = APIRouter()

# Get base directory for templates and static files relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
DOC_SAMPLE_DIR = os.path.join(BASE_DIR, "static", "doc_samples")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/list-sample-docs")
def list_sample_docs():
    try:
        files = os.listdir(DOC_SAMPLE_DIR)
        return JSONResponse(content=files)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.get("/download-sample/{filename}")
def download_sample(filename: str):
    file_path = os.path.join(DOC_SAMPLE_DIR, filename)
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": "File not found"})
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)


@router.post("/ocr")
def ocr(file: UploadFile = File(...)):
    if not file or not file.filename:
        return JSONResponse(status_code=400, content={'error': 'No file uploaded'})

    try:
        # Extract text from uploaded file using OCR service
        text = extract_text_from_file(file.file, file.filename)

        # Format/organize text using Gemini service
        final_organized_text = organize_text(text)

        return JSONResponse(content={'final_text': final_organized_text})

    except ValueError as ve:
        return JSONResponse(status_code=400, content={'error': str(ve)})
    except Exception as e:
        return JSONResponse(status_code=500, content={'error': str(e)})


@router.get("/download/{filename}")
def download(filename: str):
    directory = tempfile.gettempdir()
    file_path = os.path.join(directory, filename)
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": "File not found"})
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
