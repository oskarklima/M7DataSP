"""
Extract text from all downloaded PDFs and combine into one file
Processes all PDFs in the matematika_pdfs directory
"""

import pdfplumber
import os
from pathlib import Path

# Configuration
PDF_DIR = "matematika_pdfs"
OUTPUT_FILE = "matematika_all_text.txt"

def get_all_pdf_files(directory):
    """Recursively find all PDF files in directory"""
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in sorted(files):  # Sort for consistent ordering
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return sorted(pdf_files)  # Sort again by full path

def extract_text_from_pdf(pdf_path):
    """Extract text from a single PDF file"""
    try:
        text_content = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
        return "\n".join(text_content)
    except Exception as e:
        print(f"  ✗ Error extracting {pdf_path}: {e}")
        return None

def main():
    """Main function to extract all PDFs"""
    print("="*70)
    print("PDF Text Extraction - All Files")
    print("="*70)
    
    # Check if directory exists
    if not os.path.exists(PDF_DIR):
        print(f"Error: Directory '{PDF_DIR}' not found!")
        print("Please run download_all_pdfs.py first.")
        return
    
    # Get all PDF files
    print(f"\nScanning directory: {PDF_DIR}")
    pdf_files = get_all_pdf_files(PDF_DIR)
    print(f"Found {len(pdf_files)} PDF files\n")
    
    if not pdf_files:
        print("No PDF files found!")
        return
    
    # Extract text from all PDFs
    all_text = []
    successful = 0
    failed = 0
    
    for i, pdf_path in enumerate(pdf_files, 1):
        # Get relative path for display
        rel_path = os.path.relpath(pdf_path, PDF_DIR)
        print(f"[{i}/{len(pdf_files)}] Processing: {rel_path}")
        
        # Extract text
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            # Add text without any header
            all_text.append(text)
            successful += 1
            print(f"  ✓ Extracted successfully")
        else:
            failed += 1
    
    # Save to file
    print(f"\n{'='*70}")
    print("Saving combined text...")
    print(f"{'='*70}")
    
    combined_text = "\n\n".join(all_text)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(combined_text)
    
    # Statistics
    file_size = os.path.getsize(OUTPUT_FILE)
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"\n{'='*70}")
    print("EXTRACTION SUMMARY")
    print(f"{'='*70}")
    print(f"Total PDFs processed: {len(pdf_files)}")
    print(f"Successfully extracted: {successful}")
    print(f"Failed: {failed}")
    print(f"\nOutput file: {OUTPUT_FILE}")
    print(f"File size: {file_size:,} bytes ({file_size_mb:.2f} MB)")
    print(f"Full path: {os.path.abspath(OUTPUT_FILE)}")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
