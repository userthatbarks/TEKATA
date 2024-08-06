import io
import os
import zipfile
import tarfile
import logging
import pymupdf

def tar_processing(archieve_dir):

    global pdf_count
    global tar_count
    global errors
    
    logger.info("Reading the TAR archives into memory")
    
    for item in os.listdir(archieve_dir):
        tar = os.path.join(archieve_dir, item)
        if os.path.isfile(tar) and tarfile.is_tarfile(tar):
            with tarfile.TarFile(name=tar, mode='r', encoding='utf-8', debug='3') as tar_archive:
                tar_count += 1
                for pdf in tar_archive.getmembers():
                    
                    # Outer PDF verification:
                    if pdf.isfile() and (pdf.name.endswith('.pdf') or pdf.name.endswith('.PDF')):
                        with tar_archive.extractfile(pdf) as pdf_file:
                            try:
                                pdf_data = io.BytesIO(pdf_file.read())
                                doc = pymupdf.Document(stream=pdf_data, filetype="pdf")

                                # Inner PDF verification:
                                if doc.is_pdf:

                                    # First page:
                                    first_page = doc.load_page(0)

                                    # Fonts pn page 1:
                                    font_values = doc.get_page_fonts(first_page.number, full=True)

                                    # Define a list with the 'keys':
                                    font_keys = ['xref', 'ext', 'type', 'basefont', 'name', 'encoding', 'referencer']

                                    # Assigns the 'key-value' pair and creates a list of dictionaries:
                                    fonts_list = [dict(zip(font_keys, font)) for font in font_values]

                                    # xref (int) is the font object number (may be zero if the PDF uses one of the builtin fonts directly)
                                    # ext (str) font file extension (e.g. “ttf”, see Font File Extensions)
                                    # type (str) is the font type (like “Type1” or “TrueType” etc.)
                                    # basefont (str) is the base font name
                                    # name (str) is the symbolic name, by which the font is referenced
                                    # encoding (str) the font’s character encoding if different from its built-in encoding (Adobe PDF References, p. 254):
                                    # referencer (int optional) the xref of the referencer. Zero if directly referenced by the page, otherwise the xref of an XObject. Only present if full=True.

                                    # Assign metadata:
                                    metadata = doc.metadata
                                    xml_metadata = doc.get_xml_metadata()

                                    format = metadata.get('format')
                                    producer = metadata.get('producer')
                                    creation_date = metadata.get('creationDate')
                                    mod_date = metadata.get('modDate')
                        
                                    result_file.write("Archieve name: {}\n".format(tar_archive.name))
                                    result_file.write("Filename: {}\n".format(pdf.name))
                                    result_file.write("Format: {}\n".format(format))
                                    result_file.write("Producer: {}\n".format(producer))
                                    result_file.write("Created: {}\n".format(creation_date))
                                    result_file.write("Last modified: {}\n".format(mod_date))
                                    result_file.write("Pages: {}\n".format(doc.page_count))
                                    result_file.write("XML Data: {}\n".format(xml_metadata))
                                    result_file.write("Fonts: \n")

                                    for font_dict in fonts_list: 
                                        for key, value in font_dict.items(): 
                                            if value: 
                                                result_file.write(f"{key}: {value} \n")
                                    result_file.write("\n")
                                    pdf_count += 1
                                    
                            except Exception as msg:
                                if 'code=7' in str(msg):
                                    errors.append(f"{tar_archive.name} :: {pdf.name} :: ERROR: Document is not a real PDF")
                                elif 'page not in document' in str(msg):
                                    errors.append(f"{tar_archive.name} :: {pdf.name} :: ERROR: No '/Pages' object, corrupted PDF")
                                
                                # Everything else to be caught here:
                                else:
                                    errors.append(f"{tar_archive.name} :: {pdf.name} :: ERROR: {msg}")

def zip_processing(archieve_dir):

    global pdf_count
    global zip_count
    global errors

    logger.info("Reading the ZIP archives into memory")

    for item in os.listdir(archieve_dir):
        zip_path = os.path.join(archieve_dir, item)

        if os.path.isfile(zip_path) and zipfile.is_zipfile(zip_path):
            zip_count += 1
            with zipfile.ZipFile(file=zip_path, mode='r', metadata_encoding='utf-8') as zip_archive:
                for pdf in zip_archive.infolist():

                # Outer PDF verification:
                    if (pdf.filename.endswith('.pdf') or pdf.filename.endswith('.PDF')):
                        try:
                            with zip_archive.open(name=pdf.filename, mode='r') as pdf_file:
                                pdf_data = io.BytesIO(pdf_file.read())
                                doc = pymupdf.Document(stream=pdf_data, filetype="pdf")

                                # Inner PDF verification:
                                if doc.is_pdf:

                                    # First page:
                                    first_page = doc.load_page(0)

                                    # Fonts pn page 1:
                                    font_values = doc.get_page_fonts(first_page.number, full=True)

                                    # Define a list with the 'keys':
                                    font_keys = ['xref', 'ext', 'type', 'basefont', 'name', 'encoding', 'referencer']

                                    # Assigns the 'key-value' pair and creates a list of dictionaries:
                                    fonts_list = [dict(zip(font_keys, font)) for font in font_values]

                                    # xref (int) is the font object number (may be zero if the PDF uses one of the builtin fonts directly)
                                    # ext (str) font file extension (e.g. “ttf”, see Font File Extensions)
                                    # type (str) is the font type (like “Type1” or “TrueType” etc.)
                                    # basefont (str) is the base font name
                                    # name (str) is the symbolic name, by which the font is referenced
                                    # encoding (str) the font’s character encoding if different from its built-in encoding (Adobe PDF References, p. 254):
                                    # referencer (int optional) the xref of the referencer. Zero if directly referenced by the page, otherwise the xref of an XObject. Only present if full=True.

                                    # Assign metadata:
                                    metadata = doc.metadata
                                    xml_metadata = doc.get_xml_metadata()

                                    format = metadata.get('format')
                                    producer = metadata.get('producer')                                            
                                    creation_date = metadata.get('creationDate')
                                    mod_date = metadata.get('modDate')
                                    
                                    result_file.write("\n")
                                    result_file.write("Archive name: {}\n".format(zip_archive.filename))
                                    result_file.write("Filename: {}\n".format(pdf.filename))
                                    result_file.write("Directory: {}\n".format(pdf.is_dir()))
                                    result_file.write("Internal Attributes: {}\n".format(pdf.internal_attr))
                                    result_file.write("External Attributes: {}\n".format(pdf.external_attr))
                                    result_file.write("CRC: {}\n".format(pdf.CRC))
                                    result_file.write("Compressed size: {}\n".format(pdf.compress_size))
                                    result_file.write("Compress type: {}\n".format(pdf.compress_type))
                                    result_file.write("Format: {}\n".format(format))
                                    result_file.write("Producer: {}\n".format(producer))
                                    result_file.write("Created: {}\n".format(creation_date))
                                    result_file.write("Last modified: {}\n".format(mod_date))
                                    result_file.write("Pages: {}\n".format(doc.page_count))
                                    result_file.write("XML Data: {}\n".format(xml_metadata))
                                    result_file.write("Fonts: \n")

                                    for font_dict in fonts_list: 
                                        for key, value in font_dict.items(): 
                                            if value: 
                                                result_file.write(f"{key}: {value} \n")
                                    result_file.write("\n")
                                    pdf_count += 1

                        except Exception as msg:
                            if 'code=7' in str(msg):
                                errors.append(f"{zip_archive.filename} :: {pdf.filename} :: ERROR: Document is not a real PDF")
                            elif 'page not in document' in str(msg):
                                errors.append(f"{zip_archive.filename} :: {pdf.filename} :: ERROR: No '/Pages' object, corrupted PDF")
                            
                            # Everything else to be caught here:
                            else:
                                errors.append(f"{zip_archive.filename} :: {pdf.filename} :: ERROR: {msg}")

pdf_count = 0
tar_count = 0
zip_count = 0

errors = []

result_file = open(r'C:\Users\User_1\PDF_BULK_RESULTS', mode='w', encoding='utf-8')

# Create logging scheme for 'root' logger:
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, 
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(filename)s - %(message)s'
    )

zip_processing(r'C:\Users\User_1\Documents')
tar_processing(r'C:\Users\User_1\Documents')

result_file.write("|=======================: SUMMARY :=======================|\n")
result_file.write("PDF: {} ".format(pdf_count))
result_file.write("TAR: {} ".format(tar_count))
result_file.write("ZIP: {} \n".format(zip_count))
result_file.write("\nEXCEPTIONS:\n")
result_file.write("\n".join(errors))

logger.info("Append the results to file")
logger.info("Finished")