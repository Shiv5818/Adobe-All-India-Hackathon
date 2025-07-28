# Adobe Hackathon PDF to JSON Converter

## Overview
This project is a scalable Go application that automatically processes all PDF files in a specified input directory and generates corresponding JSON files in an output directory. It is designed for offline use, works on AMD64 (x86_64) architecture, and is fully containerized for easy deployment.

## Features
- **Automatic PDF Processing:** Scans the `/app/input` directory for all `.pdf` files and generates a `.json` file for each in `/app/output`.
- **Concurrent Processing:** Uses a worker pool for fast, parallel conversion of multiple PDFs.
- **Structured Output:** Each JSON file contains the extracted title and outline (headings) from the PDF.
- **Offline Operation:** No network calls; all processing is local.
- **Docker Compatible:** Ready for build and run on AMD64 Linux systems.

## Requirements
- **CPU Architecture:** AMD64 (x86_64)
- **No GPU dependencies**
- **Works offline**
- **Model size ≤ 200MB** (no ML model used)
- **Poppler-utils** (for `pdftotext`)

## Directory Structure
```
├── Dockerfile
├── go.mod
├── go.sum
├── main.go
├── helpers/
│   └── helpers.go
├── input/
│   ├── file01.pdf
│   └── ...
├── output/
│   ├── file01.json
│   └── ...
```

## Approach
This solution uses Go for its concurrency and performance. The application leverages a worker pool to process multiple PDFs in parallel, making it scalable for large batches. Text extraction is performed using the `pdftotext` utility (from poppler-utils), which is installed in the Docker container. The extracted text is parsed to identify the document title and outline (headings), which are then saved in structured JSON files.

## Models or Libraries Used
- **Go standard library** for concurrency, file I/O, and JSON handling
- **poppler-utils (pdftotext)** for PDF text extraction (installed in the container)
- No machine learning models are used; all logic is rule-based and deterministic

## How It Works
1. **Startup:** The application ensures the input and output directories exist.
2. **Discovery:** It finds all `.pdf` files in `/app/input`.
3. **Processing:** Each PDF is processed using `pdftotext` (from poppler-utils), extracting the title and outline.
4. **Output:** For each PDF, a JSON file with the same base name is written to `/app/output`.

## Output Format
Each output JSON file contains:
- `title`: The detected title of the PDF.
- `outline`: An array of headings with their level and page number.

Example:
```json
{
  "title": "Application form for grant of LTC advance",
  "outline": [
    { "level": "H2", "text": "Application form for grant of LTC advance", "page": 0 },
    { "level": "H2", "text": "Date of entering the Central Government", "page": 0 }
  ]
}
```

## Customization
- Adjust the number of workers in `main.go` (`numWorkers`) for performance tuning.
- Modify extraction logic in `helpers/helpers.go` for different PDF structures.

## How to Build and Run
1. **Build the Docker image:**
   ```bash
   docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
   ```
2. **Run the container:**
   ```bash
   docker run --rm \
     -v $(pwd)/input:/app/input \
     -v $(pwd)/output:/app/output \
     --network none \
     mysolutionname:somerandomidentifier
   ```
   - Place your PDF files in the `input/` directory before running.
   - The output JSON files will appear in the `output/` directory.

---

