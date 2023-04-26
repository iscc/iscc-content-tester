import os
import shutil
import tika
from tika import parser
from multiprocessing import Pool, cpu_count, Queue
from tqdm import tqdm
from pathlib import Path
from iscc_sdk import text_extract
import PyPDF2
from io import BytesIO

# Configuration
PDF_DIR = "/tmp/openalex-pdfs"
OUTPUT_DIR = "/tmp/iscc-media/modified_pdfs"
CUTOFF_PERCENTAGE = 10  # Remove 10% of text from the end
PROCESS_PDF_COUNT = 10  # Number of PDFs to process
PROCESSES = cpu_count()  # Number of parallel processes

def init_tika(queue):
    global TIKA_QUEUE
    TIKA_QUEUE = queue
    tika.initVM()

def extract_text(args):
    pdf_file, output_dir, cutoff_percentage = args
    parsed_pdf = parser.from_file(pdf_file)
    text = parsed_pdf['content']

    collapsed_text = textid.text_collapse(text)
    cutoff_index = int(len(text) * (1 - cutoff_percentage / 100))
    collapsed_text = text[:cutoff_index]

    pdf_output_dir = os.path.join(output_dir, Path(pdf_file).stem)
    os.makedirs(pdf_output_dir, exist_ok=True)

    output_file = os.path.join(pdf_output_dir, f"{Path(pdf_file).stem}_collapsed.pdf")

    with open(pdf_file, 'rb') as original_file:
        original_pdf = PyPDF2.PdfReader(original_file)

        new_pdf = PyPDF2.PdfFileWriter()
        new_pdf.addBlankPage()
        new_pdf.addPage(original_pdf.getPage(0))
        new_pdf.pages[0].extract_text = lambda: collapsed_text

        for key, value in original_pdf.getDocumentInfo().items():
            new_pdf.addMetadata({key: value})

        with open(output_file, 'wb') as output_pdf:
            new_pdf.write(output_pdf)

    shutil.copy(pdf_file, pdf_output_dir)
    return pdf_file

def process_pdfs(pdf_list, output_dir, cutoff_percentage):
    queue = Queue()
    with Pool(PROCESSES, initializer=init_tika, initargs=(queue,)) as pool:
        tasks = [(pdf, output_dir, cutoff_percentage) for pdf in pdf_list]
        progress_bar = tqdm(total=len(tasks), desc="Processing PDFs")
        for processed_file in pool.imap_unordered(extract_text, tasks):
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
    print(f"Number of parallel processes: {PROCESSES}\n")

    process_pdfs(pdf_files, OUTPUT_DIR, CUTOFF_PERCENTAGE)
