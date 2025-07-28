# Adobe Hackathon PDF Collection Analyzer

## Overview
This project is an intelligent PDF collection analyzer that automatically extracts, ranks, and analyzes sections from collections of PDF documents using modern NLP techniques. The solution leverages DistilBERT transformer models for semantic understanding and provides persona-based relevance scoring for document sections.

## Features
- **Intelligent Section Extraction:** Automatically identifies and extracts meaningful sections from PDF documents
- **NLP-Powered Ranking:** Uses DistilBERT transformer model for semantic analysis and relevance scoring
- **Persona-Based Analysis:** Tailors section importance based on specified user personas and job-to-be-done tasks
- **Batch Processing:** Processes multiple document collections simultaneously
- **Modular Architecture:** Clean separation of concerns for maintainability and extensibility
- **Docker Compatible:** Fully containerized for consistent deployment across environments
- **Offline Operation:** Works without network connectivity once model is downloaded

## Requirements
- **CPU Architecture:** AMD64 (x86_64)
- **No GPU dependencies**
- **Python 3.8+**
- **Model:** DistilBERT (automatically downloaded, ~250MB)

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

## How It Works

### 1. Data Flow
1. **Input Processing:** Reads collection configuration from `challenge1b_input.json`
2. **PDF Extraction:** Extracts text from PDFs with precise page-to-text mapping
3. **Section Identification:** Uses NLP techniques to identify document sections
4. **Relevance Ranking:** Scores sections based on persona and job-to-be-done criteria
5. **Subsection Analysis:** Provides refined analysis of important sections
6. **Output Generation:** Saves structured results to `challenge1b_output.json`

### 2. NLP Pipeline
- **Text Extraction:** Uses `pdfminer.six` for robust PDF text extraction
- **Section Detection:** Identifies headings and content blocks using pattern recognition
- **Semantic Analysis:** DistilBERT model analyzes content relevance
- **Ranking Algorithm:** Combines semantic similarity with structural importance

### 3. Input Format
Each collection contains a `challenge1b_input.json` file:
```json
{
  "documents": [
    {"filename": "document1.pdf"},
    {"filename": "document2.pdf"}
  ],
  "persona": {
    "role": "Data Scientist"
  },
  "job_to_be_done": {
    "task": "Extract methodology sections"
  }
}
```

### 4. Output Format
Generated `challenge1b_output.json` contains:
```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "Data Scientist",
    "job_to_be_done": "Extract methodology sections",
    "processing_timestamp": "2024-01-15T10:30:00Z"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "section_title": "Methodology",
      "page_number": 3,
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "refined_text": "Detailed methodology analysis...",
      "page_number": 3
    }
  ]
}
```

## Installation and Usage

### Option 1: Docker (Recommended)
```bash
# Build the Docker image
docker build -t adobe-1b:latest .

# Run the analyzer
docker run --rm -v "$PWD:/app" adobe-1b:latest
```

### Option 2: Local Development
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download the NLP model
python download_model.py

# Run the analyzer
python src/main.py
```

## Model Information
- **Model:** DistilBERT (distilbert-base-uncased)
- **Size:** ~250MB
- **Purpose:** Sequence classification and semantic similarity
- **Download:** Automatic on first run or via `download_model.py`

## Customization

### Adding New Collections
1. Create a new `Collection_X/` directory
2. Add PDF files to `Collection_X/PDFs/`
3. Create `Collection_X/challenge1b_input.json` with your configuration
4. Run the analyzer

### Modifying Analysis Logic
- **Section Detection:** Edit `text_analyzer.py` → `identify_sections()`
- **Ranking Algorithm:** Modify `text_analyzer.py` → `rank_sections()`
- **Subsection Analysis:** Customize `text_analyzer.py` → `analyze_subsections()`

### Performance Tuning
- Adjust logging levels in `main.py`
- Modify batch processing parameters
- Optimize model inference settings

## Architecture Benefits
- **Modularity:** Each component has a single responsibility
- **Scalability:** Easy to add new document types or analysis methods
- **Maintainability:** Clean interfaces between modules
- **Extensibility:** Simple to integrate new NLP models or techniques
- **Robustness:** Comprehensive error handling and logging

## Troubleshooting

### Common Issues
1. **Model Download Fails:** Run `python download_model.py` manually
2. **PDF Extraction Errors:** Check PDF file integrity and permissions
3. **Memory Issues:** Reduce batch size or use smaller model variant
4. **Docker Build Fails:** Ensure sufficient disk space for model download

### Logging
The application provides detailed logging for debugging:
- INFO: Processing progress and status
- WARNING: Non-critical issues (missing files, etc.)
- ERROR: Critical failures requiring attention

---

*Part of Adobe All India Hackathon submission*
