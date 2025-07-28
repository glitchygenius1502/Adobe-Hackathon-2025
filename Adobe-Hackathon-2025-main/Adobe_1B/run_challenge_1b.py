from pathlib import Path
import json
import fitz  # PyMuPDF
from collections import Counter
from datetime import datetime
import re
import nltk
from nltk.corpus import stopwords

def setup_nltk():
    """Checks for and downloads required NLTK data packages."""
    packages = {
        'punkt': 'tokenizers/punkt',
        'stopwords': 'corpora/stopwords'
    }
    for pkg_id, pkg_path in packages.items():
        try:
            nltk.data.find(pkg_path)
        except LookupError:
            print(f"--- First-time setup: Downloading NLTK '{pkg_id}' package... ---")
            nltk.download(pkg_id, quiet=True)

#  HELPER FUNCTION 1: EXTRACT HEADINGS AND PARAGRAPHS

def extract_document_structure(pdf_path):
    doc = fitz.open(pdf_path)
    structure = []
    all_lines, font_sizes = [], Counter()
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict", sort=True)["blocks"]
        for b in blocks:
            if b.get('type') == 0:
                for l in b["lines"]:
                    line_text = "".join(s["text"] for s in l["spans"]).strip()
                    if not line_text: continue
                    first_span = l["spans"][0]
                    all_lines.append({
                        "text": line_text, "size": round(first_span["size"]),
                        "bold": "bold" in first_span["font"].lower(), "page": page_num, "y0": l["bbox"][1]
                    })
                    font_sizes[round(first_span["size"])] += len(line_text)
    if not font_sizes: return doc, []
    base_size = font_sizes.most_common(1)[0][0] if font_sizes else 12
    heading_sizes = sorted([s for s in font_sizes if s > base_size], reverse=True)
    size_to_level = {size: f"H{i+1}" for i, size in enumerate(heading_sizes)}
    for line in all_lines:
        level = size_to_level.get(line["size"])
        if not level and line["bold"] and len(line['text'].split()) < 10 and not line['text'].endswith('.'):
             level = f"H{len(heading_sizes) + 1}"
        structure.append({"level": level if level else "P", "text": line["text"], "page": line["page"], "y0": line["y0"]})
    return doc, structure

#  HELPER FUNCTION 2: IMPORTANCE RANKING 

def rank_importance(section_title, job_to_be_done):
    """Ranks section importance based on relevance to the job_to_be_done."""
    title_words = set(re.findall(r'\w+', section_title.lower()))
    query_words = set(re.findall(r'\w+', job_to_be_done.lower()))

    stop_words = set(stopwords.words('english'))
    title_words -= stop_words
    query_words -= stop_words

    common_words = title_words.intersection(query_words)

    if len(common_words) >= 2: return 1  # Most relevant
    if len(common_words) == 1: return 2  # Relevant

    # Fallback for generic travel-related terms if the query is also about travel
    generic_query_keywords = {"plan", "guide", "trip", "itinerary", "find"}
    if query_words.intersection(generic_query_keywords):
        if any(k in title_words for k in ["nightlife", "entertainment", "adventures", "activities", "do"]): return 2
        if any(k in title_words for k in ["restaurants", "hotels", "cuisine", "cities", "stay", "eat"]): return 3

    return 4  # Low relevance

#  NEW HELPER FUNCTION 3: GET CONTENT UNDER A HEADING
def get_content_under_heading(doc_name, heading_item, all_docs_structure):
    """Finds all paragraph text under a given heading until the next one."""
    structure = all_docs_structure[doc_name][1]
    try:
        start_index = structure.index(heading_item)
    except ValueError:
        return ""

    content = []
    for i in range(start_index + 1, len(structure)):
        item = structure[i]
        if item['level'] != 'P':  # Stop if we hit any other heading
            break
        content.append(item['text'])
    return " ".join(content)

#  HELPER FUNCTION 4: THE DYNAMIC AI TRAVEL PLANNER
def generate_dynamic_summary(ranked_sections, all_docs_structure, job_to_be_done):
    """
    Synthesizes a response based on the job-to-be-done and the most relevant
    document sections, simulating an AI-driven analysis.
    """
    top_sections = [s for s in ranked_sections if s['importance_rank'] <= 2][:5] # Use top 5 relevant sections

    if not top_sections:
        return [{"document": "Synthesized Summary", "refined_text": "Could not find relevant sections in the documents for your request. Please try a different query.", "page_number_constraints": []}]

    summary_points = []
    query_words = set(re.findall(r'\w+', job_to_be_done.lower())) - set(stopwords.words('english'))

    for section_info in top_sections:
        doc_name = section_info['document']
        doc_structure = all_docs_structure[doc_name][1]
        heading_item = next((item for item in doc_structure if item['text'] == section_info['section_title'] and item['page'] == section_info['page_number']), None)

        if not heading_item: continue

        content = get_content_under_heading(doc_name, heading_item, all_docs_structure)
        if not content: continue

        sentences = nltk.sent_tokenize(content)
        key_sentences = [s for s in sentences if any(w in s.lower() for w in query_words)]

        # Fallback to first 2 sentences if no specific keywords are matched
        summary_for_section = " ".join(key_sentences[:2] if key_sentences else sentences[:2])

        if summary_for_section:
            summary_points.append(
                f"Regarding '{section_info['section_title']}', the document suggests: \"{summary_for_section.strip()}\" (from {doc_name}, page {section_info['page_number']})"
            )

    # Structure the final output like a plan or a list of suggestions
    is_plan_request = any(word in job_to_be_done.lower() for word in ['plan', 'itinerary', 'day', 'trip', 'schedule'])

    if is_plan_request:
        intro = f"Based on your request to '{job_to_be_done}', here is a suggested plan based on the provided documents:"
        plan_steps = [f"Step {i+1}: {point}" for i, point in enumerate(summary_points)]
        final_text = f"{intro}\n\n" + "\n\n".join(plan_steps)
    else:
        intro = f"In response to your query '{job_to_be_done}', here are the key findings from the documents:"
        bullet_points = [f"- {point}" for point in summary_points]
        final_text = f"{intro}\n\n" + "\n".join(bullet_points)

    return [{"document": "Synthesized Summary", "refined_text": final_text or "No specific details found for your request.", "page_number_constraints": [s['page_number'] for s in top_sections]}]

#  MAIN PROCESSING FUNCTION - FULLY UPGRADED
def perform_analysis(input_data, pdf_paths):
    persona = input_data.get("persona", {}).get("role")
    job_to_be_done = input_data.get("job_to_be_done", {}).get("task", "")

    # Step 1: Extract and Rank all sections based on job_to_be_done
    extracted_sections_output = []
    all_docs_structure = {}
    for pdf_path in pdf_paths:
        doc, structure = extract_document_structure(pdf_path)
        all_docs_structure[pdf_path.name] = (doc, structure)

        headings = [item for item in structure if item['level'] != 'P']
        for heading in headings:
            rank = rank_importance(heading["text"], job_to_be_done)
            extracted_sections_output.append({
                "document": pdf_path.name, "section_title": heading["text"],
                "importance_rank": rank, "page_number": heading["page"]
            })

    extracted_sections_output.sort(key=lambda x: x['importance_rank'])

    # Step 2: Generate a dynamic summary based on the most relevant sections
    sub_section_analysis_output = generate_dynamic_summary(
        extracted_sections_output, all_docs_structure, job_to_be_done
    )

    # Step 3: Assemble the final output
    final_output = {
        "metadata": {"input_documents": [path.name for path in pdf_paths], "persona": persona, "job_to_be_done": job_to_be_done, "processing_timestamp": datetime.now().isoformat()},
        "extracted_sections": [s for s in extracted_sections_output if s['importance_rank'] <= 2], # Only show relevant sections
        "sub_section_analysis": sub_section_analysis_output
    }
    return final_output

def process_collection(collection_path):
    # This function remains largely the same
    print(f"--- Processing Collection: {collection_path.name} ---")
    input_json_path = collection_path / "challenge1b_input.json"
    pdfs_dir = collection_path / "PDFs"
    output_json_path = collection_path / "challenge1b_output.json"
    if not all([input_json_path.exists(), pdfs_dir.is_dir()]): return
    with open(input_json_path, 'r', encoding='utf-8') as f: input_data = json.load(f)
    pdf_paths = list(pdfs_dir.glob("*.pdf"))
    final_output = perform_analysis(input_data, pdf_paths)
    with open(output_json_path, 'w', encoding='utf-8') as f: json.dump(final_output, f, indent=4)
    print(f"  - Successfully wrote DYNAMIC SUMMARY to {output_json_path.name}\n")

if __name__ == "__main__":
    setup_nltk()
    challenge_dir = Path(__file__).parent
    collection_dirs = sorted([d for d in challenge_dir.iterdir() if d.is_dir() and d.name.startswith("Collection")])
    for collection_dir in collection_dirs:
        process_collection(collection_dir)
    print("--- All collections processed. ---")
