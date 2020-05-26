from invoke import task

from wolk.scraper import scrape, upload_data

@task
def build(c):
    """Build the dataset by uploading to S3

    Arguments:
        c {object} -- context
    """
    scrape()
    upload_data()