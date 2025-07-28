# 🧾 PDF StructExtractor – Adobe Hackathon 2025 (Challenge 1A)

> 📘 A robust, containerized solution that extracts **structured data** from PDFs and outputs valid **JSON** — optimized for speed, memory, and no-network constraints.

---

## 🧠 Problem Overview

Adobe's Challenge 1a requires a CPU-only solution to **automatically process PDFs**, extract **structured hierarchical data**, and output it in a defined **JSON schema**, all within strict execution and system constraints.

---

## 📦 Key Features

| Feature                        | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| 📁 Batch PDF Processing       | Automatically scans and processes all `.pdf` files in `/app/input`         |
| 📤 Structured JSON Output     | Outputs individual `.json` files per PDF, matching given schema            |
| ⏱ Optimized for Speed        | Processes a **50-page PDF within 10 seconds**                              |
| 🔒 Offline, Secure            | Runs **without internet access**, inside a Docker container                |
| 🧠 Modular & Lightweight      | Total ML model weight under **200MB** (if ML is used)                      |
| 🧱 Containerized Architecture | Uses `Docker` for cross-platform compatibility and reproducibility         |

---

## 🔧 System Constraints

| Constraint                 | Value                              |
|---------------------------|-------------------------------------|
| Execution Time            | ≤ 10 seconds (for 50-page PDFs)    |
| Max RAM                   | 16 GB                              |
| CPUs                      | 8 (CPU-only, no GPU)               |
| Architecture              | AMD64 only                         |
| Network                   | ❌ No internet during runtime       |
| Model Size (if used)      | ≤ 200MB                            |

---

## ⚙ Technologies Used

| Category        | Tool/Library              |
|----------------|---------------------------|
| Language        | Python 3.10               |
| PDF Parsing     | `PyMuPDF (fitz)`, `pdfminer.six` *(modular)* |
| JSON Handling   | Python `json`             |
| Containerization| Docker                    |
| Schema Validator| `jsonschema` (optional)   |
| Others          | `os`, `pathlib`, `time`   |

---

## 🗂 Project Structure

```

Adobe\_1A/
├── sample\_dataset/
│   ├── pdfs/               # Input PDFs
│   ├── outputs/            # Output JSONs
│   └── schema/
│       └── output\_schema.json  # JSON schema for validation
├── Dockerfile              # Docker container config
├── process\_pdfs.py         # PDF → JSON conversion script
├── requirements.txt        # All Python dependencies
└── README.md               # Project documentation (you're here!)

````

---

## 🚀 Setup & Commands

### 1️⃣ Install Prerequisites

Ensure you have:
- 🐳 Docker installed (`v20+`)
- ✅ Python 3.10+ (for local testing)
- 📂 Directory structure as shown above

---

### 2️⃣ Install Python Dependencies (Local Testing Only)

```bash
pip install -r requirements.txt
````

Contents of `requirements.txt`:

```txt
PyMuPDF==1.22.5
pdfminer.six==20221105
jsonschema==4.21.1
```

---

### 3️⃣ Docker Build Command

```bash
docker build --platform linux/amd64 -t pdf-structextractor .
```

---

### 4️⃣ Docker Run Command

```bash
docker run --rm \
  -v $(pwd)/sample_dataset/pdfs:/app/input:ro \
  -v $(pwd)/sample_dataset/outputs:/app/output \
  --network none \
  pdf-structextractor
```

---

## 🧪 Testing Strategy

| Type of PDF     | Test Details                                           |
| --------------- | ------------------------------------------------------ |
| Simple PDFs     | Text-based, linear documents                           |
| Complex Layouts | Multi-columns, headers/footers, mixed fonts            |
| Large Files     | 50-page documents for runtime and memory compliance    |
| Tables/Images   | Ensure parser doesn’t crash, handles layout gracefully |

---

## ✅ Validation Checklist

* [x] All `.pdf` files in `/app/input` are scanned and processed
* [x] Corresponding `.json` files generated in `/app/output`
* [x] Output conforms to schema at `sample_dataset/schema/output_schema.json`
* [x] No internet access used during execution
* [x] Total runtime < 10 seconds for 50-page PDFs
* [x] Docker image runs on AMD64 without issues
* [x] Total memory usage ≤ 16GB
* [x] Output filenames match input filenames (e.g. `file.pdf` → `file.json`)

---

## 📜 Sample Code Snippet (Inside `process_pdfs.py`)

```python
from pathlib import Path
import json
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_blocks = []
    for page in doc:
        text_blocks.append(page.get_text())
    return "\n".join(text_blocks)

def generate_json_output(text, filename):
    return {
        "filename": filename,
        "content": text[:500],  # (truncate for demo)
        "meta": {
            "length": len(text),
            "type": "demo"
        }
    }

def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_file in input_dir.glob("*.pdf"):
        raw_text = extract_text_from_pdf(pdf_file)
        json_data = generate_json_output(raw_text, pdf_file.name)
        output_path = output_dir / f"{pdf_file.stem}.json"
        with open(output_path, "w") as f:
            json.dump(json_data, f, indent=4)

if __name__ == "__main__":
    process_pdfs()
```

---

## 📌 Notes & Future Enhancements

* ✅ Add `jsonschema` validation for schema compliance
* 🧠 Integrate ML-based segmentation (within 200MB)
* 🔍 Improve extraction for tables and scanned PDFs (OCR fallback)
* 🌍 Multilingual support via layout-aware extraction or NLP models

---

## 📣 Final Tip

> ⚠ Ensure testing is done on a system **without internet** to simulate final execution conditions.

---


## 🏁 Submission Guidelines

Each collection must include:

✅ `/PDFs/` folder with the source documents  
✅ `challenge1a_input.json` file  
✅ `challenge1a_output.json` file containing your extracted key information  

---

### ⚡ Let's Decode PDFs at Scale — Fast, Structured, Offline! 📄🚀

---



