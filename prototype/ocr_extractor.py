# prototype/ocr_extractor.py
import re, os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import dateparser

# -------------------------------------------------
# SET THESE PATHS CORRECTLY FOR WINDOWS
# Example: Poppler bin folder -> C:\poppler-24.08.0\bin
# Example: Tesseract exe -> C:\Program Files\Tesseract-OCR\tesseract.exe
POPPLER_PATH = r"C:\Users\mysak\Downloads\Release-25.07.0-0\poppler-25.07.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# -------------------------------------------------

# Optional: spaCy for better org extraction (use only if installed)
try:
    import spacy
    _nlp = spacy.load("en_core_web_sm")
    SPACY_OK = True
except Exception:
    SPACY_OK = False
    _nlp = None

def pdf_to_text(pdf_path, dpi=300):
    """Convert PDF to text via page images -> pytesseract OCR."""
    pages = convert_from_path(pdf_path, dpi=dpi, poppler_path=POPPLER_PATH)
    texts = []
    for page in pages:
        texts.append(pytesseract.image_to_string(page, lang="eng"))
    return "\n".join(texts)

def image_to_text(image_path):
    img = Image.open(image_path)
    return pytesseract.image_to_string(img, lang="eng")

def normalize_text(text):
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# --- extraction helpers ---
def extract_dates(text):
    results = []
    try:
        from dateparser.search import search_dates
        found = search_dates(text, settings={'PREFER_DAY_OF_MONTH': 'first'})
    except Exception:
        found = None

    if found:
        for txt, dt in found:
            try:
                iso = dt.date().isoformat()
            except Exception:
                iso = None
            results.append({'text': txt, 'date': iso, 'confidence': 0.95})

    pattern = r'\b\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}\b'
    for m in set(re.findall(pattern, text)):
        dt = dateparser.parse(m, settings={'DATE_ORDER': 'DMY'})
        if dt:
            results.append({'text': m, 'date': dt.date().isoformat(), 'confidence': 0.9})

    seen, dedup = set(), []
    for r in results:
        key = (r.get('text'), r.get('date'))
        if key not in seen:
            dedup.append(r); seen.add(key)
    return dedup

def extract_amounts(text):
    pattern = r'((?:Rs\.?|INR|₹|\$|USD)\s?[0-9]+(?:[0-9,]*)(?:\.\d{1,2})?)'
    found = re.findall(pattern, text, flags=re.I)
    return [{'text': f.strip(), 'confidence': 0.95} for f in set(found)]

def extract_providers(text):
    providers = set()
    for line in text.split('\n'):
        if re.search(r'\b(Hospital|Clinic|Center|Centre|Medical|Laboratory|Lab)\b', line, re.I):
            providers.add(line.strip())
    if SPACY_OK:
        doc = _nlp(text)
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                providers.add(ent.text.strip())
    return [{'text': p, 'confidence': 0.85} for p in providers]

def simple_summary(text, max_sentences=3):
    sents = re.split(r'(?<=[.!?])\s+', text)
    if not sents:
        return ""
    keywords = ['injury','injuries','diagnosis','hospital','treatment','bill','billed','statute','incident','accident','ER','emergency']
    scored = []
    for i,s in enumerate(sents):
        score = sum(1 for kw in keywords if kw.lower() in s.lower())
        score += max(0, 1 - (i / max(1,len(sents))))
        scored.append((score, i, s.strip()))
    scored.sort(reverse=True)
    top = [s for _,_,s in scored[:max_sentences]]
    ordered = sorted(top, key=lambda ss: sents.index(ss))
    return ' '.join(ordered)

def compute_statute(incident_date_iso, years=2):
    dt = datetime.fromisoformat(incident_date_iso)
    expiry = dt + relativedelta(years=years)
    return expiry.date().isoformat()

def process_file(path, statute_years=2):
    if path.lower().endswith('.pdf'):
        text = pdf_to_text(path)
    else:
        text = image_to_text(path)
    text = normalize_text(text)
    dates = extract_dates(text)
    amounts = extract_amounts(text)
    providers = extract_providers(text)

    incident = None
    if dates:
        parsed = [d for d in dates if d.get('date')]
        if parsed:
            parsed_sorted = sorted(parsed, key=lambda x: x['date'])
            incident = parsed_sorted[0]['date']

    summary = simple_summary(text, max_sentences=3)
    out = {
        'file': os.path.basename(path),
        'incident_date': incident,
        'dates': dates,
        'amounts': amounts,
        'providers': providers,
        'summary': summary
    }
    if incident:
        out['statute_expiry'] = compute_statute(incident, years=statute_years)
    return out
