import os
import json
from pathlib import Path
import fitz  # PyMuPDF
import re
from collections import Counter


def extract_structure_from_pdf(pdf_path):
    """
    Analyzes a PDF to extract a structured outline, limited to headings H1-H4,
    with logic to handle text fragmentation and noise.
    """
    doc = fitz.open(pdf_path)
    
    # --- 1. EXTRACT ALL TEXT LINES WITH STYLE INFORMATION ---
    all_lines = []
    font_sizes = Counter()
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict", sort=True)["blocks"]
        for b in blocks:
            if b['type'] == 0:
                for l in b["lines"]:
                    line_text = "".join(s["text"] for s in l["spans"]).strip()
                    if not line_text: continue
                    
                    first_span = l["spans"][0]
                    all_lines.append({
                        "text": line_text,
                        "size": round(first_span["size"]),
                        "bold": "bold" in first_span["font"].lower(),
                        "page": page_num,
                        "y0": l["bbox"][1]
                    })
                    font_sizes[round(first_span["size"])] += len(line_text)


    if not font_sizes:
        return {"title": pdf_path.stem, "outline": []}


    base_size = font_sizes.most_common(1)[0][0] if font_sizes else 12
    heading_sizes = sorted([s for s in font_sizes if s > base_size], reverse=True)
    size_to_level = {size: f"H{i+1}" for i, size in enumerate(heading_sizes)}
        
    raw_outline = []
    for line in all_lines:
        level = size_to_level.get(line["size"])

        # === THIS IS THE MINIMAL CHANGE ===
        # If not a heading by size, check if it's a 'special' bold line
        if not level and line["bold"]:
            # A bold line is only a heading if it's short and not a full sentence
            word_count = len(line['text'].split())
            if word_count < 10 and not line['text'].endswith('.'):
                level = f"H{len(heading_sizes) + 1}"
        # ================================
            
        if level:
            try:
                level_num = int(level.replace('H', ''))
                if level_num > 4: continue # Keep the H4 limit
            except (ValueError, IndexError): continue
            
            raw_outline.append({"level": level, "text": line["text"], "page": line["page"], "y0": line['y0']})


    # De-duplication logic remains the same
    raw_outline.sort(key=lambda x: (x['page'], -len(x['text']), x['y0']))
    final_outline, added_text_on_page = [], {}
    for item in raw_outline:
        page, text = item['page'], item['text']
        if page not in added_text_on_page: added_text_on_page[page] = set()
        is_fragment = any(text in existing for existing in added_text_on_page[page])
        if not is_fragment and text.strip() not in ('•', '▪', '▫'):
            final_outline.append(item)
            added_text_on_page[page].add(text)
    
    final_outline.sort(key=lambda x: (x['page'], x['y0']))
    for item in final_outline: del item['y0']


    title = doc.metadata.get('title') or pdf_path.stem.replace("_", " ").title()
    if final_outline and final_outline[0]['level'] in ('H1', 'H2'):
        title = final_outline[0]['text']


    return {"title": title, "outline": final_outline}


def process_pdfs():
    # This main function is the same, just calling the extractor
    input_dir = Path("sample_dataset/pdfs")
    output_dir = Path("sample_dataset/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return


    for pdf_file in pdf_files:
        print(f"Processing {pdf_file.name}...")
        try:
            extracted_data = extract_structure_from_pdf(pdf_file)
            output_file = output_dir / f"{pdf_file.stem}.json"
            with open(output_file, "w", encoding='utf-8') as f:
                json.dump(extracted_data, f, indent=4)
            print(f" -> Successfully saved to {output_file.name}")
        except Exception as e:
            print(f" -> Failed to process {pdf_file.name}: {e}")


if __name__ == "__main__":
    print("Starting PDF processing with smarter bold-text detection...")
    process_pdfs() 
    print("Completed processing PDFs.")
