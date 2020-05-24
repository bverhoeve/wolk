import os
import logging
import http
import requests
from typing import Dict
import json
from pathlib import Path

DATA_DIR = 'data'


AWS_DIR = 'aws'
AWS_DEFAULT_DATA_LOC = os.path.join(DATA_DIR, AWS_DIR)
AWS_EC2_URL = 'http://www.ec2instances.info/instances.json'
AWS_RDS_URL = 'http://www.ec2instances.info/rds/instances.json'
AWS_EC2_FILE = 'ec2_instances.json'
AWS_RDS_FILE = 'rds_instances.json'

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

def scrape(data_location: str = DATA_DIR):

    # If there is no location to store the scraped data, create it.

    if not (os.path.exists(data_location) and os.path.isdir(data_location)):
        logging.info(f'Data location does not exist, creating directory {data_location}')
        os.mkdir(data_location)
    
    logging.info('Scraping AWS data')
    scrape_aws()
    logging.info('Scrape successful!')

if __name__ == "__main__":
    scrape()