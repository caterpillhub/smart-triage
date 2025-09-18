SmartTriage Prototype

SmartTriage is a proof-of-concept Python tool that automates document ingestion for personal injury cases. It extracts key details (dates, providers, amounts), computes statutory deadlines, and produces a short case summary.

📦 Installation
1. Clone the project
git clone <your-repo-url>
cd smarttrie

2. Create and activate virtual environment

Windows (PowerShell):

python -m venv venv
venv\Scripts\Activate

macOS/Linux:

python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

Dependencies include:

pdf2image – for converting PDFs to images
pytesseract – OCR with Tesseract
Pillow – image handling
dateparser, python-dateutil – parsing dates
flask – simple API server
(optional) spacy + en_core_web_sm for NER

4. Install external tools

Poppler (for pdf2image)
Download: Poppler for Windows
Extract and set path to bin folder (e.g., C:\poppler-24.08.0\bin).
Tesseract OCR
Download: Tesseract OCR (Windows)
Install to default: C:\Program Files\Tesseract-OCR\tesseract.exe.
Update ocr_extractor.py if installed in another path.

🚀 How to Run
CLI Demo

Run extraction on a sample file:
python prototype/cli_demo.py prototype/samples/medical_bill.pdf

Expected output (JSON):

{
  "file": "medical_bill.pdf",
  "incident_date": "2024-07-14",
  "providers": [{"text": "St. Mercy Hospital", "confidence": 0.85}],
  "amounts": [{"text": "$12,400", "confidence": 0.95}],
  "summary": "John Doe suffered whiplash...",
  "statute_expiry": "2026-07-14"
}

API Demo

Start the Flask server:
python prototype/app.py

Upload a document via curl:
curl -F "file=@prototype/samples/medical_bill.pdf" http://127.0.0.1:5000/ingest

Or test with Postman by sending a POST request to /ingest with form-data containing the file.

📂 Project Structure
prototype/
│── app.py              # Flask API
│── cli_demo.py         # Command-line demo
│── ocr_extractor.py    # Core OCR + extraction logic
│── samples/            # Example PDF inputs

⚠️ Notes & Limitations

Prototype stage: works best on English text documents and clear scans.
OCR accuracy depends on PDF quality and Tesseract language settings.
Attorneys must review extracted data before relying on it.
Planned enhancements: better medical NER, advanced summarization, CloudLex API integration.

🙌 Credits
Built with Python, Tesseract OCR, and Poppler.
