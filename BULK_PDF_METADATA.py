import io
import os
import zipfile
import tarfile
import logging
import datetime
from PyPDF2 import PdfReader

pdf_count = 0
tar_count = 0
zip_count = 0

errors = []

# Create logging scheme for modules:
logging.basicConfig(level=logging.ERROR , format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# Create the logger names and set level:
logger_main = logging.getLogger('MAIN')
logger_main.setLevel('INFO')

# Open the result file for writing
result_file = open("/home/results", 'w')

def tar_processing(archive_dir_date):

    global pdf_count
    global tar_count
    global errors

    logger_main.info("Started")
    logger_main.info("TAR processing - Getting TAR archives")
    logger_main.info("TAR processing - Check the PDFs and metadata")
    logger_main.info("TAR processing - Try-Catch if any exceptions")

    for item in os.listdir(archive_dir_date):
        tar = os.path.join(archive_dir_date, item)

        if os.path.isfile(tar) and tarfile.is_tarfile(tar):
                with tarfile.open(tar, 'r') as tar_archive:
                    tar_count += 1
                    for pdf in tar_archive.getmembers():
                        if pdf.isfile() and (pdf.name.endswith('.pdf') or pdf.name.endswith('.PDF')):
                            try:
                                with tar_archive.extractfile(pdf) as pdf_file:
                                    if pdf_file:
                                        pdf_data = io.BytesIO(pdf_file.read())
                                        pdf_reader = PdfReader(pdf_data)
                                        
                                        num_pages = len(pdf_reader.pages)
                                        result_file.write("\n")
                                        result_file.write("Archive: {}\n".format(tar_archive.name))
                                        result_file.write("Name: {}\n".format(pdf.name))
                                        result_file.write("Pages: {}\n".format(num_pages))
                                        result_file.write("Size: {}\n".format(pdf.size))
                                        result_file.write("Time: {}\n".format(datetime.datetime.fromtimestamp(pdf.mtime).strftime('%Y-%m-%d %H:%M:%S')))
                                        result_file.write("\n")
                                        pdf_count += 1                                 
                            except Exception as e:
                                errors.append(f"{tar} :: {pdf.name} :: {e}")

def zip_processing(archive_dir_date):

    global pdf_count
    global zip_count
    global errors

    logger_main.info("ZIP processing - Getting ZIP archives")
    logger_main.info("ZIP processing - Check the PDFs and metadata")
    logger_main.info("ZIP processing - Try-Catch if any exceptions")

    for item in os.listdir(archive_dir_date):
        zip_path = os.path.join(archive_dir_date, item)

        if os.path.isfile(zip_path) and zipfile.is_zipfile(zip_path):
                with zipfile.ZipFile(zip_path, 'r') as zip_archive:
                    zip_count += 1
                    for zip_file in zip_archive.infolist():
                        if zip_file.filename.endswith('.pdf') or zip_file.filename.endswith('.PDF'):
                            try:
                                with zip_archive.open(zip_file.filename, 'r') as pdf_file:
                                    pdf_data = io.BytesIO(pdf_file.read())
                                    pdf_reader = PdfReader(pdf_data)
                                    num_pages = len(pdf_reader.pages)

                                    result_file.write("\n")
                                    result_file.write("Archive name: {}\n".format(zip_archive.filename))
                                    result_file.write("File name: {}\n".format(zip_file.filename))
                                    result_file.write("Last modified: {}/{}/{} {:02d}:{:02d}:{:02d}\n".format(*zip_file.date_time[0:6]))
                                    result_file.write("Directory: {}\n".format(zip_file.is_dir()))
                                    result_file.write("Internal Attributes: {}\n".format(zip_file.internal_attr))
                                    result_file.write("External Attributes: {}\n".format(zip_file.external_attr))
                                    result_file.write("CRC: {}\n".format(zip_file.CRC))
                                    result_file.write("Compressed size: {}\n".format(zip_file.compress_size))
                                    result_file.write("Compress type: {}\n".format(zip_file.compress_type))
                                    result_file.write("Pages: {}\n".format(num_pages))
                                    result_file.write("\n")
                                    pdf_count += 1
                            except Exception as e:
                                errors.append(f"{zip_path} :: {zip_file.filename} :: {e}")

tar_processing("/dir/with/tars")
zip_processing("/dir/with/zips")

logger_main.info("Append the results to file")
logger_main.info("Finished")

result_file.write("TOTAL FILES: {}\n".format(pdf_count))
result_file.write("TAR Archives: {}\n".format(tar_count))
result_file.write("ZIP Archives: {}\n".format(zip_count))

result_file.write("\nEXCEPTIONS:\n")
result_file.write("\n".join(errors))

result_file.close()
