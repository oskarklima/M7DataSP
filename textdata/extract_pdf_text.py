"""
PDF Text Extraction Script
Extracts text from PDF files using pdfplumber library
"""

import pdfplumber

def extract_text_from_pdf(pdf_path, output_path=None):
    """
    Extract text from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_path (str, optional): Path to save extracted text. If None, prints to console.
    
    Returns:
        str: Extracted text
    """
    extracted_text = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Processing {len(pdf.pages)} pages...")
            
            for i, page in enumerate(pdf.pages, 1):
                print(f"Extracting page {i}...")
                text = page.extract_text()
                if text:
                    extracted_text.append(f"--- Page {i} ---\n{text}\n")
        
        full_text = "\n".join(extracted_text)
        
        # Save to file if output path is provided
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_text)
            print(f"\nText saved to: {output_path}")
        else:
            print("\n" + "="*50)
            print("EXTRACTED TEXT:")
            print("="*50)
            print(full_text)
        
        return full_text
    
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

if __name__ == "__main__":
    # Extract text from the PDF
    pdf_file = "9427.pdf"
    output_file = "9427_extracted_text.txt"
    
    extract_text_from_pdf(pdf_file, output_file)
