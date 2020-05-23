import os
import json

from typing import Dict

from .scraper import scrape_aws_data, store_aws_data


DATA_DIR = 'data'
AWS_FILE = 'aws_data.json'

def get_aws_data() -> Dict:
    
    return scrape_aws_data()


