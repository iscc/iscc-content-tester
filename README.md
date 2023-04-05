# ISCC PDF Content Extractor and Tester

This script extracts text from a specified number of PDF files, removes a percentage of text from the beginning, and saves the remaining text as plain text files. It uses Apache Tika for text extraction and multiprocessing for faster processing.

## Development Requirements

- Python 3.6+
- Apache Tika (Python library)
- tqdm (Python library)
- iscc-sdk (Python library)

## Development Installation

1. Clone the repository:

```
git clone https://github.com/wollooo/pdf-text-extractor.git
cd pdf-text-extractor
```

2. Create a virtual environment and activate it:

```
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Modify the configuration variables in the script to suit your needs:

```python
PDF_DIR = "/path/to/pdf/directory"
OUTPUT_DIR = "/path/to/output/directory"
CUTOFF_PERCENT = 10  # Remove 10% of text from the beginning
PROCESS_PDF_COUNT = 10  # Number of PDFs to process
PROCESSES = cpu_count()  # Number of parallel processes
```

Replace `/path/to/pdf/directory` and `/path/to/output/directory` with the paths to the input and output directories, respectively. You can modify the `CUTOFF_PERCENT` and `PROCESS_PDF_COUNT` variables to change the percentage of text to remove and the number of PDFs to process, respectively.

2. Run the script:

```
python scripts/pdf_text_extractor.py
```

The script will process the specified PDF files in the input directory, remove the specified percentage of text from the beginning, and save the remaining text as plain text files in the output directory.
