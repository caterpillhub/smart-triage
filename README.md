# 🩺 SmartTriage

> **Intelligent Document Processing for Personal Injury Cases**

SmartTriage is a proof-of-concept Python tool that automates document ingestion for personal injury cases. It intelligently extracts key details including dates, medical providers, and financial amounts, computes statutory deadlines, and produces concise case summaries to streamline legal workflows.

## ✨ Features

- **📄 Document Processing**: Automated PDF ingestion with OCR capabilities
- **🔍 Smart Extraction**: Identifies dates, providers, and monetary amounts
- **⏰ Deadline Calculation**: Computes statutory deadlines automatically  
- **📝 Case Summarization**: Generates concise case overviews
- **🔌 Dual Interface**: Both CLI and REST API access

---

## 📦 Installation

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd smarttriage
```

### 2. Setup Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- `pdf2image` – PDF to image conversion
- `pytesseract` – OCR with Tesseract engine
- `Pillow` – Advanced image processing
- `dateparser`, `python-dateutil` – Intelligent date parsing
- `flask` – Lightweight API server
- `spacy` + `en_core_web_sm` – Named entity recognition *(optional)*

### 4. External Tools Setup

#### Poppler (Required for PDF processing)
- **Download**: [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
- **Setup**: Extract and add `bin` folder to system PATH
  - Example path: `C:\poppler-24.08.0\bin`

#### Tesseract OCR (Required for text extraction)
- **Download**: [Tesseract OCR for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
- **Default Installation**: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- **Custom Path**: Update path in `ocr_extractor.py` if needed

***

## 🚀 Usage

### CLI Interface

Process documents directly from command line:

```bash
python prototype/cli_demo.py prototype/samples/medical_bill.pdf
```

**Sample Output:**
```json
{
  "file": "medical_bill.pdf",
  "incident_date": "2024-07-14",
  "providers": [{"text": "St. Mercy Hospital", "confidence": 0.85}],
  "amounts": [{"text": "$12,400", "confidence": 0.95}],
  "summary": "John Doe suffered whiplash...",
  "statute_expiry": "2026-07-14"
}
```

### REST API

Launch the Flask development server:

```bash
python prototype/app.py
```

**Upload via cURL:**
```bash
curl -F "file=@prototype/samples/medical_bill.pdf" http://127.0.0.1:5000/ingest
```

**Postman Integration:**
- Method: `POST`
- URL: `http://127.0.0.1:5000/ingest`
- Body: `form-data` with file upload

***

## 📁 Project Structure

```
prototype/
├── app.py              # Flask REST API server
├── cli_demo.py         # Command-line interface
├── ocr_extractor.py    # Core OCR and extraction engine
└── samples/            # Sample PDF test files
```

***

## ⚠️ Important Considerations

### Current Limitations
- **Prototype Stage**: Optimized for English text documents and high-quality scans
- **OCR Dependency**: Accuracy varies with PDF quality and Tesseract configuration
- **Legal Review Required**: All extracted data must be verified by qualified attorneys

### Planned Enhancements
- Advanced medical entity recognition
- Enhanced summarization algorithms
- CloudLex API integration
- Multi-language support

***

## 🛠️ Technology Stack

**Core Technologies:**
- Python 3.x
- Tesseract OCR Engine
- Poppler PDF Utilities

**Key Libraries:**
- Flask for API framework
- OpenCV for image processing
- spaCy for natural language processing

***

## 🤝 Contributing

We welcome contributions! Please ensure all changes maintain compatibility with the existing OCR pipeline and follow Python best practices.

## 📄 License

This project is provided as-is for educational and prototype purposes. Please consult legal professionals before deploying in production environments.
