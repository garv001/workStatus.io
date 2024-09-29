import boto3
import logging

class S3Uploader:
    def __init__(self, bucket_name, aws_access_key, aws_secret_key, region):
        # Initialize the S3 client
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        self.bucket_name = bucket_name

    def upload_file(self, file_path, s3_key):
        try:
            # Upload file to S3 bucket
            self.s3.upload_file(file_path, self.bucket_name, s3_key)
            print(f"Successfully uploaded {file_path} to {self.bucket_name}/{s3_key}")
        except Exception as e:
            logging.error(f"Error uploading {file_path}: {e}")
            print(f"Upload failed: {e}")
