import logging
from typing import overload

import boto3

from ..config import Config
from ..model import File
from ..schema import FileCreateRequest, FileUpdateRequest
from ..utils import ensure_user_owns_resource
from .account import read as read_accounts

logger = logging.getLogger(__name__)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=Config.aws.access_key,
    aws_secret_access_key=Config.aws.secret_key,
    region_name=Config.aws.region,
)


def generate_upload_presigned_url(
    filename: str,
    content_type: str,
):
    return s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": Config.aws.bucket_name,
            "Key": filename,
            "ContentType": content_type,
        },
        ExpiresIn=3600,  # 1 hour validity
        HttpMethod="PUT",
    )


def generate_download_presigned_url(filename: str):
    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": Config.aws.bucket_name,
            "Key": filename,
        },
    )


def create(file_data: FileCreateRequest, account_id: str) -> File:
    logger.info("Adding new file %s", file_data)
    account = read_accounts(account_id)
    file = File(account=account, **file_data.model_dump()).create()
    logger.info("Added new file %s", file.id)
    return file


@overload
def read(file_id: str) -> File: ...
@overload
def read(**kwargs) -> list[File]: ...
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
