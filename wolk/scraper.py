import logging
import requests
import http
from typing import Dict
import json

from .exceptions import AWSDataScrapeException

AWS_URL = 'https://raw.githubusercontent.com/powdahound/ec2instances.info/master/www/instances.json'
AWS_DATA_LOCATION = './data/aws_data.json'

def scrape_aws_data() -> Dict:
    """Scrapes the AWS data from EC2instances.info

    Raises:
        AWSDataScrapeException: Raised when an error occurs when getting the data

    Returns:
        Dict -- Dict of JSON response
    """
    logging.info('Scraping data for AWS from EC2instances.info')
    
    response = requests.get(AWS_URL)

    if response.status_code == http.HTTPStatus.OK.value:
        return response.json()
    else:
        logging.exception('Error while scraping AWS data from EC2instances.info')
        logging.exception(f'Response status code: {response.status_code}')
        logging.exception(f'Response content: {response.text}')
        raise AWSDataScrapeException(f'Error while scraping AWS data from EC2instances.info')

def store_aws_data(aws_data: Dict):

    with open(AWS_DATA_LOCATION, 'w') as fp:
        json.dump(aws_data, fp)



    