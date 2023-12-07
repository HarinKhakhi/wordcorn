from datetime import datetime
from os import path
import json
import logging

from src.models import ConfigurationModel, MessageModel

def load_configuration(file = './assets/default_config.json'):
    if not path.isfile(file):
        raise Exception(f'configuration file {file} not found!')
    
    config_file = open(file)
    config_dict = json.load(config_file)
    config_file.close()

    for message in config_dict['messages']:
        prompt_file = open(message['content'])
        prompt = prompt_file.read()
        message['content'] = prompt
        prompt_file.close()

    return ConfigurationModel(**config_dict)


def get_logger(name, dir='./logs'):
    logger = logging.getLogger(name)
    
    # setting up file handler
    current_datetime_str = datetime.now().strftime('%d_%m_%Y')
    fileHandler = logging.FileHandler(filename=f'{dir}/logs-{current_datetime_str}.log', mode='a')

    # setting up formatter
    formatter = logging.Formatter('%(levelname)s | %(asctime)s: %(message)s')
    fileHandler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)

    return logger