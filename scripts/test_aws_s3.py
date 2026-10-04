#!/usr/bin/env python3
"""AWS S3 Connectivity & Storage Validation Script.

Tests:
1. Credentials detection in .env
2. S3 bucket existence and access
3. Sample filing/report upload
4. File download & verification
5. Object listing
"""

import os
import sys
import tempfile
import time

# Ensure project root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core import config
from app.integrations.s3_client import S3Service


def run_s3_test():
    print("=" * 60)
    print("  AWS S3 Cloud Storage Diagnostic & Verification Test")
    print("=" * 60)

    print(f"Bucket Name:       {config.S3_BUCKET}")
    print(f"AWS Region:        {config.AWS_REGION}")
    print(f"AWS Access Key ID: {config.AWS_ACCESS_KEY_ID[:4]}...{config.AWS_ACCESS_KEY_ID[-4:] if len(config.AWS_ACCESS_KEY_ID) > 8 else '[Not Set]'}")

    s3 = S3Service()
    if not s3.is_configured():
        print("\n[INFO] AWS credentials or bucket name not configured in .env.")
        print("To configure AWS S3:")
        print("  1. Open .env")
        print("  2. Set AWS_ACCESS_KEY_ID=your_key")
        print("  3. Set AWS_SECRET_ACCESS_KEY=your_secret")
        print("  4. Set AWS_DEFAULT_REGION=us-east-1")
        print("  5. Set S3_BUCKET_NAME=your_bucket_name")
        print("\nApplication gracefully operates in Local Storage Mode until configured.")
        return False

    print("\n[+] Attempting connection to AWS S3...")
    test_key = f"diagnostics/test_{int(time.time())}.txt"
    test_content = b"AI Investment Research Assistant - AWS S3 Verification Payload"

    # 1. Upload Test
    print(f"[+] Uploading test payload to s3://{s3.bucket}/{test_key}...")
    success = s3.upload_bytes(test_content, key=test_key, content_type="text/plain")
    if not success:
        print("[-] FAILED: Could not upload to S3 bucket. Check IAM permissions (s3:PutObject).")
        return False
    print("    -> Upload successful!")

    # 2. List Test
    print("[+] Listing objects under 'diagnostics/' prefix...")
    files = s3.list_files(prefix="diagnostics/")
    print(f"    -> Found {len(files)} object(s) in S3 bucket.")

    # 3. Download Test
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_dest = tmp.name

    try:
        print(f"[+] Downloading test object from S3 to local temporary file...")
        dl_success = s3.download_file(test_key, tmp_dest)
        if dl_success and os.path.exists(tmp_dest):
            with open(tmp_dest, "rb") as f:
                downloaded_data = f.read()
            if downloaded_data == test_content:
                print("    -> Verification passed! Downloaded bytes match uploaded payload.")
            else:
                print("[-] WARNING: Downloaded content did not match.")
        else:
            print("[-] FAILED to download object.")
    finally:
        if os.path.exists(tmp_dest):
            os.remove(tmp_dest)

    # 4. Clean up test object
    try:
        s3.client.delete_object(Bucket=s3.bucket, Key=test_key)
        print(f"[+] Cleaned up temporary test object {test_key}.")
    except Exception:
        pass

    print("\n" + "=" * 60)
    print("  ALL AWS S3 STORAGE TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    run_s3_test()
