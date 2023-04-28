import os
import pdfplumber
from multiprocessing import Pool
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

source_dir = r'your_source_path'
target_dir = r'you_target_path'

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

def pdf_to_txt(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        txt_file_name = os.path.basename(file_path).replace('.pdf', '.txt')
        txt_file_path = os.path.join(target_dir, txt_file_name)
        with open(txt_file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        logger.info(f'转换文件 {file_path} 成功!')
    except:
        logger.error(f'转换文件 {file_path} 失败!')

if __name__ == '__main__':
    pool = Pool(6)
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        if file_path.endswith('.pdf'):
            pool.apply_async(pdf_to_txt, args=(file_path,))
    pool.close()
    pool.join()
    print('PDF2TXTfinish')
