import argparse
import os
import json
from tqdm import tqdm
from dotenv import load_dotenv
from copy import deepcopy
import threading

from openai import OpenAI
import utils as utils

###################### Configuration ###################### 
TOTAL_THREADS = 10

parser = argparse.ArgumentParser()

parser.add_argument('--wordlist', help='input wordlist')
parser.add_argument('--output_dir', help='output directory path')
parser.add_argument('--output_file', help='name of the file with all data combined (without ext)')
parser.add_argument('--operation_mode', help='[test, override, reuse]')

args = parser.parse_args()
wordlist_file = args.wordlist 
output_dir = args.output_dir
output_file = args.output_file 
operation_mode = args.operation_mode
if not os.path.isdir(output_dir): os.makedirs(output_dir)

load_dotenv()

openai_client = OpenAI()

current_config = utils.load_configuration(file='./assets/default_config.json')
current_config = current_config.model_dump(exclude_none=True)
logger = utils.get_logger('script')

logger.info('script started...')
logger.info('current configuration: %s', current_config)
###########################################################

############################ functions ############################ 
def get_wordlist(input_file):
    wordlist_file = open(input_file, encoding='utf-8')
    wordlist = [word.strip().lower().replace(',', '') for word in wordlist_file.readlines()]
    wordlist_file.close()

    return wordlist


def perform_task(word):
    global output_dir, operation_mode, current_config, logger, openai_client

    # check if already requested
    if (operation_mode == 'reuse') and os.path.isfile(f'{output_dir}/{word}.txt'):
        return

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


def combine_results(input_dir, output_file):
    def get_data(file):
        try:
            with open(file, 'r') as f: 
                return json.load(f)
        except:
            print('not json:', word)
            return {}

    arr = []
    for filename in os.listdir(input_dir):
        obj = {
            'word': filename.split('.')[0],
            **get_data(os.path.join(input_dir, filename))
        }
        arr.append(obj)

    with open(output_file, 'w') as output:
        json.dump(arr, output, indent=4)
###########################################################

wordlist = get_wordlist(wordlist_file)
total_count = len(wordlist) if operation_mode != 'test' else TOTAL_THREADS

for start_i in tqdm(range(0, total_count, TOTAL_THREADS)):
    threads = []
    for word in wordlist[start_i: start_i+TOTAL_THREADS]:
        thread = threading.Thread(target=perform_task, args=(word, ))
        thread.start()
        threads.append(thread)

    for thread in threads: thread.join()

combine_results(output_dir, output_file)
