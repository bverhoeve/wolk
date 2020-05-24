from flask import Flask
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

from wolk import routes