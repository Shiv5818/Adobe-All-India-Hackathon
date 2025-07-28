import re
import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer

def load_model_and_tokenizer(model_path="models/distilbert"):
    """Load the pre-trained DistilBERT model and tokenizer."""
    try:
        model = DistilBertForSequenceClassification.from_pretrained(model_path)
        tokenizer = DistilBertTokenizer.from_pretrained(model_path)
        return model, tokenizer
    except Exception as e:
        print(f"Error loading model/tokenizer: {e}")
        return None, None

def preprocess_text(text):
    """Preprocess text by removing extra whitespace and limiting length."""
    text = re.sub(r'\s+', ' ', text.strip())
    return text[:512]  # Truncate to fit DistilBERT's max length

def identify_sections(text, page_num):
    """
    Identify sections in the text based on heuristics.
    
    Args:
        text (str): Text from a single page.
        page_num (int): Page number.
    Returns:
        list: List of (section_title, section_text, page_number) tuples.
    """
    lines = text.split('\n')
    sections = []
    current_section = None
    current_text = []
    
    # Heuristic: Headings are short, capitalized, or followed by content
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Detect headings: short lines (<50 chars), capitalized, or followed by content
        if (len(line) < 50 and 
            (line.isupper() or line.istitle() or re.match(r'^[A-Z][A-Za-z\s\-\:]+$', line))):
            if current_section and current_text:
                sections.append((current_section, '\n'.join(current_text), page_num))
            current_section = line
            current_text = []
        elif current_section:
            current_text.append(line)
    
    if current_section and current_text:
        sections.append((current_section, '\n'.join(current_text), page_num))
    
    return sections

def rank_sections(sections, persona, job_to_be_done):
    """
    Rank sections based on relevance using DistilBERT.
    
    Args:
        sections (list): List of (section_title, section_text, page_number) tuples.
        persona (str): Persona role description.
        job_to_be_done (str): Task description.
    Returns:
        list: Top 5 ranked sections with (section_title, section_text, page_number, rank).
    """
    model, tokenizer = load_model_and_tokenizer()
    if not model or not tokenizer:
        return [(s[0], s[1], s[2], i + 1) for i, s in enumerate(sections[:5])]
    
    model.eval()
    query = f"{persona} {job_to_be_done}".lower()
    inputs = [preprocess_text(s[1]) for s in sections]
    inputs.append(query)  # Include query for comparison
    
    encodings = tokenizer(inputs, padding=True, truncation=True, max_length=512, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**encodings)
        scores = outputs.logits[:, 1].cpu().numpy()  # Probability of positive class
    
    section_scores = scores[:-1]  # Exclude query score
    
    # Sort sections by score, assign ranks
    ranked_sections = [
        (sections[i][0], sections[i][1], sections[i][2], idx + 1)
        for idx, i in enumerate(sorted(range(len(section_scores)), key=lambda k: section_scores[k], reverse=True))
    ]
    
    return ranked_sections[:5]  # Return top 5 sections

def analyze_subsections(ranked_sections, persona, job_to_be_done):
    """
    Perform subsection analysis by extracting refined text.
    
    Args:
        ranked_sections (list): List of ranked sections.
        persona (str): Persona role description.
        job_to_be_done (str): Task description.
    Returns:
        list: List of dictionaries with refined text and page number.
    """
    # Simple keyword-based filtering for relevance
    keywords = set((persona + " " + job_to_be_done).lower().split())
    
    analysis = []
    for section in ranked_sections:
        section_text = section[1]
        page_number = section[2]
        
        # Split into sentences for granular analysis
        sentences = re.split(r'(?<=[.!?])\s+', section_text)
        relevant_sentences = [
            s for s in sentences 
            if any(keyword in s.lower() for keyword in keywords)
        ]
        
        refined_text = ' '.join(relevant_sentences[:3])  # Limit to 3 sentences for conciseness
        if refined_text:
            analysis.append({
                "refined_text": preprocess_text(refined_text),
                "page_number": page_number
            })
    
    return analysis