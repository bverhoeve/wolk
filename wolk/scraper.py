import logging
import requests
import http

from .exceptions import AWSDataScrapeException

AWS_URL = 'https://raw.githubusercontent.com/powdahound/ec2instances.info/master/www/instances.json'

def scrape_aws_data():
    logging.info('Scraping data for AWS from EC2instances.info')
    
    response = requests.get(AWS_URL)

    if response.status_code is http.HTTPStatus.OK:
        return response.json()
    else:
        logging.exception('Error while scraping AWS data from EC2instances.info')
        logging.excpetion(f'Response status code: {response.status_code}')
        logging.exception(f'Response content: {response.text}')
        raise AWSDataScrapeException(f'Error while scraping AWS data from EC2instances.info')

    