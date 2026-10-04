import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import List, Dict, Any, Optional
from app.core import config


class S3Service:
    """Manages cloud document storage and report archiving with AWS S3."""

    def __init__(self):
        self.bucket = config.S3_BUCKET
        self.region = config.AWS_REGION
        self.access_key = config.AWS_ACCESS_KEY_ID
        self.secret_key = config.AWS_SECRET_ACCESS_KEY
        self._client = None

    @property
    def client(self):
        """Lazy-loaded boto3 client to prevent crash when credentials are unset."""
        if self._client is None and self.is_configured():
            self._client = boto3.client(
                "s3",
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region,
            )
        return self._client

    def is_configured(self) -> bool:
        """Check if AWS credentials and bucket are properly configured."""
        placeholders = {"", "your_aws_access_key_id", "your_aws_secret_access_key"}
        return (
            bool(self.access_key)
            and self.access_key not in placeholders
            and bool(self.secret_key)
            and self.secret_key not in placeholders
            and bool(self.bucket)
        )

    def upload_file(self, file_path: str, key: str) -> bool:
        """Upload a local file to S3 bucket."""
        if not self.is_configured():
            return False
        try:
            self.client.upload_file(file_path, self.bucket, key)
            return True
        except (ClientError, NoCredentialsError) as e:
            print(f"S3 upload error for {key}: {e}")
            return False

    def upload_bytes(
        self, data: bytes, key: str, content_type: str = "application/octet-stream"
    ) -> bool:
        """Upload in-memory bytes directly to S3."""
        if not self.is_configured():
            return False
        try:
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=data,
                ContentType=content_type,
            )
            return True
        except (ClientError, NoCredentialsError) as e:
            print(f"S3 put_object error for {key}: {e}")
            return False

    def download_file(self, key: str, dest_path: str) -> bool:
        """Download an S3 object to local disk."""
        if not self.is_configured():
            return False
        try:
            os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
            self.client.download_file(self.bucket, key, dest_path)
            return True
        except (ClientError, NoCredentialsError) as e:
            print(f"S3 download error for {key}: {e}")
            return False

    def list_files(self, prefix: str = "") -> List[Dict[str, Any]]:
        """List objects stored in S3 bucket with given prefix."""
        if not self.is_configured():
            return []
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
        except (ClientError, NoCredentialsError) as e:
            print(f"S3 list_objects error: {e}")
            return []

    def generate_presigned_url(self, key: str, expiration: int = 3600) -> Optional[str]:
        """Generate a temporary pre-signed URL for direct browser access."""
        if not self.is_configured():
            return None
        try:
            return self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": key},
                ExpiresIn=expiration,
            )
        except Exception as e:
            print(f"Failed to generate presigned URL for {key}: {e}")
            return None
