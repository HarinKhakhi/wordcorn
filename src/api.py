from dotenv import load_dotenv
import json

from fastapi import FastAPI
from openai import OpenAI

import utils as utils
from models import ConfigurationModel

###################### Configuration ###################### 
load_dotenv()

api = FastAPI()
openai_client = OpenAI()

current_config = utils.load_configuration(file='./assets/default_config.json')
logger = utils.get_logger('api')

logger.info('server started...')
logger.info('current configuration: %s', current_config.model_dump())
###########################################################

@api.post('/configure')
def configure_server(configuration: ConfigurationModel):
    logger.debug('/configure called with new configuration: ', configuration.model_dump())
    
    current_config = configuration

    return {
        'configuration': current_config.model_dump(exclude_none=True)
    }
    

@api.get('/get-story')
def get_story(word):
    logger.debug(f'/get-story?word={word} called')

    config_dict = current_config.model_dump(exclude_none=True)
    config_dict['messages'].append({
        'role': 'user',
        'content': f'the word is {word}'
    })

    logger.debug('calling chatgpt-api with args: %s', json.dumps(config_dict, indent=4))
    response = openai_client.chat.completions.create(
        **config_dict
    )
    logger.info('got response: %s', response)    

    return_response = json.loads(response.choices[0].message.content)
    return return_response


@api.get('/health-check')
def health_check():
    return {
        'health': 'good'
    }