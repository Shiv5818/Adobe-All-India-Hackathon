# Adobe All India Hackathon Solutions

This repository contains solutions for the Adobe All India Hackathon challenges, implementing two distinct PDF processing solutions.

## 🏗️ Project Structure

```
Adobe-All-India-Hackathon/
├── Adobe_1A/          # Challenge 1A: PDF to JSON Converter (Go)
├── Adobe_1B/          # Challenge 1B: PDF Collection Analyzer (Python)
└── README.md          # This file
```

## 📋 Solutions Overview

### Adobe_1A - PDF to JSON Converter
**Language:** Go
**Purpose:** Converts PDF files to structured JSON format with title and outline extraction

**Key Features:**
- Concurrent PDF processing with worker pools
- Offline operation (no network dependencies)
- Docker containerized for AMD64 architecture
- Extracts document titles and hierarchical outlines
- Batch processing of multiple PDFs

### Adobe_1B - PDF Collection Analyzer
**Language:** Python
**Purpose:** Analyzes collections of PDFs using NLP for section ranking and analysis

**Key Features:**
- NLP-powered section identification and ranking
- Persona-based relevance scoring
- DistilBERT transformer model integration
- Modular architecture for scalability
- Batch processing of document collections

## 🚀 Quick Start

### Prerequisites
- Docker (recommended)
- Go 1.19+ (for Adobe_1A local development)
- Python 3.8+ (for Adobe_1B local development)

### Running Adobe_1A (PDF to JSON)
```bash
cd Adobe_1A
# Build Docker image
docker build --platform linux/amd64 -t adobe-1a:latest .

# Run with your PDFs
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  adobe-1a:latest
```

### Running Adobe_1B (PDF Analyzer)
```bash
cd Adobe_1B
# Build Docker image
docker build -t adobe-1b:latest .

# Run analysis
docker run --rm -v "$PWD:/app" adobe-1b:latest
```

## 📁 Input/Output Formats

### Adobe_1A
- **Input:** PDF files in `input/` directory
- **Output:** JSON files with extracted titles and outlines

### Adobe_1B
- **Input:** Collection directories with PDFs and configuration JSON
- **Output:** Analyzed sections with importance rankings

## 🛠️ Development

Each solution includes detailed README files with specific setup instructions:
- [Adobe_1A README](./Adobe_1A/README.md) - Go-based PDF converter
- [Adobe_1B README](./Adobe_1B/README.md) - Python-based PDF analyzer

## 📊 Architecture Highlights

- **Adobe_1A:** Leverages Go's concurrency for high-performance PDF processing
- **Adobe_1B:** Uses modern NLP techniques with transformer models for intelligent analysis
- Both solutions are containerized for consistent deployment across environments

## 🏆 Hackathon Compliance

Both solutions meet the hackathon requirements:
- ✅ Offline operation capability
- ✅ AMD64 architecture support
- ✅ Docker containerization
- ✅ Model size constraints (where applicable)
- ✅ No GPU dependencies

---

*Developed for Adobe All India Hackathon*