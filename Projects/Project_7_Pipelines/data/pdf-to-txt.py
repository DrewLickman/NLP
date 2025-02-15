import pdfplumber
import os
from typing import Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_fomc_transcript(text: str) -> str:
    """
    Clean FOMC transcript text by removing specific formatting elements.
    
    Args:
        text (str): The raw transcript text
        
    Returns:
        str: The cleaned transcript text
    """
    # Split text into lines
    lines = text.split('\n')
    
    # Remove first 3 and last line if they exist
    if len(lines) > 4:  # Only remove if we have enough lines
        lines = lines[3:-1]
    
    # Find page breaks and their surrounding lines
    indices_to_remove = set()
    for i, line in enumerate(lines):
        if "=== Page Break ===" in line:
            # Mark the page break and two lines before and after for removal
            for j in range(max(0, i-2), min(len(lines), i+3)):
                indices_to_remove.add(j)
    
    # Create new list with clean lines
    cleaned_lines = [line for i, line in enumerate(lines) if i not in indices_to_remove]
    
    # Join lines back together
    return '\n'.join(cleaned_lines)

def extract_text_from_pdf(
    pdf_path: str,
    output_path: Optional[str] = None,
    page_numbers: Optional[list[int]] = None,
    clean_fomc: bool = True
) -> str:
    """
    Extract text from a PDF file, optionally clean it, and save it to a text file.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_path (str, optional): Path where to save the extracted text
        page_numbers (list[int], optional): List of specific pages to extract (0-based index)
        clean_fomc (bool): Whether to apply FOMC transcript cleaning
    
    Returns:
        str: Extracted text from the PDF
    
    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        ValueError: If the PDF file is invalid or corrupted
    """
    try:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        with pdfplumber.open(pdf_path) as pdf:
            # If no specific pages are requested, extract all pages
            if page_numbers is None:
                page_numbers = range(len(pdf.pages))
            
            # Validate page numbers
            max_pages = len(pdf.pages)
            valid_pages = [p for p in page_numbers if 0 <= p < max_pages]
            if len(valid_pages) != len(page_numbers):
                logging.warning(f"Some requested pages are out of range. PDF has {max_pages} pages.")
            
            # Extract text from specified pages
            text_content = []
            for page_num in valid_pages:
                page = pdf.pages[page_num]
                text_content.append(page.extract_text() or '')
            
            # Combine all text with page separators
            full_text = "\n\n=== Page Break ===\n\n".join(text_content)
            
            # Clean the text if requested
            if clean_fomc:
                full_text = clean_fomc_transcript(full_text)
            
            # Save to file if output path is provided
            if output_path:
                output_dir = os.path.dirname(output_path)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(full_text)
            
            return full_text

    except Exception as e:
        logging.error(f"Error processing PDF: {str(e)}")
        raise

def batch_convert_pdfs(
    input_dir: str,
    output_dir: str,
    clean_fomc: bool = True
) -> None:
    """
    Convert all PDFs in a directory to text files.
    
    Args:
        input_dir (str): Directory containing PDF files
        output_dir (str): Directory where text files will be saved
        clean_fomc (bool): Whether to apply FOMC transcript cleaning
    """
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        txt_file = os.path.splitext(pdf_file)[0] + '.txt'
        txt_path = os.path.join(output_dir, txt_file)
        
        # Skip if text file already exists
        if os.path.exists(txt_path):
            logging.info(f"Skipping {txt_file} (already exists)")
            continue
            
        try:
            extract_text_from_pdf(pdf_path, txt_path, clean_fomc=clean_fomc)
            logging.info(f"Successfully generated {txt_file}")
        except Exception as e:
            logging.error(f"Failed to convert {pdf_file}: {str(e)}")
            continue

if __name__ == "__main__":
    input_directory = "./data/fomc_transcripts"
    output_directory = "./data/extracted_text"
    try:
        batch_convert_pdfs(input_directory, output_directory, clean_fomc=True)
        print("Batch conversion completed successfully!")
    except Exception as e:
        print(f"Error during batch conversion: {str(e)}")