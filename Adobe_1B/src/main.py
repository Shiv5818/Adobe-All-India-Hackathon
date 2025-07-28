# main.py - Entry point for processing PDF collections
import os
import glob
import logging
from pdf_processor import extract_text_from_pdf
from text_analyzer import identify_sections, rank_sections, analyze_subsections
from utils import load_input_json, save_output_json, get_timestamp

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

COLLECTION_PATTERN = "Collection_*"  # Configurable pattern for collection directories

def process_collection(collection_dir: str) -> None:
    """Process a single collection and generate output JSON."""
    input_json_path = os.path.join(collection_dir, "challenge1b_input.json")
    output_json_path = os.path.join(collection_dir, "challenge1b_output.json")
    pdf_dir = os.path.join(collection_dir, "PDFs")

    input_data = load_input_json(input_json_path)
    if not input_data:
        logging.warning(f"No input data found for {collection_dir}, skipping.")
        return
    documents = input_data.get("documents", [])
    persona = input_data.get("persona", {}).get("role", "")
    job_to_be_done = input_data.get("job_to_be_done", {}).get("task", "")

    all_extracted_sections = []
    all_subsection_analysis = []

    for doc in documents:
        pdf_path = os.path.join(pdf_dir, doc.get("filename", ""))
        if not os.path.exists(pdf_path):
            logging.warning(f"{pdf_path} not found, skipping.")
            continue
        # Extract text with page numbers
        text_by_page = extract_text_from_pdf(pdf_path)
        if not text_by_page:
            logging.warning(f"No text extracted from {pdf_path}, skipping.")
            continue
        # Identify and rank sections
        sections = [section for page_num, text in text_by_page.items() for section in identify_sections(text, page_num)]
        ranked_sections = rank_sections(sections, persona, job_to_be_done)
        # Collect extracted sections
        for section_title, _, page_number, importance_rank in ranked_sections:
            all_extracted_sections.append({
                "document": doc.get("filename", ""),
                "section_title": section_title,
                "page_number": page_number,
                "importance_rank": importance_rank
            })
        # Analyze subsections
        subsection_analysis = analyze_subsections(ranked_sections, persona, job_to_be_done)
        for analysis in subsection_analysis:
            all_subsection_analysis.append({
                "document": doc.get("filename", ""),
                "refined_text": analysis.get("refined_text", ""),
                "page_number": analysis.get("page_number", "")
            })
    # Prepare output
    output = {
        "metadata": {
            "input_documents": [doc.get("filename", "") for doc in documents],
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": get_timestamp()
        },
        "extracted_sections": all_extracted_sections,
        "subsection_analysis": all_subsection_analysis
    }
    save_output_json(output, output_json_path)
    logging.info(f"Output saved to {output_json_path}")

def main() -> None:
    """Process all collections dynamically."""
    collection_dirs = glob.glob(COLLECTION_PATTERN)
    if not collection_dirs:
        logging.warning("No collection directories found.")
        return
    for collection_dir in collection_dirs:
        if os.path.isdir(collection_dir):
            logging.info(f"Processing {collection_dir}...")
            process_collection(collection_dir)
        else:
            logging.warning(f"{collection_dir} is not a directory, skipping.")

if __name__ == "__main__":
    main()