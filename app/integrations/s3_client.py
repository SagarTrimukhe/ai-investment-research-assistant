import os
import boto3
from typing import List, Dict, Any, Optional
from app.core import config


class S3Service:
    """Manages cloud document storage and report archiving with AWS S3."""

    def __init__(self):
        self.bucket = config.S3_BUCKET
        self.region = config.AWS_REGION
        self.client = boto3.client(
            "s3",
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            region_name=self.region,
        )

    def upload_file(self, file_path: str, key: str) -> bool:
        """Upload a local file to S3 bucket."""
        try:
            self.client.upload_file(file_path, self.bucket, key)
            return True
        except Exception as e:
            print(f"S3 upload error for {key}: {e}")
            return False

    def upload_bytes(
        self, data: bytes, key: str, content_type: str = "application/octet-stream"
    ) -> bool:
        """Upload in-memory bytes directly to S3."""
        try:
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=data,
                ContentType=content_type,
            )
            return True
        except Exception as e:
            print(f"S3 put_object error for {key}: {e}")
            return False

    def download_file(self, key: str, dest_path: str) -> bool:
        """Download an S3 object to local disk."""
        try:
            os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
            self.client.download_file(self.bucket, key, dest_path)
            return True
        except Exception as e:
            print(f"S3 download error for {key}: {e}")
            return False

    def list_files(self, prefix: str = "") -> List[Dict[str, Any]]:
        """List objects stored in S3 bucket with given prefix."""
        try:
            resp = self.client.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
            contents = resp.get("Contents", [])
            return [
                {
                    "key": item["Key"],
                    "size": item["Size"],
                    "last_modified": item["LastModified"].isoformat(),
                }
                for item in contents
            ]
        except Exception as e:
            print(f"S3 list_objects error: {e}")
            return []
