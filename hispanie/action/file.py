import logging
import os

import boto3

from ..model import File
from ..schema import FileCreateRequest, FileUpdateRequest
from ..utils import ensure_user_owns_resource
from .account import read as read_accounts

logger = logging.getLogger(__name__)

# AWS Configuration
S3_BUCKET = os.getenv("S3_BUCKET")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)


def generate_upload_presigned_url(
    filename: str,
    content_type: str,
):
    return s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": S3_BUCKET,
            "Key": filename,
            "ContentType": content_type,
            # "ACL": "public-read",  # Optional, depends on your use case
        },
        ExpiresIn=3600,  # 1 hour validity
        HttpMethod="PUT",
    )


def generate_download_presigned_url(filename: str):
    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": S3_BUCKET,
            "Key": filename,
        },
    )


def create(file_data: FileCreateRequest, account_id: str) -> File:
    logger.info("Adding new file %s", file_data)
    account = read_accounts(account_id)
    file = File(account=account, **file_data.model_dump()).create()
    logger.info("Added new file %s", file.id)
    return file


def read(file_id: str | None = None, **kwargs) -> File | list[File]:
    if file_id:
        logger.info("Reading %s data", file_id)
        return File.get(id=file_id)
    else:
        logger.info("Reading all data")
        return File.find(**kwargs)


def update(file_id: str, account_id: str, event_data: FileUpdateRequest) -> File:
    logger.info("Updating %s file", file_id)
    file = File.get(id=file_id)
    ensure_user_owns_resource(account_id, file.account_id)
    result = file.update(**event_data.model_dump(exclude_none=True))
    logger.info("Updated file %s", file_id)
    return result


def delete(file_id: str, account_id: str) -> File:
    logger.info("Deleting %s file", file_id)
    file = File.get(id=file_id)
    ensure_user_owns_resource(account_id, file.account_id)
    result = file.delete()
    logger.info("Deleted file %s", file_id)
    return result
