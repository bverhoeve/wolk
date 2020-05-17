from flask import render_template, url_for
from wolk import app

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
    page_logo = url_for('static', filename='assets/aws_logo.svg')
    return render_template('aws.html', page_logo=page_logo)

@app.route('/azure')
def azure():
    return 'Microsoft Azure page'

@app.route('/gcp')
def gcp():
    return 'GCP'