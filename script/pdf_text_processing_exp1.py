import os
import shutil
from functools import partial
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from pathlib import Path
from tika import parser
import warnings

# Configuration
PDF_DIR = "/iscc/openalex-pdfs"
OUTPUT_DIR = "/iscc/txt_exp1"
CUTOFF_PERCENTAGE = 10  # Remove 10% of text from the beginning of the half text
PROCESS_PDF_COUNT = 1000  # Number of PDFs to process
PROCESSES = 16  # Number of processes

def extract_and_modify_pdf(output_dir, cutoff_percentage, input_pdf):
    try:
        # Parse the PDF using Tika
        parsed_pdf = parser.from_file(input_pdf)
        original_text = parsed_pdf['content']

        # Calculate the number of characters to remove (10% of the beginning of the half text)
        text_length = len(original_text)
        remove_chars = int(text_length * cutoff_percentage / 100 // 2)

        # Split the text into the original and the modified parts
        modified_text = original_text[remove_chars:]

        output_file = os.path.join(output_dir, f"{Path(input_pdf).stem}.txt")
        with open(output_file, 'w', encoding='utf-8') as modified_file:
            modified_file.write(modified_text)

    except Exception as e:
        print(f"Error processing {input_pdf}: {e}")
        return input_pdf

    return input_pdf

def process_pdfs(pdf_list, output_dir, cutoff_percentage):
    with Pool(PROCESSES) as pool:
        func = partial(extract_and_modify_pdf, output_dir, cutoff_percentage)
        progress_bar = tqdm(total=len(pdf_list), desc="Processing PDFs")
        for processed_file in pool.imap_unordered(func, pdf_list):
            progress_bar.update(1)
            progress_bar.set_postfix({"Processed": Path(processed_file).name})
    progress_bar.close()

if __name__ == "__main__":
    pdf_files = [os.path.join(PDF_DIR, f) for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    pdf_files = pdf_files[:PROCESS_PDF_COUNT]
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Parameters:")
    print(f"PDF Directory: {PDF_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Cutoff Percentage: {CUTOFF_PERCENTAGE}%")
    print(f"Number of PDFs to process: {PROCESS_PDF_COUNT}")
    print(f"Number of processes: {PROCESSES}\n")

    process_pdfs(pdf_files, OUTPUT_DIR, CUTOFF_PERCENTAGE)
