package helpers

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strings"
	"sync"
	"unicode"
)

// OutlineEntry represents a heading in the PDF outline
// PDFData holds the extracted title and outline from a PDF

type OutlineEntry struct {
	Level string `json:"level"` // Heading level (H1, H2, H3)
	Text  string `json:"text"`  // Heading text
	Page  int    `json:"page"`  // Page number
}

type PDFData struct {
	Title   string        `json:"title"`   // PDF title
	Outline []OutlineEntry `json:"outline"` // List of outline entries
}

// ProcessPDF runs pdftotext and extracts structured data from a PDF
func ProcessPDF(pdfPath, _ string) (PDFData, error) {
	var data PDFData
	cmd := exec.Command("pdftotext", "-layout", pdfPath, "-")
	var out bytes.Buffer
	cmd.Stdout = &out
	// Run pdftotext command
	err := cmd.Run()
	if err != nil {
		return PDFData{}, fmt.Errorf("failed to extract text from %s: %v", pdfPath, err)
	}
	pages := strings.Split(out.String(), "\f") // Split text into pages
	if len(pages) == 0 {
		return PDFData{}, fmt.Errorf("no pages found in %s", pdfPath)
	}
	data.Title = ExtractTitle(pages)
	data.Outline = ExtractOutline(pages)
	return data, nil
}

// ExtractTitle finds a prominent title from the first page or repeated headers
func ExtractTitle(pages []string) string {
	if len(pages) == 0 {
		return ""
	}
	lines := strings.Split(pages[0], "\n")
	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line != "" && len(line) > 5 && len(line) < 100 {
			if IsProminent(line) {
				return CleanText(line)
			}
		}
	}
	repeated := FindRepeatedText(pages)
	if repeated != "" {
		return CleanText(repeated)
	}
	return "Untitled"
}

// IsProminent checks if a line looks like a title (supports multilingual)
func IsProminent(line string) bool {
	upperCount := 0
	letterCount := 0
	for _, r := range line {
		if unicode.IsLetter(r) {
			letterCount++
			if unicode.IsUpper(r) {
				upperCount++
			}
		}
	}
	// For non-Latin scripts, rely on length and position
	if letterCount == 0 {
		return false
	}
	// Check for prominence based on uppercase ratio or length
	return (letterCount > 0 && upperCount > letterCount/2) || len(line) > 20
}

// FindRepeatedText detects text that repeats across pages (e.g., headers)
func FindRepeatedText(pages []string) string {
	if len(pages) < 2 {
		return ""
	}
	counts := make(map[string]int)
	for _, page := range pages {
		lines := strings.Split(page, "\n")
		for _, line := range lines {
			line = strings.TrimSpace(line)
			if line != "" && len(line) > 5 && len(line) < 100 {
				counts[line]++
			}
		}
	}
	for text, count := range counts {
		if count > len(pages)/2 {
			return text
		}
	}
	return ""
}

// ExtractOutline detects headings from all pages
func ExtractOutline(pages []string) []OutlineEntry {
	var outline []OutlineEntry
	seen := make(map[string]bool)
	// Enhanced regex for better heading detection
	reHeading := regexp.MustCompile(`^(Section|Chapter|Part|Appendix|Introduction|Conclusion|Abstract|Summary|References|Bibliography)\s+[A-Z\d]*|^[A-Z][A-Za-z\s\-\:\.\d]{3,}$|^\d+\.?\s+[A-Z][A-Za-z\s\-\:]{3,}|^[A-Z\s]{3,}$`)
	for pageNum, page := range pages {
		scanner := bufio.NewScanner(strings.NewReader(page))
		prevIndent := 0
		for scanner.Scan() {
			line := strings.TrimSpace(scanner.Text())
			if line == "" || IsNoise(line, pages) {
				continue // Skip empty or noisy lines
			}
			if reHeading.MatchString(line) && !seen[line] {
				level := DetermineLevel(line, prevIndent)
				outline = append(outline, OutlineEntry{
					Level: level,
					Text:  CleanText(line),
					Page:  pageNum + 1, // Convert to 1-based page numbering
				})
				seen[line] = true
				prevIndent = CountIndent(line)
			}
		}
	}
	return outline
}

// DetermineLevel infers heading level based on indentation and text clues
func DetermineLevel(line string, prevIndent int) string {
	indent := CountIndent(line)
	if indent > prevIndent {
		return "H2" // Sub-level if indented more
	} else if indent < prevIndent {
		return "H1" // Higher level if less indented
	}
	if strings.Contains(line, ":") {
		return "H3" // Colons often indicate sub-sections
	}
	if regexp.MustCompile(`^[A-Z\s]+$`).MatchString(line) {
		return "H1" // All caps for top-level
	}
	return "H2" // Default mid-level
}

// CountIndent counts leading spaces for level inference
func CountIndent(line string) int {
	return len(line) - len(strings.TrimLeft(line, " "))
}

// IsNoise detects repetitive or irrelevant text
func IsNoise(line string, pages []string) bool {
	count := 0
	for _, page := range pages {
		if strings.Contains(page, line) {
			count++
		}
	}
	return count > len(pages)*2 // Appears too often
}

// CleanText removes extra spaces and special characters
func CleanText(text string) string {
	return strings.TrimSpace(regexp.MustCompile(`\s+`).ReplaceAllString(text, " "))
}

// SetupDirectories ensures input and output directories exist
func SetupDirectories(inputDir, outputDir string) error {
	if err := os.MkdirAll(inputDir, 0755); err != nil {
		return fmt.Errorf("Error creating input directory: %v", err)
	}
	if err := os.MkdirAll(outputDir, 0755); err != nil {
		return fmt.Errorf("Error creating output directory: %v", err)
	}
	return nil
}

// GetPDFs returns a list of PDF files in the input directory
func GetPDFs(inputDir string) ([]os.DirEntry, error) {
	files, err := os.ReadDir(inputDir)
	if err != nil {
		return nil, fmt.Errorf("Error reading input directory: %v", err)
	}
	var pdfs []os.DirEntry
	for _, file := range files {
		if !file.IsDir() && strings.ToLower(filepath.Ext(file.Name())) == ".pdf" {
			pdfs = append(pdfs, file)
		}
	}
	return pdfs, nil
}

// ProcessAndWriteJSON processes a PDF and writes its JSON output
func ProcessAndWriteJSON(inputDir, outputDir string, file os.DirEntry) error {
	jsonFileName := strings.TrimSuffix(file.Name(), ".pdf") + ".json"
	jsonPath := filepath.Join(outputDir, jsonFileName)
	pdfPath := filepath.Join(inputDir, file.Name())
	data, err := ProcessPDF(pdfPath, file.Name())
	if err != nil {
		return fmt.Errorf("error processing %s: %v", file.Name(), err)
	}
	jsonData, err := json.MarshalIndent(data, "", "    ")
	if err != nil {
		return fmt.Errorf("error marshaling JSON for %s: %v", file.Name(), err)
	}
	if err := os.WriteFile(jsonPath, jsonData, 0644); err != nil {
		return fmt.Errorf("error writing JSON file for %s: %v", file.Name(), err)
	}
	fmt.Printf("Processed %s -> %s\n", file.Name(), jsonFileName)
	return nil
}

// Worker processes files from the jobs channel and sends errors to errs channel
func Worker(inputDir, outputDir string, jobs <-chan os.DirEntry, errs chan<- error, wg *sync.WaitGroup) {
	defer wg.Done()
	for file := range jobs {
		err := ProcessAndWriteJSON(inputDir, outputDir, file)
		if err != nil {
			errs <- err
		}
	}
}
