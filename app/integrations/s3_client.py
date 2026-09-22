import boto3
from app.core import config


class S3Service:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            region_name=config.AWS_REGION,
        )
        self.bucket = config.S3_BUCKET

    def upload(self, file_path: str, key: str):
        self.client.upload_file(file_path, self.bucket, key)

    def download(self, key: str, dest_path: str):
        self.client.download_file(self.bucket, key, dest_path)
