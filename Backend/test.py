import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')  # Adjust the path to your .env file
load_dotenv(dotenv_path)

print(f"AWS_ACCESS_KEY: {os.getenv('AWS_ACCESS_KEY')}")
print(f"AWS_SECRET_ACCESS_KEY: {os.getenv('AWS_SECRET_ACCESS_KEY')}")
print(f"AWS_REGION: {os.getenv('AWS_REGION')}")
print(f"AWS_S3_BUCKET_NAME: {os.getenv('AWS_S3_BUCKET_NAME')}")