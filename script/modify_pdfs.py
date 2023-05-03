import os
import shutil
from functools import partial
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from pathlib import Path
from PyPDF4 import PdfFileReader, PdfFileWriter
import warnings
from PyPDF4.utils import PdfReadWarning
warnings.filterwarnings("ignore", category=PdfReadWarning)

# Configuration
PDF_DIR = "/iscc/openalex-pdfs"
OUTPUT_DIR = "/iscc/pdfs"
CUTOFF_PERCENTAGE = 10  # Remove 10% of text from the end
PROCESS_PDF_COUNT = 1000  # Number of PDFs to process
PROCESSES = 1  # Number of processes

def extract_and_modify_pdf(output_dir, cutoff_percentage, input_pdf):
    pdf_folder_name = Path(input_pdf).stem
    pdf_output_dir = os.path.join(output_dir, pdf_folder_name)

    try:
        with open(input_pdf, 'rb') as original_file:
            original_pdf = PdfFileReader(original_file)

            # Decrypt the PDF if it is encrypted
            if original_pdf.isEncrypted:
                try:
                    original_pdf.decrypt('')
                except Exception as e:
                    print(f"Error decrypting {input_pdf}: {e}")
                    return input_pdf

            os.makedirs(pdf_output_dir, exist_ok=True)

            output_pdf = os.path.join(pdf_output_dir, f"{pdf_folder_name}_collapsed.pdf")
            original_pdf_path = os.path.join(pdf_output_dir, os.path.basename(input_pdf))

            new_pdf = PdfFileWriter()

            # Copy metadata
            for key, value in original_pdf.getDocumentInfo().items():
                new_pdf.addMetadata({key: str(value)})

            # Calculate the number of pages to keep (90%)
            num_pages = original_pdf.getNumPages()
            keep_pages = int(num_pages * (1 - cutoff_percentage / 100))

            # Add the first 90% of the pages to the new PDF
            for i in range(keep_pages):
                new_pdf.addPage(original_pdf.getPage(i))

            # Save the new PDF
            with open(output_pdf, 'wb') as output_file:
                new_pdf.write(output_file)

    except Exception as e:
        print(f"Error processing {input_pdf}: {e}")
        return input_pdf
    finally:
        # Copy the original PDF to the output directory even if an error occurs
        if not os.path.exists(pdf_output_dir):
            os.makedirs(pdf_output_dir, exist_ok=True)
        original_pdf_path = os.path.join(pdf_output_dir, os.path.basename(input_pdf))
        shutil.copy(input_pdf, original_pdf_path)

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
