import os
import json
import boto3
import logging

from .constants import (
    DATA_DIR,
    S3_BUCKET,
    AWS_DIR,
    AWS_EC2_FILE,
    AWS_RDS_FILE,
    AZURE_DIR,
    GCP_DIR
)

# Initialisation of data directory
if not os.path.exists(DATA_DIR):
    logging.debug('No data directories yet, creating')
    aws_path: str = os.path.join(DATA_DIR, AWS_DIR)
    azure_path: str = os.path.join(DATA_DIR, AZURE_DIR)
    gcp_path: str = os.path.join(DATA_DIR, GCP_DIR)
    os.makedirs(aws_path, exist_ok=True)
    os.makedirs(azure_path, exist_ok=True)
    os.makedirs(gcp_path, exist_ok=True)

def has_local_data(file_path: str = None) -> bool:
    return os.path.exists(file_path) and os.path.isfile(file_path)
            
def get_aws_data(data_type: str = None):

    file_path: str = None
    object_key: str = None

    if data_type is None or data_type == 'ec2':
        file_path: str = os.path.join(DATA_DIR, AWS_DIR, AWS_EC2_FILE)
        object_key: str = DATA_DIR + '/' + AWS_DIR + '/' + AWS_EC2_FILE
    elif data_type == 'rds':
        file_path: str = os.path.join(DATA_DIR, AWS_DIR, AWS_RDS_FILE)
        object_key: str = DATA_DIR + '/' + AWS_DIR + '/' + AWS_RDS_FILE
    else:
        raise ValueError(f'{data_type} is not supported, choose "ec2" or "rds"')

    logging.debug(f'Loading AWS {data_type} data')

    if has_local_data(file_path):
        logging.info('Locally cached data found')
        with open(file_path, 'r') as fp:
            return json.load(fp)
        
    else:
        # If no local data is present, download it from S3 and persist it.
        logging.info('No locally cached data found, downloading from S3')
        s3 = boto3.client('s3')
        logging.debug(f'Downloading {object_key} from {S3_BUCKET} to {file_path}')
        s3.download_file(S3_BUCKET, object_key, file_path)
        
        # Once downloaded, load in the cached data
        return get_aws_data(data_type)