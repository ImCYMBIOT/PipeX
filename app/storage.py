import boto3
import os
import logging
from botocore.exceptions import ClientError
import pandas as pd
from dotenv import load_dotenv


load_dotenv() 
logger = logging.getLogger(__name__)

def save_to_file(data, file_path, format = 'csv'):
    try:
        if format == 'csv':
            data.to_csv(file_path, index=False)
        elif format == 'json':
            data.to_json(file_path, orient='records', lines=True)
        else:
            raise ValueError("File format not supported.")
    except Exception as e:
        logger.error(f"Failed to save data to file: {str(e)}")
        raise
    
def upload_to_s3(file_path, bucket_name, key):
    s3 = boto3.client(
        "s3",
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name = os.getenv("AWS_REGION")
    )
    
    try:
        s3.upload_file(file_path, bucket_name, key)
        logger.info(f"File uploaded to S3 bucket: {bucket_name}")
    except ClientError as e:
        logger.error(f"Failed to upload file to S3 bucket: {str(e)}")
        raise 
    