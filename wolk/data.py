import os
import json
import boto3
import logging

from .constants import (
    DATA_DIR,
    S3_BUCKET,
    AWS_DIR,
    AWS_EC2_FILE,
    AWS_RDS_FILE
)

def has_local_data(data_location: str = None) -> bool:

    if os.path.exists(DATA_DIR) and os.path.isdir(DATA_DIR):

        # If no data is specified, the general data directory is checked
        if data_location is None:
            return True
        else:
            data_dir = os.path.join(DATA_DIR, data_location)
            return os.path.exists(data_dir) and os.path.isdir(data_dir) and not (len(os.listdir(data_dir)) == 0)
    
    return False
            
def get_aws_data(data_type: str = None):

    ec2_file = os.path.join(DATA_DIR, AWS_DIR, AWS_EC2_FILE)
    rds_file = os.path.join(DATA_DIR, AWS_DIR, AWS_RDS_FILE)

    ec2_s3_key = DATA_DIR + '/' + AWS_DIR + '/' + AWS_EC2_FILE
    rds_s3_key = DATA_DIR + '/' + AWS_DIR + '/' + AWS_RDS_FILE

    # there might be a bug here, since has_local_data only checks if the directory is not empty,
    # not the actual file. Will probably fix later.
    if has_local_data(AWS_DIR):

        logging.info('Locally cached data found')
        
        # Return EC2 data by default
        if data_type is None or data_type == 'ec2':
            with open(ec2_file, 'r') as fp:
                return json.load(fp)

        elif data_type == 'rds':
            with open(rds_file, 'r') as fp:
                return json.load(rds_file)
        else:
            raise ValueError(f'{data_type} is not supported, choose "ec2" or "rds"')

    else:
        # If no local data is present, download it from S3 and persist it.
        logging.info('No locally cached data found, downloading from S3')
        s3 = boto3.client('s3')
        if data_type is None or data_type == 'ec2':
            os.makedirs(os.path.dirname(os.path.join(DATA_DIR, AWS_DIR)), exist_ok=True)
            s3.download_file(S3_BUCKET, ec2_s3_key, ec2_file)
            return get_aws_data(data_type)
        elif data_type == 'rds':
            os.makedirs(os.path.dirname(os.path.join(DATA_DIR, AWS_DIR)), exist_ok=True)
            s3.download_fileobj(S3_BUCKET, rds_s3_key, ec2_file)
            return get_aws_data(data_type)
        else:
            raise ValueError(f'{data_type} is not supported, choose "ec2" or "rds"')