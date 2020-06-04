import os
import logging
import http
import requests
from typing import Dict
import json
from pathlib import Path
import boto3
from botocore.exceptions import ClientError

from .constants import (
    DATA_DIR,
    S3_BUCKET,
    AWS_DIR,
    AWS_DEFAULT_DATA_LOC,
    AWS_EC2_FILE,
    AWS_RDS_FILE,
    AZURE_DEFAULT_DATA_LOC
)

AWS_EC2_URL = 'http://www.ec2instances.info/instances.json'
AWS_RDS_URL = 'http://www.ec2instances.info/rds/instances.json'

AZURE_VM_MASTER_DATA_LINK = 'https://azure.microsoft.com/en-us/pricing/details/virtual-machines/'
AZURE_VM_SUB_PAGES = [
    'linux',
    'red-hat',
    'rhel-ha',
    'rhel-sap-business',
    'rhel-sap-hana',
    'rhel-sap-hana-ha',
    'sles-basic',
    'sles-standard',
    'sles-hpc-standard',
    'sles-sap',
    'ubuntu-advantage-essential',
    'ubuntu-advantage-standard',
    'ubuntu-advantage-advanced',
    'ml-server-rhel',
    'ml-server-ubuntu',
    'sql-server-enterprise-linux',
    'sql-server-standard-linux',
    'sql-server-web-linux',
    'sql-server-enterprise-redhat',
    'sql-server-standard-redhat',
    'sql-server-web-redhat',
    'sql-server-enterprise-sles',
    'sql-server-standard-sles',
    'sql-server-web-sles',
    'windows',
    'biztalk-enterprise',
    'biztalk-standard',
    'ml-server-windows',
    'sharepoint',
    'sql-server-enterprise',
    'sql-server-standard',
    'sql-server-web'
]

def scrape_aws(data_location: str = AWS_DEFAULT_DATA_LOC) -> None:

    # If there is no location to store the scraped data, create it.

    if not (os.path.exists(data_location) and os.path.isdir(data_location)):
        logging.info(f'Data location does not exist, creating directory {data_location}')
        os.mkdir(data_location)

    logging.info('Scraping data for AWS from www.ec2instances.info')

    logging.info('Scraping data for AWS EC2 instances')
    response: requests.Response = requests.get(AWS_EC2_URL)

    if response.status_code == http.HTTPStatus.OK.value:
        ec2_data: Dict = response.json()

        with open(os.path.join(data_location, AWS_EC2_FILE), 'w') as fp:
            json.dump(ec2_data, fp)

        logging.info(f'Scrape successful, saved data to {os.path.join(data_location, AWS_EC2_FILE)}')
    else:
        logging.info(f'Error while scraping EC2 data from {AWS_EC2_URL}')
    
    logging.info('Scraping data for AWS RDS instances')
    response: requests.Response = requests.get(AWS_RDS_URL)

    if response.status_code == http.HTTPStatus.OK.value:
        rds_data: Dict = response.json()

        with open(os.path.join(data_location, AWS_RDS_FILE), 'w') as fp:
            json.dump(rds_data, fp)

        logging.info(f'Scrape successful, saved data to {os.path.join(data_location, AWS_RDS_FILE)}')
    else:
        logging.info(f'Error while scraping RDS data from {AWS_RDS_URL}')

def scrape_azure_data(data_location: str = AZURE_DEFAULT_DATA_LOC) -> None:
    pass

def scrape(data_location: str = DATA_DIR):

    # If there is no location to store the scraped data, create it.

    if not (os.path.exists(data_location) and os.path.isdir(data_location)):
        logging.info(f'Data location does not exist, creating directory {data_location}')
        os.mkdir(data_location)
    
    logging.info('Scraping AWS data')
    scrape_aws()
    logging.info('Scrape successful!')

def upload_data_to_s3(file_name: str, bucket: str, object_name=None):

    # If no s3 object name was provided, use the filename
    if object_name is None:
        object_name = file_name
    
    s3_client = boto3.client('s3')

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)

    except ClientError as e:
        logging.error(e)
        return False
    
    logging.info(f'Uploaded scraped data to S3: s3://{S3_BUCKET}{object_name}')
    return True

def upload_data():
    """Upload scraped data to S3
    """

    logging.info(f'Uploading scraped AWS data to S3 bucket {S3_BUCKET}')
    aws_dir = os.path.join(DATA_DIR, AWS_DIR)
    ec2_data_file = os.path.join(aws_dir, AWS_EC2_FILE)
    rds_data_file = os.path.join(aws_dir, AWS_RDS_FILE)

    upload_data_to_s3(ec2_data_file, S3_BUCKET)
    upload_data_to_s3(rds_data_file, S3_BUCKET)
    logging.info('Upload of AWS data complete')



if __name__ == "__main__":
    scrape()