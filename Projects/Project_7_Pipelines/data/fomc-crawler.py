import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def get_press_conference_pages(base_url="https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    
    try:
        # Fetch the calendar page
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all "Press Conference" links
        press_conf_links = []
        for link in soup.find_all('a', href=True):
            if "Press Conference" in link.text and "fomcpresconf" in link['href'].lower():
                full_url = urljoin("https://www.federalreserve.gov", link['href'])
                press_conf_links.append(full_url)
        
        return press_conf_links
        
    except Exception as e:
        print(f"Error finding press conference pages: {str(e)}")
        return []

def get_transcript_pdf_url(press_conf_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    
    try:
        response = requests.get(press_conf_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the "Transcript (PDF)" link
        for link in soup.find_all('a', href=True):
            if "Transcript (PDF)" in link.text:
                return urljoin("https://www.federalreserve.gov", link['href'])
        
        return None
        
    except Exception as e:
        print(f"\nError accessing press conference page {press_conf_url}: {str(e)}")
        return None

def download_pdf(url, output_dir):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/pdf,*/*'
    }
    
    try:
        pdf_name = url.split('/')[-1]
        output_path = os.path.join(output_dir, pdf_name)
        
        # Skip if file already exists
        if os.path.exists(output_path):
            print(f"\nSkipping {pdf_name} (already exists)")
            return True
            
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"\nSuccessfully downloaded: {pdf_name}")
        return True
        
    except Exception as e:
        print(f"\nError downloading {url}: {str(e)}")
        return False

def main():
    # Create downloads directory
    output_dir = './data/fomc_transcripts'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get all press conference pages
    print("Finding press conference pages...")
    press_conf_pages = get_press_conference_pages()
    
    if not press_conf_pages:
        print("No press conference pages found!")
        return
    
    print(f"\nFound {len(press_conf_pages)} press conference pages.")
    
    # Get and download PDFs from each page
    pdf_urls = []
    print("\nGathering transcript PDF links...")
    for page_url in tqdm(press_conf_pages):
        pdf_url = get_transcript_pdf_url(page_url)
        if pdf_url:
            pdf_urls.append(pdf_url)
        time.sleep(0.1)  # Be nice to the server
    
    if not pdf_urls:
        print("No transcript PDFs found!")
        return
    
    print(f"\nFound {len(pdf_urls)} transcript PDFs to download:")
    for url in pdf_urls:
        print(f"- {url}")
    
    # proceed = input("\nProceed with download? (y/n): ")
    # if proceed.lower() != 'y':
    #     print("Download cancelled")
    #     return
    
    print("\nDownloading PDFs...")
    for url in tqdm(pdf_urls):
        download_pdf(url, output_dir)
        time.sleep(1)  # Be nice to the server
    
    print("\nDownload process completed!")

if __name__ == "__main__":
    main()