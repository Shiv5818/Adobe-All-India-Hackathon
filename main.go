package main

import (
	"fmt"
	"os"
	"sync"
	"adobe-A1/helpers"
)

func main() {
	const inputDir = "./input"      // Directory containing PDF files
	const outputDir = "./output"    // Directory to store JSON outputs
	const numWorkers = 4            // Number of concurrent workers

	// Ensure input and output directories exist
	if err := helpers.SetupDirectories(inputDir, outputDir); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	// Get list of PDF files to process
	pdfs, err := helpers.GetPDFs(inputDir)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	jobs := make(chan os.DirEntry, len(pdfs)) // Channel for PDF jobs
	errChan := make(chan error, len(pdfs))     // Channel for errors
	var wg sync.WaitGroup                     // WaitGroup for worker synchronization

	// Start worker pool for concurrent processing
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go helpers.Worker(inputDir, outputDir, jobs, errChan, &wg)
	}

	// Send PDF files to workers
	for _, file := range pdfs {
		jobs <- file
	}
	close(jobs)

	wg.Wait()      // Wait for all workers to finish
	close(errChan) // Close error channel

	// Print errors if any occurred during processing
	var hadError bool
	for err := range errChan {
		fmt.Println(err)
		hadError = true
	}
	if hadError {
		os.Exit(1)
	}
}