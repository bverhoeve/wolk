import os

DATA_DIR = 'data'

S3_BUCKET = 'wolk.data'


AWS_DIR = 'aws'
AWS_DEFAULT_DATA_LOC = os.path.join(DATA_DIR, AWS_DIR)
AWS_EC2_FILE = 'ec2_instances.json'
AWS_RDS_FILE = 'rds_instances.json'