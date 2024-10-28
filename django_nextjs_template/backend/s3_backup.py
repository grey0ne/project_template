import os
from typing import Any
import boto3 # type: ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
from django.conf import settings

S3_BACKUP_PATH = '/tmp/s3_backup'


def download_dir(client: Any, dir: str, local_dir: str, bucket: str):
    paginator = client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dir):
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                print(f'Downloading {subdir.get("Prefix")}')
                download_dir(client, subdir.get('Prefix'), local_dir, bucket)
        for file in result.get('Contents', []):
            dest_pathname = os.path.join(local_dir, file.get('Key'))
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            if not file.get('Key').endswith('/'):
                client.download_file(bucket, file.get('Key'), dest_pathname)


def backup_s3():
    client = boto3.client( # type: ignore
        service_name='s3',
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_KEY,
    )
    download_dir(client, '', S3_BACKUP_PATH, settings.S3_BUCKET)

backup_s3()