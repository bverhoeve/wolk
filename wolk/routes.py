from flask import render_template, url_for
from typing import Dict

from wolk import app
from .scraper import scrape
from .data import get_aws_data

AWS_LOGO = 'assets/aws_logo.svg'
AZURE_LOGO = 'assets/microsoft_azure_logo.svg'
GCP_LOGO = 'assets/google_cloud_logo.svg'

servers = [
        {
            'cloud_provider': 'AWS',
            'name': 'T2 micro',
            'api_name': 't2.micro',
            'memory': '2 GiB',
            'vCPUs': '2',
            'GPUs': '0',
            'GPU_model': 'None',
            'storage': 'EBS Only',
            'network_performance': '25 Mbps',
            'linux_on_demand_cost': '$5 hourly',
            'windows_on_demand_cost': '$20 hourly',
        },
        {
            'cloud_provider': 'AWS',
            'name': 'T2 micro',
            'api_name': 't2.micro',
            'memory': '2 GiB',
            'vCPUs': '2',
            'GPUs': '0',
            'GPU_model': 'None',
            'storage': 'EBS Only',
            'network_performance': '25 Mbps',
            'linux_on_demand_cost': '$5 hourly',
            'windows_on_demand_cost': '$20 hourly',
        }
    ]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', servers=servers)

@app.route('/aws')
def aws():
    instances = get_aws_data('ec2')
    page_logo = url_for('static', filename=AWS_LOGO)
    region = 'us-east-1'
    reserved_type = 'yrTerm1Convertible.allUpfront'

    return render_template('aws.html', page_logo=page_logo, instances=instances, region=region, reserved_type=reserved_type)

@app.route('/azure')
def azure():
    page_logo = url_for('static', filename=AZURE_LOGO)
    return render_template('azure.html', page_logo=page_logo)

@app.route('/gcp')
def gcp():
    page_logo = url_for('static', filename=GCP_LOGO)
    return render_template('google_cloud.html', page_logo=page_logo)