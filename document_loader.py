# import os
# import pandas as pd
# from unstructured.partition.pdf import partition_pdf
# from unstructured.partition.docx import partition_docx
# from unstructured.partition.text import partition_text
# from unstructured.partition.xlsx import partition_xlsx
# from unstructured.partition.csv import partition_csv
# from pptx import Presentation


# def extract_text(file_path):
#     """Detect file type and extract text efficiently."""
#     ext = os.path.splitext(file_path)[1].lower()

#     if ext == ".pdf":
#         elements = partition_pdf(file_path, strategy="fast")  # Optimized for speed
#         return "\n".join([elem.text for elem in elements if elem.text])

#     elif ext == ".docx":
#         elements = partition_docx(file_path)
#         return "\n".join([elem.text for elem in elements if elem.text])

#     elif ext == ".txt":
#         with open(file_path, "r", encoding="utf-8") as file:
#             return file.read()

#     elif ext == ".xlsx":
#         df = pd.read_excel(file_path, sheet_name=None)  # Read all sheets
#         text = [f"Sheet: {sheet}\n" + data.to_string() for sheet, data in df.items()]
#         return "\n".join(text)

#     elif ext == ".csv":
#         df = pd.read_csv(file_path, low_memory=False)  # Optimized for large files
#         return df.to_string()

#     elif ext == ".pptx":  # Extract text from PowerPoint slides
#         ppt = Presentation(file_path)
#         text = []
#         for slide in ppt.slides:
#             for shape in slide.shapes:
#                 if hasattr(shape, "text"):
#                     text.append(shape.text)
#         return "\n".join(text)

#     else:
#         return "Unsupported file format!"
    
#     return(extract_text)

# # Example usage:
# # file_path =r"F:\8th sem\cloud computing\virtualization.docx" # Change this to your file path
# # extracted_text = extract_text(file_path)
# # print(extracted_text) 

import io
import pandas as pd
import docx
import pdfplumber
from pptx import Presentation
from openpyxl import load_workbook

def extract_text(file_name, file_bytes):
    """Extracts text from various document formats using in-memory file content."""
    file_extension = file_name.split(".")[-1].lower()
    
    if file_extension == "pdf":
        return extract_text_from_pdf(file_bytes)
    elif file_extension == "docx":
        return extract_text_from_docx(file_bytes)
    elif file_extension == "txt":
        return extract_text_from_txt(file_bytes)
    elif file_extension in ["xlsx", "csv"]:
        return extract_text_from_excel_csv(file_bytes, file_extension)
    elif file_extension == "pptx":
        return extract_text_from_pptx(file_bytes)
    else:
        return "Unsupported file format."

def extract_text_from_pdf(file_bytes):
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

def extract_text_from_docx(file_bytes):
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_bytes):
    return file_bytes.decode("utf-8")

def extract_text_from_excel_csv(file_bytes, file_extension):
    if file_extension == "csv":
        df = pd.read_csv(io.BytesIO(file_bytes))
    else:
        df = pd.read_excel(io.BytesIO(file_bytes), engine='openpyxl')
    return df.to_string()

def extract_text_from_pptx(file_bytes):
    prs = Presentation(io.BytesIO(file_bytes))
    return "\n".join([shape.text for slide in prs.slides for shape in slide.shapes if hasattr(shape, "text")])
