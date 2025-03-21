from fastapi import FastAPI
from fastapi import File, UploadFile
from docling.document_converter import DocumentConverter
import os
from datetime import datetime

app = FastAPI()

UPLOAD_DIR = "/Users/janvichitroda/Documents/Janvi/NEU/Big_Data_Intelligence_Analytics/Assignment 4/Part1_Janvi/PDF_Summarizer_QnA/InputFiles/"
OUTPUT_DIR = "/Users/janvichitroda/Documents/Janvi/NEU/Big_Data_Intelligence_Analytics/Assignment 4/Part1_Janvi/PDF_Summarizer_QnA/OutputFiles/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, store it locally with a timestamp, convert to Markdown, and store the output.
    """
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Construct new filenames with timestamp
    new_filename = f"{timestamp}_{file.filename}"
    input_pdf_path = os.path.join(UPLOAD_DIR, new_filename)
    output_md_path = os.path.join(OUTPUT_DIR, f"{timestamp}_{file.filename}.md")

    # Save the uploaded PDF file with timestamp
    with open(input_pdf_path, "wb") as f:
        f.write(file.file.read())

    # Convert PDF to Markdown
    converter = DocumentConverter()
    result = converter.convert(input_pdf_path)
    markdown_content = result.document.export_to_markdown()

    # Save the Markdown output
    with open(output_md_path, "w") as md_file:
        md_file.write(markdown_content)

    return {
        "message": "File successfully uploaded and converted.",
        "input_file": input_pdf_path,
        "output_file": output_md_path
    }