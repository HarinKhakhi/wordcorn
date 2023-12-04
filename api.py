import sys
import logging
import json
from datetime import datetime
from dotenv import load_dotenv

from openai import OpenAI

######################## Configuration ########################
# loads all environmental variable (you should have .env file)
load_dotenv()

# setting up logger
logger = logging.getLogger('api')

# setting up file handler
current_datetime_str = datetime.now().strftime('%d_%m_%Y')
fileHandler = logging.FileHandler(filename=f'logs/logs-{current_datetime_str}.log', mode='a')

# setting up formatter
formatter = logging.Formatter('%(levelname)s | %(asctime)s: %(message)s')
fileHandler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)
###############################################################

########################## Settings ###########################
class Settings: 
    seed = 2023
    model = 'gpt-3.5-turbo'
    # model = 'gpt-4'
    max_tokens = 200
    temperature = 0.7

    system_prompt = "You are story writer who is helping english learning students understand meaning of words by using them in stories."
    user_prompt   = lambda word: f"create a short ghost story in around 100 words using the word '{word}' . Keep all the words simple except '{word}'."
###############################################################

def get_ghost_story(logger, word):
    '''
    returns a ghost story generated by chatgpt as a string which uses the input word
    '''
    
    logger.debug(f'requesting ghost story for word "{word}"...')

    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model = Settings.model,
            messages=[
                {
                    "role": "user", 
                    "content": Settings.user_prompt(word)
                }
            ],
            seed = Settings.seed,
            max_tokens = Settings.max_tokens,
            temperature= Settings.temperature
        )

        # response format https://platform.openai.com/docs/guides/text-generation/chat-completions-response-format
        ghost_story = response.choices[0].message.content

        logger.debug(f'request for ghost story of word "{word}" was successfull')
        logger.info(f'ghost story for word "{word}" is,\n{ghost_story}')
        logger.info(f'usage to get ghost story for word "{word}" is {json.dumps(dict(response.usage), indent=4)}')

        return ghost_story

    except Exception as e:
        logger.error(f'error while requesting ghost story for word "{word}": {str(e)}')
        raise

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: python api.py your_word_goes_here')
        exit(1)

    word = sys.argv[1]
    ghost_story = get_ghost_story(logger, 'abeyance')
    print(f'ghost story created using word "{word}",')
    print(ghost_story)