import os
import shutil
import PyPDF4
 # 设置目录路径
directory = ""
 # 创建两个文件夹，用于存放加密文件和未加密文件
if not os.path.exists(os.path.join(directory, "lock")):
    os.mkdir(os.path.join(directory, "lock"))
if not os.path.exists(os.path.join(directory, "unlock")):
    os.mkdir(os.path.join(directory, "unlock"))
 # 遍历目录下的文件
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.lower().endswith(".pdf"):
            file_path = os.path.join(root, file)
            try:
                pdf_reader = PyPDF4.PdfFileReader(file_path)
                # 检查文件是否加密
                if pdf_reader.isEncrypted:
                    # 如果加密，将文件移动到 lock 文件夹
                    dst_path = os.path.join(directory, "lock")
                    dst_file_path = os.path.join(dst_path, file)
                    # 如果目标路径中已经存在相同名称的文件，重命名该文件
                    if os.path.exists(dst_file_path):
                        file_name, file_ext = os.path.splitext(file)
                        new_file_name = file_name + "_1" + file_ext
                        dst_file_path = os.path.join(dst_path, new_file_name)
                    shutil.move(file_path, dst_file_path)
                else:
                    # 如果未加密，将文件移动到 unlock 文件夹
                    dst_path = os.path.join(directory, "unlock")
                    dst_file_path = os.path.join(dst_path, file)
                    # 如果目标路径中已经存在相同名称的文件，重命名该文件
                    if os.path.exists(dst_file_path):
                        file_name, file_ext = os.path.splitext(file)
                        new_file_name = file_name + "_1" + file_ext
                        dst_file_path = os.path.join(dst_path, new_file_name)
                    shutil.move(file_path, dst_file_path)
            # except PyPDF4.utils.PdfReadError:
            except ValueError as err:
                print(err)
                continue
                # 如果文件无法处理，将其跳过
                pass
