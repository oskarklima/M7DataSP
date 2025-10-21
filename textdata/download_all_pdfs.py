"""
Script to download all PDF files from Matematika v dialógoch website
Downloads PDFs from all topic pages listed on the main page
"""

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import time

# Configuration
BASE_URL = "https://www.galeje.sk/predmety/matematika/matematika-v-dialogoch/"
DOWNLOAD_DIR = "matematika_pdfs"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def create_download_directory():
    """Create the download directory if it doesn't exist"""
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        print(f"Created directory: {DOWNLOAD_DIR}")

def get_topic_links(main_url):
    """Extract all topic page links from the main page"""
    print(f"Fetching main page: {main_url}")
    response = requests.get(main_url, headers=HEADERS)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all links that are topic pages
    topic_links = []
    
    # Look for links within the main content area
    # These are the topic links like "Výroková logika", "Výrazy", etc.
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Topic pages end with a category name followed by /
        if '/matematika-v-dialogoch/' in href and href != main_url and href.endswith('/'):
            full_url = urljoin(main_url, href)
            if full_url not in topic_links:
                topic_links.append(full_url)
                print(f"  Found topic: {link.get_text(strip=True)} - {full_url}")
    
    return topic_links

def get_pdf_links_from_topic(topic_url):
    """Extract all PDF links from a topic page"""
    print(f"\nFetching topic page: {topic_url}")
    response = requests.get(topic_url, headers=HEADERS)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    pdf_links = []
    
    # Find all links pointing to PDF files
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '.pdf' in href.lower():
            full_url = urljoin(topic_url, href)
            pdf_name = link.get_text(strip=True)
            pdf_links.append((full_url, pdf_name))
            print(f"  Found PDF: {pdf_name}")
    
    return pdf_links

def sanitize_filename(filename):
    """Remove or replace invalid characters in filenames"""
    # Replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    return filename

def download_pdf(url, pdf_name, topic_name):
    """Download a single PDF file"""
    try:
        # Create subdirectory for the topic
        topic_dir = os.path.join(DOWNLOAD_DIR, sanitize_filename(topic_name))
        if not os.path.exists(topic_dir):
            os.makedirs(topic_dir)
        
        # Extract filename from URL if pdf_name is not suitable
        url_filename = os.path.basename(urlparse(url).path)
        
        # Create a clean filename combining the description and URL filename
        if pdf_name and pdf_name != url_filename:
            # Use both the description and the numeric ID from URL
            clean_name = sanitize_filename(pdf_name)
            filename = f"{clean_name}_{url_filename}"
        else:
            filename = url_filename
        
        filepath = os.path.join(topic_dir, filename)
        
        # Check if file already exists
        if os.path.exists(filepath):
            print(f"  ✓ Already exists: {filename}")
            return True
        
        # Download the PDF
        print(f"  ⬇ Downloading: {filename}")
        response = requests.get(url, headers=HEADERS, stream=True)
        response.raise_for_status()
        
        # Save the PDF
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"  ✓ Downloaded: {filename}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error downloading {url}: {e}")
        return False

def main():
    """Main function to orchestrate the download process"""
    print("="*70)
    print("PDF Downloader for Matematika v dialógoch")
    print("="*70)
    
    create_download_directory()
    
    # Step 1: Get all topic page links
    print("\n" + "="*70)
    print("STEP 1: Finding all topic pages")
    print("="*70)
    topic_links = get_topic_links(BASE_URL)
    print(f"\nFound {len(topic_links)} topic pages")
    
    # Step 2: Download PDFs from each topic page
    print("\n" + "="*70)
    print("STEP 2: Downloading PDFs from each topic")
    print("="*70)
    
    total_pdfs = 0
    downloaded_pdfs = 0
    
    for topic_url in topic_links:
        # Extract topic name from URL
        topic_name = topic_url.rstrip('/').split('/')[-1].replace('-', ' ').title()
        
        print(f"\n{'='*70}")
        print(f"Topic: {topic_name}")
        print(f"{'='*70}")
        
        # Get all PDF links from this topic page
        pdf_links = get_pdf_links_from_topic(topic_url)
        total_pdfs += len(pdf_links)
        
        # Download each PDF
        for pdf_url, pdf_name in pdf_links:
            if download_pdf(pdf_url, pdf_name, topic_name):
                downloaded_pdfs += 1
            time.sleep(0.5)  # Be nice to the server
    
    # Summary
    print("\n" + "="*70)
    print("DOWNLOAD SUMMARY")
    print("="*70)
    print(f"Total PDFs found: {total_pdfs}")
    print(f"Successfully downloaded/verified: {downloaded_pdfs}")
    print(f"Download directory: {os.path.abspath(DOWNLOAD_DIR)}")
    print("="*70)

if __name__ == "__main__":
    main()
