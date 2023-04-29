#Release memory every 50 files

import os
import pdfplumber
from multiprocessing import Pool
import logging
import gc

# Configure the logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

source_dir = r'your_pdf_path'
target_dir = r'your_txt_path'

# Check if the target directory exists, if not, create it
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

count = 0


def pdf_to_txt(file_path):
    # Global variable to count the number of processed PDF files
    global count
    try:
        # Open the PDF file
        with pdfplumber.open(file_path) as pdf:
            text = ''
            # Extract text from all pages
            for page in pdf.pages:
                text += page.extract_text()
        # Get the file name of TXT file
        txt_file_name = os.path.basename(file_path).replace('.pdf', '.txt')
        # Get the full path of TXT file
        txt_file_path = os.path.join(target_dir, txt_file_name)
        # Write text to TXT file
        with open(txt_file_path, 'w', encoding='utf-8') as f:
            f.write(text)
            # Log success message
        logger.info(f'Converted file {file_path} successfully!')
        # Increase count by 1
        count += 1
        # If count is divisible by 100, release memory
        if count % 50 == 0:
            gc.collect()
    except:
        # Log error message
        logger.error(f'Failed to convert file {file_path}!')


if __name__ == '__main__':
    # ...  
    # Create a Pool of 4 processes
    pool = Pool(4)
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        if file_path.endswith('.pdf'):
            pool.apply_async(pdf_to_txt, args=(file_path,))
    # Close the pool
    pool.close()
    # Join the processes
    pool.join()
    print('PDF to TXT conversion completed!')
