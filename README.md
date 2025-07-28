# Adobe All India Hackathon: Connecting the Dots Challenge

This repository contains solutions for the Adobe All India Hackathon "Connecting the Dots" challenge, implementing intelligent PDF processing systems that transform static documents into interactive, context-aware experiences.

## 🏗️ Project Structure

```
Adobe-All-India-Hackathon/
├── Adobe_1A/          # Challenge 1A: PDF to JSON Converter (Go)
├── Adobe_1B/          # Challenge 1B: PDF Collection Analyzer (Python)
└── README.md          # This file
```

## � Round-by-Round Solutions

### Round 1A: PDF Structure Extraction
**Adobe_1A** - Extracts structured outlines from PDFs with title and hierarchical headings (H1, H2, H3)
- **Language:** Go
- **Focus:** High-performance concurrent processing
- **Output:** JSON format with document structure

### Round 1B: Persona-Driven Document Intelligence
**Adobe_1B** - Analyzes document collections using NLP to prioritize content based on user personas and tasks
- **Language:** Python
- **Focus:** AI-powered relevance ranking
- **Output:** Persona-tailored section analysis

## 🚀 Quick Start

### Prerequisites
- Docker (recommended for both solutions)
- Go 1.19+ (for Adobe_1A local development)
- Python 3.8+ (for Adobe_1B local development)

### Running the Solutions
```bash
# Adobe_1A: PDF to JSON Converter
cd Adobe_1A
docker build --platform linux/amd64 -t adobe-1a .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none adobe-1a

# Adobe_1B: Persona-Driven Analyzer
cd Adobe_1B
docker build -t adobe-1b .
docker run --rm -v "$PWD:/app" adobe-1b
```

## 📁 Input/Output

### Adobe_1A
- **Input:** PDF files → **Output:** Structured JSON with titles and headings

### Adobe_1B
- **Input:** PDF collections + persona/task → **Output:** Ranked relevant sections

## � Documentation

Detailed setup and usage instructions:
- [Adobe_1A README](./Adobe_1A/README.md) - PDF structure extraction
- [Adobe_1B README](./Adobe_1B/README.md) - Persona-driven analysis

## 🏆 Hackathon Compliance

✅ Offline operation
✅ AMD64 architecture
✅ Docker containerization
✅ Performance requirements
✅ No GPU dependencies

---

*Adobe All India Hackathon: Connecting the Dots Challenge*