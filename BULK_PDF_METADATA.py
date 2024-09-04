from argparse import ArgumentParser
from io import BytesIO
from os import path, listdir
import os
from pymupdf import Document, pymupdf
from tarfile import TarFile, is_tarfile
from typing import IO
from zipfile import is_zipfile, ZipFile

def get_pdf_metadata(pdf_file: IO[bytes], result_file: IO) -> None:
                    
                        pdf_data = BytesIO(pdf_file.read())
                        doc = Document(stream=pdf_data, filetype="pdf")

                        # First page:
                        first_page = doc.load_page(0)

                        # Fonts on page 1:
                        font_values = doc.get_page_fonts(first_page.number, full=True)
                        font_keys = ['xref', 'ext', 'type', 'basefont', 'name', 'encoding', 'referencer']
                        fonts_list = [dict(zip(font_keys, font)) for font in font_values]

                        result_file.write(f"Archive name: {tar_archive.name}\n")
                        result_file.write(f"Filename: {pdf.name}\n")
                        
                        if doc.metadata.get('format'):
                            result_file.write(f"Format: {doc.metadata.get('format')}\n")
                        if doc.metadata.get('producer'):
                            result_file.write(f"Producer: {doc.metadata.get('producer')}\n")
                        if doc.metadata.get('creationDate'):
                            result_file.write(f"Created: {doc.metadata.get('creationDate')}\n")
                        if doc.metadata.get('modDate'):
                            result_file.write(f"Last modified: {doc.metadata.get('modDate')}\n")
                        if doc.get_xml_metadata():
                            result_file.write(f"XML Data: {doc.get_xml_metadata()}\n")
                        if doc.page_count:
                            result_file.write(f"Pages: {doc.page_count}\n")
                            result_file.write("\n")
                        if fonts_list:
                            result_file.write(f"Fonts: \n")
                            for dictionary in fonts_list:
                                for key, value in dictionary.items():
                                    if value:
                                        result_file.write(f"{key}: {value}\n")
                            result_file.write("\n")

def format_exception(exception: str) -> str:
    if 'code=7' in exception:
        return "Document is not a real PDF"
    elif 'page not in document' in exception:
        return f"No '/Pages' object, corrupted PDF"
    else:
        return exception
                        
def tar_processing(tar_path: str, result_file: IO, errors: list[str]) -> int:
    pdf_count = 0
    not_pdf_count = 0

    with TarFile(name=tar_path, encoding='utf-8', debug=3) as tar_archive:
        for pdf in tar_archive.getmembers():
            if pdf.name.lower().endswith('.pdf'):
                with tar_archive.extractfile(pdf) as pdf_file:
                    try:
                        get_pdf_metadata(pdf_file, result_file)
                        pdf_count += 1
                    except Exception as exception:
                        pdf_basename = os.path.split(pdf_file.name)
                        archieve_basename = os.path.split(tar_archive.name)
                        errors.append(f"{archieve_basename[1]} :: {pdf_basename[1]} :: ERROR: {format_exception(str(exception))}")
            else:
                 not_pdf_count += 1
    return pdf_count, not_pdf_count

def zip_processing(zip_path: str, result_file: IO, errors: list[str]) -> int:
    pdf_count = 0
    not_pdf_count = 0

    with ZipFile(file=zip_path, metadata_encoding='utf-8') as zip_archive:
        for pdf in zip_archive.infolist():
            if pdf.filename.lower().endswith('.pdf'):
                with zip_archive.open(name=pdf.filename, mode='r') as pdf_file:
                    try:
                        get_pdf_metadata(pdf_file, result_file)
                        pdf_count += 1
                    except Exception as exception:
                        pdf_basename = os.path.split(pdf_file.name)
                        archieve_basename = os.path.split(zip_archive.filename)
                        errors.append(f"{archieve_basename[1]} :: {pdf_basename[1]} :: ERROR: {format_exception(str(exception))}")
            else:
                 not_pdf_count += 1

    return pdf_count, not_pdf_count

    
def traverse_directory(result_path: str, directory_path: str):

    errors = []
    zip_files, tar_files, pdf_files, not_pdf_files = 0, 0, 0, 0

    with open(result_path, mode='w', encoding='utf-8') as result_file:
        for item in listdir(directory_path):
            archive_dir = path.join(directory_path, item)

            if path.isfile(archive_dir):
                if is_zipfile(archive_dir):
                    zip_files += 1
                    pdf_count, not_pdf_count = zip_processing(archive_dir, result_file, errors)
                    pdf_files += pdf_count  
                    not_pdf_files += not_pdf_count
                elif is_tarfile(archive_dir):
                    tar_files += 1
                    pdf_count, not_pdf_count = tar_processing(archive_dir, result_file, errors)
                    pdf_files += pdf_count
                    not_pdf_files += not_pdf_count

        result_file.write("|=======================: SUMMARY :=======================|\n")
        result_file.write(f"PDF: {pdf_files} NOT_PDF: {not_pdf_files} TAR: {tar_files} ZIP: {zip_files} ERRORS: {len(errors)}\n")
        result_file.write("\n".join(errors))

if __name__ == "__main__":
    parser = ArgumentParser(prog="BULK_PDF_METADATA_UNPACK")
    parser.add_argument("-r", "--result-path", help="Path to the file where the results will be recorded.", type=str, required=True)
    parser.add_argument("-d", "--directory-path", help="Path to the directory that needs to be checked.", type=str, required=True)
    args = parser.parse_args()

    traverse_directory(path.normpath(args.result_path), path.normpath(args.directory_path))

    traverse_directory(result_path = r'C:\Users\ratanasov2\PDF_BULK_RESULTS', directory_path = r'C:\Users\ratanasov2\TRANSFER')