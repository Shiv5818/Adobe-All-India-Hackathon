# Adobe Hackathon Round 1B: Persona-Driven Document Intelligence

## Overview
This project implements an intelligent document analyst system that extracts and prioritizes the most relevant sections from collections of PDF documents based on specific personas and their job-to-be-done tasks. Built for Adobe All India Hackathon Round 1B, it processes diverse document types and provides persona-tailored insights using DistilBERT transformer models.

## Hackathon Challenge Features
- **Persona-Driven Analysis:** Extracts and ranks sections based on specific user roles and tasks
- **Multi-Document Processing:** Handles 3-10 related PDFs across diverse domains (research, business, education)
- **Intelligent Section Detection:** Heuristic-based heading identification with title/content pattern recognition
- **DistilBERT Integration:** Transformer model for semantic relevance scoring and ranking
- **Granular Subsection Analysis:** Keyword-based refinement of important content sections
- **Generic Solution:** Adapts to various document types, personas, and job-to-be-done scenarios
- **Structured JSON Output:** Compliant with hackathon specification format
- **Offline Processing:** No internet dependencies during execution

## Hackathon Compliance
- ✅ **CPU-Only Operation:** No GPU dependencies, pure CPU processing
- ✅ **Model Size:** DistilBERT (~250MB) well under 1GB constraint
- ✅ **Processing Time:** Optimized for ≤60 seconds per document collection
- ✅ **Offline Operation:** Zero internet access during execution
- ✅ **Generic Solution:** Handles diverse domains, personas, and tasks
- ✅ **Output Format:** Exact JSON specification compliance
- ✅ **Docker Ready:** Containerized with all dependencies

## Directory Structure
```
Adobe_1B/
├── Dockerfile
├── requirements.txt
├── download_model.py
├── approach_explanation.md
├── src/
│   ├── main.py              # Entry point and orchestration
│   ├── pdf_processor.py     # PDF text extraction with page mapping
│   ├── text_analyzer.py     # NLP-based section analysis
│   └── utils.py             # JSON I/O and utility functions
├── Collection_1/
│   ├── PDFs/                # PDF files for collection 1
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
├── Collection_2/
│   └── ...
└── Collection_3/
    └── ...
```

## Technical Approach

### 1. Document Processing Pipeline
1. **Collection Discovery:** Automatically detects `Collection_*` directories
2. **Input Parsing:** Reads `challenge1b_input.json` for documents, persona, and job-to-be-done
3. **PDF Text Extraction:** Uses `pdfminer.six` with page-wise text mapping
4. **Section Identification:** Heuristic-based heading detection using pattern matching
5. **Relevance Ranking:** DistilBERT-powered semantic scoring against persona+task query
6. **Subsection Analysis:** Keyword-based refinement of top-ranked sections
7. **JSON Output:** Structured results saved to `challenge1b_output.json`

### 2. Core Algorithms

#### Section Detection Logic
```python
# Heuristic-based heading identification
def identify_sections(text, page_num):
    # Detect headings: short lines (<50 chars), capitalized, or title case
    if (len(line) < 50 and
        (line.isupper() or line.istitle() or
         re.match(r'^[A-Z][A-Za-z\s\-\:]+$', line))):
        # Process as section heading
```

#### Relevance Ranking with DistilBERT
```python
# Semantic similarity scoring
query = f"{persona} {job_to_be_done}".lower()
encodings = tokenizer(inputs, padding=True, truncation=True, max_length=512)
outputs = model(**encodings)
scores = outputs.logits[:, 1].cpu().numpy()  # Relevance scores
```

#### Subsection Analysis
```python
# Keyword-based content refinement
keywords = set((persona + " " + job_to_be_done).lower().split())
relevant_sentences = [s for s in sentences
                     if any(keyword in s.lower() for keyword in keywords)]
```

## Sample Test Cases Supported

### Test Case 1: Travel Planning
- **Documents:** 7 PDFs about South of France (Cities, Cuisine, History, etc.)
- **Persona:** Travel Planner
- **Job:** "Plan a trip of 4 days for a group of 10 college friends"
- **Output:** Prioritizes nightlife, budget restaurants, group activities

### Test Case 2: Academic Research
- **Documents:** Research papers on specific topics
- **Persona:** PhD Researcher in Computational Biology
- **Job:** "Prepare comprehensive literature review focusing on methodologies"
- **Output:** Methodology sections, performance benchmarks, datasets

### Test Case 3: Business Analysis
- **Documents:** Annual reports from competing companies
- **Persona:** Investment Analyst
- **Job:** "Analyze revenue trends, R&D investments, market positioning"
- **Output:** Financial sections, strategic insights, market data

## Input/Output Format

### Input Structure (`challenge1b_input.json`)
```json
{
  "challenge_info": {
    "challenge_id": "round_1b_002",
    "test_case_name": "travel_planner",
    "description": "France Travel"
  },
  "documents": [
    {"filename": "document1.pdf", "title": "Document Title"},
    {"filename": "document2.pdf", "title": "Document Title"}
  ],
  "persona": {
    "role": "Travel Planner"
  },
  "job_to_be_done": {
    "task": "Plan a trip of 4 days for a group of 10 college friends."
  }
}
```

### Output Structure (`challenge1b_output.json`)
```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
    "processing_timestamp": "2025-07-28T19:18:59.779328"
  },
  "extracted_sections": [
    {
      "document": "South of France - Things to Do.pdf",
      "section_title": "Nightlife and Entertainment",
      "page_number": 11,
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "South of France - Things to Do.pdf",
      "refined_text": "The South of France offers a vibrant nightlife scene, with options ranging from chic bars to lively nightclubs:",
      "page_number": 11
    }
  ]
}
```

## Installation and Usage

### Option 1: Docker (Hackathon Submission Format)
```bash
# Build the Docker image
docker build -t adobe-1b:latest .

# Run the analyzer (processes all Collection_* directories)
docker run --rm -v "$PWD:/app" adobe-1b:latest

# Verify outputs
ls Collection_*/challenge1b_output.json
jq '.metadata' Collection_1/challenge1b_output.json
```

### Option 2: Local Development
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download DistilBERT model (one-time setup)
python download_model.py

# Run the analyzer
python src/main.py

# Check processing results
cat Collection_1/challenge1b_output.json | jq '.extracted_sections[0:3]'
```

## Model and Dependencies

### DistilBERT Configuration
- **Model:** `distilbert-base-uncased` from Hugging Face
- **Size:** ~250MB (well under 1GB hackathon constraint)
- **Purpose:** Semantic relevance scoring for section ranking
- **Download:** Automatic during Docker build via `download_model.py`
- **Storage:** Cached in `models/distilbert/` directory

### Key Dependencies
```txt
pdfminer.six    # PDF text extraction with page mapping
transformers    # DistilBERT model and tokenizer
torch           # PyTorch backend for model inference
```

## Architecture and Customization

### Modular Design
```
src/
├── main.py              # Entry point and collection orchestration
├── pdf_processor.py     # PDF text extraction with page mapping
├── text_analyzer.py     # Section detection, ranking, and analysis
└── utils.py             # JSON I/O and utility functions
```

### Key Algorithms

#### Section Detection (`identify_sections`)
- **Heuristic-based:** Identifies headings using length, capitalization, and pattern matching
- **Configurable:** Adjust heading detection patterns in `text_analyzer.py`
- **Page-aware:** Maintains precise page number mapping

#### Relevance Ranking (`rank_sections`)
- **DistilBERT-powered:** Uses transformer model for semantic scoring
- **Query-based:** Combines persona and job-to-be-done as relevance query
- **Top-K Selection:** Returns top 5 most relevant sections per document

#### Subsection Analysis (`analyze_subsections`)
- **Keyword-driven:** Filters sentences containing persona/task keywords
- **Sentence-level:** Granular analysis for refined content extraction
- **Concise Output:** Limits to 3 most relevant sentences per section

### Performance Characteristics
- **Processing Time:** ~10-30 seconds per collection (3-7 documents)
- **Memory Usage:** ~500MB-1GB during model inference
- **Scalability:** Linear scaling with document count and size

## Testing and Validation

### Sample Collections Included
- **Collection_1:** Travel planning scenario (7 PDFs about South of France)
- **Collection_2:** [Additional test case]
- **Collection_3:** [Additional test case]

### Validation Steps
```bash
# Run analysis on all collections
docker run --rm -v "$PWD:/app" adobe-1b:latest

# Verify output structure
jq '.metadata | keys' Collection_1/challenge1b_output.json
jq '.extracted_sections | length' Collection_1/challenge1b_output.json
jq '.subsection_analysis | length' Collection_1/challenge1b_output.json

# Check section ranking
jq '.extracted_sections[] | select(.importance_rank == 1)' Collection_1/challenge1b_output.json
```

## Troubleshooting

### Common Issues
1. **Model Download Fails:**
   ```bash
   python download_model.py  # Manual download
   ls models/distilbert/     # Verify model files
   ```

2. **PDF Processing Errors:**
   ```bash
   # Check PDF accessibility
   ls Collection_*/PDFs/*.pdf
   # Verify input JSON format
   jq '.' Collection_*/challenge1b_input.json
   ```

3. **Memory/Performance Issues:**
   - Monitor processing time (should be <60 seconds)
   - Check available RAM during model loading
   - Reduce document collection size if needed

### Debug Mode
```bash
# Enable verbose logging
export PYTHONPATH=/app/src
python -c "import logging; logging.basicConfig(level=logging.DEBUG)"
python src/main.py
```
