from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from typing import Dict

# Extract text from PDF file with page numbers

def extract_text_from_pdf(pdf_path: str) -> Dict[int, str]:
    """
    Extract text from a PDF file, mapping page numbers to text.
    Args:
        pdf_path (str): Path to the PDF file.
    Returns:
        dict: Page number to extracted text mapping.
    """
    try:
        text_by_page = {}
        for page_num, page_layout in enumerate(extract_pages(pdf_path), start=1):
            page_text = []
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    page_text.append(element.get_text().strip())
            text_by_page[page_num] = "\n".join(page_text) if page_text else ""
        return text_by_page
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return {}