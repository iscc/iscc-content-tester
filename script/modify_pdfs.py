import os
import shutil
from multiprocessing import Pool
from pathlib import Path
from tqdm import tqdm
import PyPDF2
import pdfplumber

# Configuration
PDF_DIR = "/tmp/openalex-pdfs"
OUTPUT_DIR = "/tmp/iscc-media/modified_pdfs"
CUTOFF_PERCENTAGE = 10  # Remove 10% of text from the end
PROCESS_PDF_COUNT = 10  # Number of PDFs to process
PROCESSES = 16  # Number of processes

def extract_text(args):
    pdf_file, output_dir, cutoff_percentage = args
    with pdfplumber.open(pdf_file) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages)

    cutoff_index = int(len(text) * (1 - cutoff_percentage / 100))
    collapsed_text = text[:cutoff_index]

    pdf_output_dir = os.path.join(output_dir, Path(pdf_file).stem)
    os.makedirs(pdf_output_dir, exist_ok=True)

    output_file = os.path.join(pdf_output_dir, f"{Path(pdf_file).stem}_collapsed.pdf")

    with open(pdf_file, 'rb') as original_file:
        original_pdf = PyPDF2.PdfReader(original_file)

        page_0 = original_pdf.pages[0]
        page_0_width = page_0.mediabox.width
        page_0_height = page_0.mediabox.height
        new_pdf = PyPDF2.PdfWriter()
        new_pdf.add_blank_page(width=page_0_width, height=page_0_height)
        new_pdf.addPage(page_0)
        new_pdf.pages[0].extract_text = lambda: collapsed_text

        for key, value in original_pdf.getDocumentInfo().items():
            new_pdf.addMetadata({key: value})

        with open(output_file, 'wb') as output_pdf:
            new_pdf.write(output_pdf)

    shutil.copy(pdf_file, pdf_output_dir)
    return pdf_file

def process_pdfs(pdf_list, output_dir, cutoff_percentage):
    tasks = [(pdf, output_dir, cutoff_percentage) for pdf in pdf_list]
    with Pool(processes=PROCESSES) as pool:
        progress_bar = tqdm(total=len(tasks), desc="Processing PDFs")
        results = pool.imap_unordered(extract_text, tasks)
        for processed_file in results:
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
