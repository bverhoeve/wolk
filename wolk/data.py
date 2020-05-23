import os
import json

from typing import Dict

from .scraper import scrape_aws_data, store_aws_data


DATA_DIR = 'data'
AWS_FILE = 'aws_data.json'

def aws_data_exists() -> bool:
    # check if the path exists to the aws data file
    if os.path.exists(os.path.join('.', DATA_DIR, AWS_FILE)):
        return os.path.isfile(os.path.join('.', DATA_DIR, AWS_FILE))
    else:
        return False

def get_aws_data() -> Dict:
    
    # if the aws data exists, read it in from the file
    if aws_data_exists:
     
        with open(os.path.join('.', DATA_DIR, AWS_FILE), 'r') as fp:
            aws_data: Dict = json.load(fp)
            return aws_data
    
    # if the data does not exists, a fresh scrape is required
    aws_data: Dict = scrape_aws_data()

    # store data 
    store_aws_data(aws_data)

    return aws_data



