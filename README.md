# SynapseOCR

## 1. Project Overview

A document OCR web app. Upload a PDF or image, extract its text (via Tesseract OCR, with PDFs converted to images first), then clean up and structure the extracted text using Google's Gemini model.

## 2. Core Features

- File upload endpoint that runs OCR (`POST /ocr`) and returns the organized text
- PDF-to-image conversion via `pdf2image`/Poppler, then text extraction via `pytesseract` (`app/services/ocr_service.py`)
- Post-processing/cleanup of raw OCR output using the Gemini API (`app/services/gemini_service.py`)
- Sample documents available for quick testing (`GET /list-sample-docs`, `GET /download-sample/{filename}`)
- Result export/download (`GET /download/{filename}`)
- Simple server-rendered frontend (Jinja2 template) served at `/`

## 3. Tech Stack

| Component | Technology |
|---|---|
| Backend | FastAPI, Uvicorn |
| OCR | `pytesseract` + system Tesseract OCR engine |
| PDF handling | `pdf2image` + Poppler |
| Text cleanup | Google Gemini API |
| Export | `python-docx`, `reportlab` |

## 4. Project Structure

```
SynapseOCR/
├── app/
│   ├── api/endpoints.py        # routes: upload, OCR, sample docs, download
│   ├── services/
│   │   ├── ocr_service.py       # Tesseract/pdf2image extraction
│   │   └── gemini_service.py    # Gemini-based text cleanup
│   ├── static/doc_samples/      # sample files for the UI
│   ├── templates/index.html     # frontend page
│   ├── config.py                # env-driven settings
│   └── main.py                  # FastAPI app
├── run.py                       # entrypoint (uvicorn)
└── requirements.txt
```

## 5. Prerequisites

- Python 3.10+
- System packages: `tesseract-ocr`, `poppler-utils`
- A Google Gemini API key

## 6. How to Run

1. Install system dependencies (not pip-installable): Tesseract OCR and Poppler.
   ```bash
   sudo apt-get install tesseract-ocr poppler-utils
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables (create a `.env` file in the project root):
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   TESSERACT_PATH=/usr/bin/tesseract      # optional override
   POPPLER_PATH=/usr/bin                  # optional override
   ```
4. Run the server:
   ```bash
   python run.py
   ```
   The app listens on `http://127.0.0.1:9068`.

## 7. API Documentation

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Server-rendered upload page. |
| GET | `/list-sample-docs` | Lists sample documents available for testing. |
| GET | `/download-sample/{filename}` | Downloads a sample document. |
| POST | `/ocr` | Uploads a PDF/image, runs OCR, and returns Gemini-cleaned text. |
| GET | `/download/{filename}` | Downloads a previously generated result file. |

## 8. Environment Variables

| Variable | Default | Description |
|---|---|---|
| `GEMINI_API_KEY` | — | Required for Gemini-based text cleanup. |
| `TESSERACT_PATH` | system default | Optional override for the Tesseract binary path. |
| `POPPLER_PATH` | system default | Optional override for the Poppler binary path. |

## 9. Known Limitations

- No automated tests currently exist in the repository.
- Requires system-level binaries (Tesseract, Poppler) that are not managed via `requirements.txt`.

## License

No LICENSE file is present in this repository.
