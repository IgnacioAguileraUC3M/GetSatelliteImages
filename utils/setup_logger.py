import logging 
import logging.config
import json
import logging


def setup_logging():
    with open('./config/logging.json', 'r') as fp:
        loggingconfig = json.load(fp)
    logging.config.dictConfig(loggingconfig)
