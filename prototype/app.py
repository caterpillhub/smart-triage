# prototype/app.py
import os
from flask import Flask, request, jsonify
from ocr_extractor import process_file

app = Flask(__name__)
UPLOAD_DIR = "/tmp/smarttrie_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route("/ingest", methods=["POST"])
def ingest():
    if "file" not in request.files:
        return jsonify({"error":"No file uploaded"}), 400
    f = request.files["file"]
    path = os.path.join(UPLOAD_DIR, f.filename)
    f.save(path)
    result = process_file(path, statute_years=2)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
