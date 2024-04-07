import io
import os
import zipfile
import tarfile
import logging
import warnings
import datetime
from PyPDF2 import PdfReader

# <module>.
    # <class>.
        # <object>.
            # <method>.
                # <attribute>

# Control warnings
warnings.filterwarnings("default")

# Control errors from PyPDF2
logger_zip = logging.getLogger("PyPDF2")
logger_zip.setLevel(logging.ERROR)

logger_tar = logging.getLogger("tarfile")
logger_tar.setLevel(logging.ERROR)

file_count = 0
errors = []

result_file = open(r"C:\Users\ratanasov2\OneDrive - DXC Production\Desktop\results", 'a')

archieve_dir= r"C:\Users\ratanasov2\COMBO"

# TAR TAR TAR TAR TAR TAR TAR TAR TAR TAR TAR TAR
def tar_processing():

    global file_count
    global errors

    for item in os.listdir(archieve_dir):
        tar = os.path.join(archieve_dir, item)

        if tarfile.is_tarfile(tar):
            
            with tarfile.TarFile(tar, 'r') as tar_archieve:

                for pdf in tar_archieve.getmembers():

                    if pdf.name.endswith('.pdf') or pdf.name.endswith('.PDF'):

                        with tar_archieve.extractfile(pdf) as pdf_file:

                            # Read the PDF file's content in binary mode:
                            pdf_data = io.BytesIO(pdf_file.read())

                            # Check integrity
                            try:
                                pdf_reader = PdfReader(pdf_data)
                                num_pages = len(pdf_reader.pages)
                                if num_pages == 0:
                                    msg = f"ERROR: {pdf_file} is invalid or empty!"
                                    errors.append(msg)

                            except Exception as e:
                                msg = f"{tar_archieve.filename} - {pdf_file.filename} : {e}"
                                errors.append(msg)

                            result_file.write("\n")
                            result_file.write("Archieve: {}\n".format(tar_archieve.name))
                            result_file.write("Name: {}\n".format(pdf.name))
                            result_file.write("Pages: {}\n".format(num_pages))
                            result_file.write("Size: {}\n".format(pdf.size))
                            result_file.write("Time: {}\n".format(datetime.datetime.fromtimestamp(pdf.mtime).strftime('%Y-%m-%d %H:%M:%S')))
                            result_file.write("\n")
                            file_count += 1
                    else:
                        continue

# ZIPS ZIPS ZIPS ZIPS ZIPS ZIPS ZIPS ZIPS ZIPS ZIPS 
def zip_processing():

    global file_count
    global errors

    # Get full path to each zip file:
    for item in os.listdir(archieve_dir):
        zip = os.path.join(archieve_dir, item)

        # Checks if the file is ZIP:
        if zipfile.is_zipfile(zip):

            # Initiates the 'ZipFile' class and creates the 'zip_archieve':
            with zipfile.ZipFile(zip, 'r') as zip_archieve:

                # Get information about each file inside:
                for zip_file in zip_archieve.infolist():

                    # Check if the file is a PDF:
                    if zip_file.filename.endswith('.pdf') or zip_file.filename.endswith('.PDF'):

                        # Open the PDF file from the ZIP archive:
                        with zip_archieve.open(zip_file.filename, 'r') as pdf_file:
                                
                            # Read the PDF file's content in binary mode:
                            pdf_data = io.BytesIO(pdf_file.read())

                            # Check integrity
                            try:
                                pdf_reader = PdfReader(pdf_data)
                                num_pages = len(pdf_reader.pages)
                                if num_pages == 0:
                                    msg = f"ERROR: {pdf_file} is invalid or empty!"
                                    errors.append(msg)

                            except Exception as e:
                                msg = f"{zip_archieve.filename} - {zip_file.filename}: {e}"
                                errors.append(msg)

                            # Write information to the result file
                            # - using 'format' method to include leading zeros on HH:MM:SS 
                            # ({:02d}:{:02d}:{:02d})

                            # Zipinfo class parameters:
                            result_file.write("\n")
                            result_file.write("Archive name: {}\n".format(zip_archieve.filename))
                            result_file.write("File name: {}\n".format(zip_file.filename))
                            result_file.write("Last modified: {}/{}/{} {:02d}:{:02d}:{:02d}\n".format(*zip_file.date_time[0:6]))
                            result_file.write("Directory: {}\n".format(zip_file.is_dir()))
                            result_file.write("Internal Attributes: {}\n".format(zip_file.internal_attr))
                            result_file.write("External Attributes: {}\n".format(zip_file.external_attr))
                            result_file.write("CRC: {}\n".format(zip_file.CRC))
                            result_file.write("Compressed size: {}\n".format(zip_file.compress_size))
                            result_file.write("Compress type: {}\n".format(zip_file.compress_type))
                            result_file.write("Pages: {}\n".format(len(pdf_reader.pages)))
                            result_file.write("\n")
                            file_count += 1  

zip_processing()
tar_processing()

# Writes the count:
result_file.write("Total files: {}\n".format(file_count))

# Troubling ones:
result_file.write("\n")
result_file.write("ERRORS: ")
result_file.write("\n".join(map(str, errors)))
result_file.write("\n")

#Print results
print("RESULTS: --> ", result_file.name)

#Close the file
result_file.close()











