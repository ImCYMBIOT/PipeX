import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from dotenv import load_dotenv
import os

def test_s3_access():
    """
    Test if AWS credentials can access the specified S3 bucket.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Get credentials and bucket details from environment variables
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    bucket_name = os.getenv("BUCKET_NAME")
    region_name = os.getenv("AWS_REGION")

    if not all([aws_access_key, aws_secret_key, bucket_name, region_name]):
        print("Error: Missing required environment variables. Check your .env file.")
        return

    try:
        # Initialize the S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )
        
        # Attempt to list objects in the bucket
        print(f"Checking access to bucket: {bucket_name}")
        response = s3.list_objects_v2(Bucket=bucket_name)
        
        if 'Contents' in response:
            print(f"Access successful! Bucket contains {len(response['Contents'])} objects.")
        else:
            print("Access successful! Bucket is empty.")
    
    except NoCredentialsError:
        print("Error: AWS credentials are missing or not provided.")
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials.")
    except ClientError as e:
        print(f"Client error: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_s3_access()
