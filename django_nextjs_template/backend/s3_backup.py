import os
from typing import Any
import boto3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
from django.conf import settings

S3_BACKUP_PATH = '/tmp/s3_backup'
# This is the endpoint URL without the bucket name for DigitalOcean Spaces, because otherwise it will not work
ENDPOINT_URL = settings.S3_ENDPOINT.replace(f'{settings.S3_MEDIA_BUCKET}.', '')

def download_dir(client: Any, dir: str, local_dir: str, bucket: str):
    print(f'Downloading Directory "{dir}" from bucket "{bucket}"')
    paginator = client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dir):
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                download_dir(client, subdir.get('Prefix'), local_dir, bucket)
        for file in result.get('Contents', []):
            dest_pathname = os.path.join(local_dir, file.get('Key'))
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            if not file.get('Key').endswith('/'):
                client.download_file(bucket, file.get('Key'), dest_pathname)


def backup_s3():
    print('Initiating S3 Backup')
    print(f'S3 Endpoint {ENDPOINT_URL}')
    print(f'S3 Bucket {settings.S3_MEDIA_BUCKET}') 
    print(f'S3 Key ID {settings.S3_ACCESS_KEY_ID}')
    client = boto3.client( # type: ignore
        service_name='s3',
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_KEY,
    )
    download_dir(client, '', S3_BACKUP_PATH, settings.S3_MEDIA_BUCKET)

backup_s3()