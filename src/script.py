from os import path
import json
from tqdm import tqdm
from dotenv import load_dotenv
from copy import deepcopy

from openai import OpenAI
import utils as utils

###################### Configuration ###################### 
load_dotenv()

openai_client = OpenAI()

current_config = utils.load_configuration(file='./assets/default_config.json')
current_config = current_config.model_dump(exclude_none=True)
logger = utils.get_logger('script')

logger.info('script started...')
logger.info('current configuration: %s', current_config)
###########################################################

dir = './data/out'

wordlist_file = open(f'./data/wordlist.txt', encoding='utf-8')
wordlist = wordlist_file.readlines()
wordlist_file.close()

for line in tqdm(wordlist):
    word = line.strip()

    # check if already requested
    if path.isfile(f'{dir}/{word}.json'):
        continue

    # setting up configuration
    new_config = deepcopy(current_config)
    new_config['messages'].append({
        'role': 'user',
        'content': f'the word is {word}'
    })

    # calling api
    logger.debug('calling chatgpt-api with args: %s', json.dumps(new_config, indent=4))    
    response = openai_client.chat.completions.create(
        **new_config
    )
    logger.info('got response: %s', response) 

    # writing to file
    json_object = response.choices[0].message.content
    object_file = open(f'{dir}/{word}.txt', 'w')
    object_file.write(json_object)
    object_file.close()
