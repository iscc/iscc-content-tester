# ISCC PDF Content Extractor and Tester

This repository contains two scripts:
1. `download_pdfs_from_mongo.py`: Downloads a specified number of PDFs from a MongoDB collection using the provided credentials.
2. `pdf_text_extractor.py`: Extracts text from a specified number of PDF files, removes a percentage of text from the beginning, and saves the remaining text as plain text files. It uses Apache Tika for text extraction and multiprocessing for faster processing.

## Development Requirements

- Python 3.6+
- pymongo (Python library)
- requests (Python library)
- tqdm (Python library)
- Apache Tika (Python library)
- iscc-sdk (Python library)

## Development Installation

1. Clone the repository:

<<<<<<< HEAD


\```
=======
```
>>>>>>> 9369d40154688aea3505aadbb646d729ad778a48
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

### Downloading PDFs from MongoDB

1. Modify the configuration variables in the `download_pdfs_from_mongo.py` script to suit your needs:

\```python
USERNAME = 'user'
PASSWORD = 'passwort'
DOWNLOAD_FOLDER = 'downloads'  # Default download folder
NUM_FILES = 5  # Default number of files to download
\```
Replace user and passwort with your MongoDB credentials.

2. Run the script:
\```python
python download_pdfs_from_mongo.py <username> <password> <download_folder> <num_files>
\```

Replace <username>, <password>, <download_folder>, and <num_files> with your MongoDB credentials, the desired download folder, and the number of files you want to download, respectively.

### Extracting Text from PDFs

1. Modify the configuration variables in the `modify_pdfs.py` script to suit your needs:

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
