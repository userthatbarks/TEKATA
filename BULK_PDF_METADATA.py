import io
import os
import zipfile
import tarfile
import logging
import datetime
from pdfreader import PDFDocument

    # <module>.
        # <class>.
            # <object>.
                # <method>.
                    # <attribute>


file_count = 0
errors = []
warnings = []

# Create logging scheme for modules:
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# Create the logger names and set level: 
logger_main = logging.getLogger('STATUS')

logger_zip = logging.getLogger("PDFDocument")
logger_zip.setLevel(logging.ERROR)

# Results file:
result_file = open(r"C:\Users\User1\results", 'w')

# Archieve directory:
archieve_dir= r"C:\Users\User1\COMBO"

# TAR TAR TAR TAR TAR TAR TAR TAR TAR TAR TAR TAR


def tar_processing():
    print()

    global file_count
    global errors
    global warnings

    logger_main.info("Started")
    logger_main.info("TAR processing - Getting TAR archieves")
    logger_main.info("TAR processing - Check the PDFs and metadata")
    logger_main.info("TAR processing - Try-Catch if any exceptions")

    for item in os.listdir(archieve_dir):
        tar = os.path.join(archieve_dir, item)

        if tarfile.is_tarfile(tar):
            
            with tarfile.TarFile(tar, 'r') as tar_archieve:

                for pdf in tar_archieve.getmembers():

                    if pdf.name.endswith('.pdf') or pdf.name.endswith('.PDF'):

                        with tar_archieve.extractfile(pdf) as pdf_file:

                            try:
                                pdf_data = io.BytesIO(pdf_file.read())
                                doc = PDFDocument(pdf_data)
                                all_pages = [page for page in doc.pages()]

                            except Exception as e:

                                msg = f"{tar_archieve.name} - {pdf_file.name} : {e}"
                                errors.append(msg)

                            result_file.write("\n")
                            result_file.write("Archieve: {}\n".format(tar_archieve.name))
                            result_file.write("Name: {}\n".format(pdf.name))
                            result_file.write("Pages: {}\n".format(len(all_pages)))
                            result_file.write("Size: {}\n".format(pdf.size))
                            result_file.write("Time: {}\n".format(datetime.datetime.fromtimestamp(pdf.mtime).strftime('%Y-%M-%D %H:%M:%S')))
                            result_file.write("\n")
                            file_count += 1
                    else:
                        continue

# ZIPS ZIPS ZIPS ZIPS ZIPS ZIPS ZIPS ZIPS ZIPS ZIPS 
def zip_processing():

    global file_count
    global errors
    global warnings

    logger_main.info("ZIP processing - Getting TAR archieves")
    logger_main.info("ZIP processing - Check the PDFs and metadata")
    logger_main.info("ZIP processing - Try-Catch if any exceptions")

    for item in os.listdir(archieve_dir):
        zip = os.path.join(archieve_dir, item)

        if zipfile.is_zipfile(zip):

            with zipfile.ZipFile(zip, 'r') as zip_archieve:
                
                for zip_file in zip_archieve.infolist():

                    if zip_file.filename.endswith('.pdf') or zip_file.filename.endswith('.PDF'):

                        with zip_archieve.open(zip_file.filename, 'r') as pdf_file:

                            try:
                                pdf_data = io.BytesIO(pdf_file.read())
                                doc = PDFDocument(pdf_data)

                            except Exception as e:

                                msg = f"{zip_archieve.filename} - {pdf_file.name} : {e}"
                                errors.append(msg)
                                
                            # Write information to the result file
                            # - using 'format' method to include leading zeros on HH:MM:SS 
                            # ({:02d}:{:02d}:{:02d})                        

                            all_pages = [page for page in doc.pages()]

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
                            result_file.write("Pages: {}\n".format(len(all_pages)))
                            result_file.write("\n")
                            file_count += 1  

tar_processing()
zip_processing()

logger_main.info("Append the results to file")
logger_main.info("Finished")

result_file.write("TOTAL FILES: {}\n".format(file_count))

result_file.write("\n")
result_file.write("EXCEPTIONS: ")
result_file.write("\n")
result_file.write("\n".join(map(str, errors)))
result_file.write("\n")

print()
print("RESULTS: --> ", result_file.name)

result_file.close()
