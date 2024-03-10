from datetime import datetime
from os import path
import os
import json
import logging

from openai import OpenAI

class Database:
    '''handles file saving, loading and combining results'''

    def __init__(self, logger, db_path, name, data_dir='data'):
        self.logger = logger
        self.name = name
        self.db_path = path.join(db_path, name)
        self.db_data_path = path.join(self.db_path, data_dir)

        # creating db directories if not present
        if not path.isdir(self.db_path): 
            os.makedirs(self.db_path)
        if not path.isdir(self.db_data_path):
            os.makedirs(self.db_data_path)

    def does_exist(self, word):
        file_path = path.join(self.db_data_path, f'{word}.txt')
        return path.isfile(file_path)

    def load_json_data(self, filename, is_path=False):
        try:
            file_path = filename
            if not is_path:
                file_path = path.join(self.db_data_path, filename)

            with open(file_path, 'r') as file: 
                return json.load(file)
        except:
            return {
                'word': filename
            }

    def save_data(self, word, content):
        file_path = path.join(self.db_data_path, f'{word}.txt')
        file = open(file_path, 'w')
        file.write(content)
        file.close()


    def combine_results(self, filename):
        '''combines all the data in data_diretory where all individual data is stored'''
        
        all_data = []
        for _filename in os.listdir(self.db_data_path):
            obj = self.load_json_data(_filename)
            all_data.append(obj)

        file_path = path.join(self.db_path, filename)
        with open(file_path, 'w') as file:
            json.dump(all_data, file, indent=4)

class ChatGPT:
    '''a wrapper around chatgpt-api'''
    def __init__(self, logger, model='gpt-3.5-turbo-1106'):
        # default config
        self.config = {
            'model': model,
            'messages': [],
            'response_format': {
                'type': 'json_object'
            }
        }    
        self.chatgpt_client = OpenAI()
        self.logger = logger


    def ask(self, prompts):
        '''
        call the chatgpt api using the given prompt 
        '''

        self.logger.debug('calling chatgpt-api with args: %s', json.dumps(prompts, indent=4))    

        self.config['messages'] = prompts
        response = self.chatgpt_client.chat.completions.create(
            **self.config
        ) 

        self.logger.info('got response: %s', response) 

        return response

    def get_message(self, response):
        '''extracts the content from completions object'''
        return response.choices[0].message.content


def get_wordlist(input_file, is_test):
    wordlist_file = open(input_file, encoding='utf-8')
    wordlist = []

    if is_test:
        for _ in range(10):
            line = wordlist_file.readline().rstrip()
            wordlist.append(line)
    else:
        wordlist = [word.rstrip() for word in wordlist_file.readlines()]

    wordlist_file.close()
    return wordlist


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
