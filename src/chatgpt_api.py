from argparse import ArgumentParser
from time import sleep
from dotenv import load_dotenv
import threading
from tqdm import tqdm

import utils
import prompts

###################### Configuration ###################### 
parser = ArgumentParser()

# required
parser.add_argument('--name', help='title your data')
parser.add_argument('--wordlist', help='input wordlist')
parser.add_argument('--database', help='path to directory where all files will be stored')
parser.add_argument('--prompt', help='prompt which will be passed to chatgpt')
# optional
parser.add_argument('--test', action='store_true', help='run the script for only few words')
parser.add_argument('--reuse', action='store_true', help='reuse the old data if present')
parser.add_argument('--threads', type=int, default=10, help='number of threads to run') 

args = parser.parse_args()

# mapping cli args to variable names 
script_name = args.name 
wordlist_filepath = args.wordlist
db_path = args.database
prompt_name = args.prompt
is_test = args.test
reuse_data = args.reuse
total_threads = args.threads
###################################################################

############################ functions ############################ 
def perform_task(chatgpt, database, word, prompt):
    response = chatgpt.ask(prompt.get_prompt())
    response = chatgpt.get_message(response)

    database.save_data(word, response)
###########################################################

load_dotenv()
logger = utils.get_logger('chatgpt-script')
chatgpt = utils.ChatGPT(logger)
database = utils.Database(logger, db_path, name=script_name)

logger.info('script started...')
logger.info('current configuration: %s', chatgpt.config)

wordlist = utils.get_wordlist(wordlist_filepath, is_test)
total_words = len(wordlist)

for start_i in tqdm(range(0, total_words, total_threads)):
    threads = []

    any_new_found = False
    for word in wordlist[start_i: start_i+total_threads]:

        # check if already requested
        if reuse_data and database.does_exist(word): 
            continue
        
        any_new_found = True
        prompt = prompts.MeaningsPrompt(word)
        # prompt = prompts.SynonymsAndAntonymsPrompt(word)
        # prompt = prompts.MnemonicsPrompt(word)
        # prompt = prompts.StoryPrompt(word)
        # prompt = prompts.UsagePrompt(word)
        # prompt = prompts.QuestionsPrompt(word)
        # prompt = prompts.TagPrompt(word)

        thread = threading.Thread(target=perform_task, args=(chatgpt, database, word, prompt))
        thread.start()
        threads.append(thread)

    for thread in threads: thread.join()
    if any_new_found: sleep(20)

database.combine_results('all_combined.json')
