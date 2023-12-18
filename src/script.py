import sys
import os
import json
from tqdm import tqdm
from dotenv import load_dotenv
from copy import deepcopy

from openai import OpenAI
import utils as utils

###################### Configuration ###################### 
input_file = sys.argv[1]
output_dir = sys.argv[2]
output_file = sys.argv[3]

load_dotenv()

openai_client = OpenAI()

current_config = utils.load_configuration(file='./assets/default_config.json')
current_config = current_config.model_dump(exclude_none=True)
logger = utils.get_logger('script')

logger.info('script started...')
logger.info('current configuration: %s', current_config)
###########################################################
if not os.path.isdir(output_dir): os.makedirs(output_dir)

wordlist_file = open(input_file, encoding='utf-8')
wordlist = wordlist_file.readlines()
wordlist_file.close()

new_count = 0
for line in tqdm(wordlist[:10]):
    word = line.strip().lower()

    # check if already requested
    if os.path.isfile(f'{output_dir}/{word}.txt'):
        continue

    new_count += 1
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
    object_file = open(f'{output_dir}/{word}.txt', 'w')
    object_file.write(json_object)
    object_file.close()

print(f'called openai api for {new_count} words')

def get_data(file):
    with open(file, 'r') as f: 
        return str(f.read())


arr = []
for filename in os.listdir(output_dir):
    obj = {
        'word': filename.split('.')[0],
        'mnemonic': get_data(os.path.join(output_dir, filename))
    }
    arr.append(obj)

with open(output_file, 'w') as output:
    json.dump(arr, output, indent=4)