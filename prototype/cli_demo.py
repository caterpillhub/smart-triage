# prototype/cli_demo.py
import sys, json
from ocr_extractor import process_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python cli_demo.py path/to/file.pdf")
        sys.exit(1)
    path = sys.argv[1]
    result = process_file(path, statute_years=2)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
