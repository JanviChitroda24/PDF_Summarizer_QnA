from fastapi import FastAPI, File, UploadFile
from docling.document_converter import DocumentConverter
import os
from dotenv import load_dotenv
import boto3
from datetime import datetime

app = FastAPI()

# Local directories
UPLOAD_DIR = "/Users/janvichitroda/Documents/Janvi/NEU/Big_Data_Intelligence_Analytics/Assignment 4/Part1_Janvi/PDF_Summarizer_QnA/InputFiles/"
OUTPUT_DIR = "/Users/janvichitroda/Documents/Janvi/NEU/Big_Data_Intelligence_Analytics/Assignment 4/Part1_Janvi/PDF_Summarizer_QnA/OutputFiles/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')  # Adjust the path to your .env file
load_dotenv(dotenv_path)

# AWS Configuration from Environment Variables
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")

# Initialize S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the PDF Summarizer API!"}

@app.get("/check-s3-connection/")
async def check_s3_connection():
    try:
        # Attempt to list objects in the specified S3 bucket
        response = s3_client.list_objects_v2(Bucket=AWS_S3_BUCKET_NAME)
        
        # If the bucket contains objects, return a success message
        if 'Contents' in response:
            return {"message": "Connected to S3 successfully!", "objects_in_bucket": len(response['Contents'])}
        else:
            return {"message": "Connected to S3 successfully, but the bucket is empty."}
    
    except Exception as e:
        # If there’s an error connecting to S3, return an error message
        return {"error": "Failed to connect to S3", "details": str(e)}

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, store it locally with a timestamp, convert to Markdown, store output,
    and upload both files to S3. Generate pre-signed URLs for private access.
    """
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Construct filenames with timestamp
    new_filename = f"{timestamp}_{file.filename}"
    print(new_filename)
    input_pdf_path = os.path.join(UPLOAD_DIR, new_filename)
    output_md_path = os.path.join(OUTPUT_DIR, f"{timestamp}_{file.filename}.md")

    # Save the uploaded PDF file locally
    with open(input_pdf_path, "wb") as f:
        f.write(file.file.read())

    # Convert PDF to Markdown
    converter = DocumentConverter()
    result = converter.convert(input_pdf_path)
    markdown_content = result.document.export_to_markdown()

    # Save the Markdown output locally
    with open(output_md_path, "w") as md_file:
        md_file.write(markdown_content)

    # Upload files to S3
    s3_pdf_key = f"pdf/{new_filename}"
    s3_md_key = f"markdown/{timestamp}_{file.filename}.md"

    s3_client.upload_file(input_pdf_path, AWS_S3_BUCKET_NAME, s3_pdf_key)
    s3_client.upload_file(output_md_path, AWS_S3_BUCKET_NAME, s3_md_key)

    # Generate pre-signed URLs (valid for 1 hour)
    pdf_presigned_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': AWS_S3_BUCKET_NAME, 'Key': s3_pdf_key},
        ExpiresIn=3600  # 1 hour expiration
    )

    md_presigned_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': AWS_S3_BUCKET_NAME, 'Key': s3_md_key},
        ExpiresIn=3600  # 1 hour expiration
    )

    return {
        "message": "File successfully uploaded, converted, and stored in S3.",
        "input_file": input_pdf_path,
        "output_file": output_md_path,
        "pdf_presigned_url": pdf_presigned_url,
        "md_presigned_url": md_presigned_url
    }
