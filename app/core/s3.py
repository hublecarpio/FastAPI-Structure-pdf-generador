import boto3
from botocore.exceptions import ClientError
from app.core.config import settings


def get_s3_client():
    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        return boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
    return None


def upload_file(bucket: str, key: str, data: bytes) -> bool:
    client = get_s3_client()
    if client is None:
        return _local_upload(key, data)
    
    try:
        client.put_object(Bucket=bucket, Key=key, Body=data)
        return True
    except ClientError:
        return False


def get_file(bucket: str, key: str) -> bytes | None:
    client = get_s3_client()
    if client is None:
        return _local_get(key)
    
    try:
        response = client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read()
    except ClientError:
        return None


def delete_file(bucket: str, key: str) -> bool:
    client = get_s3_client()
    if client is None:
        return _local_delete(key)
    
    try:
        client.delete_object(Bucket=bucket, Key=key)
        return True
    except ClientError:
        return False


import os

LOCAL_STORAGE_PATH = "local_storage"


def _local_upload(key: str, data: bytes) -> bool:
    try:
        full_path = os.path.join(LOCAL_STORAGE_PATH, key)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'wb') as f:
            f.write(data)
        return True
    except Exception:
        return False


def _local_get(key: str) -> bytes | None:
    try:
        full_path = os.path.join(LOCAL_STORAGE_PATH, key)
        with open(full_path, 'rb') as f:
            return f.read()
    except Exception:
        return None


def _local_delete(key: str) -> bool:
    try:
        full_path = os.path.join(LOCAL_STORAGE_PATH, key)
        if os.path.exists(full_path):
            os.remove(full_path)
        return True
    except Exception:
        return False
