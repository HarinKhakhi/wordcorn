import argparse
from os import makedirs
from os.path import join, isdir
import json

import requests
from bs4 import BeautifulSoup
import threading

ANTONYMS_L0_CLASS = {
    'type': 'li',
    'class': 'border-antonym-rel-level-0'
}
ANTONYMS_L1_CLASS_TAG = {
    'type': 'li',
    'class': 'border-antonym-rel-level-1'
}
MEANING_CLASS_TAG = {
    'type': 'div',
    'class': 'definition-cluster'
}


##################### Configuration #####################
parser = argparse.ArgumentParser()
parser.add_argument('--total_threads', type=int, default=10)
parser.add_argument('--wordlist_file', type=str)
parser.add_argument('--output_dir', type=str)
parser.add_argument('--output_file', type=str)
parser.add_argument('--scrape_tag', type=str)
parser.add_argument('--test', default=argparse.SUPPRESS)

args = parser.parse_args()
total_threads = args.total_threads
wordlist_file = args.wordlist_file
output_dir = args.output_dir
output_file = args.output_file
scrape_tag = args.scrape_tag
is_test = True if 'test' in args else False

if not isdir(output_dir):
    makedirs(output_dir)

get_url = lambda word: f'https://www.yourdictionary.com/{word}'
#########################################################

def get_antonyms(html):
    antonyms = []
    for antonyms_li in html.find_all('li', class_='border-antonym-rel-level-0'):
        antonym = antonyms_li.get_text()
        antonyms.append(antonym)
    return antonyms


def get_meanings(html):
    meanings = []
    for meaning_div in html.find_all('div', class_='definition-cluster'):
        meaning = next(next(meaning_div.children).children).get_text()
        meanings.append(meaning)
    return meanings

def get_data(word):
    url = get_url(word)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    with open(join(output_dir, f'{word}.txt'), 'w') as output_file:
        data = []
        if scrape_tag == 'meanings':
            data = get_meanings(soup)
            for ele in data:
                output_file.write(ele + '\n')
        elif scrape_tag == 'antonyms':
            data = get_antonyms(soup)
            for ele in data:
                output_file.write(ele + '\n')
    
###################### Scraping #########################
wordlist_file = open(wordlist_file, encoding='utf-8')
wordlist = [word.strip().lower().replace(',', '') for word in wordlist_file.readlines()]
wordlist_file.close()

if is_test: wordlist = wordlist[:total_threads]

index = 0
total_words = len(wordlist)
while index < len(wordlist):
    remaining = total_words - index 
    print(f'remaining: {(remaining/total_words):.2%}', end='\r')

    threads = []
    for thread_i in range(total_threads):
        if index >= len(wordlist): break

        word = wordlist[index]
        index += 1

        thread = threading.Thread(target=get_data, args=(word, ))
        threads.append(thread)

        thread.start()

    for thread in threads:
        thread.join()


########################### Combining ######################
all_words = []
for word in wordlist:
    data_file = open(join(output_dir, f'{word}.txt'))
    data = data_file.read().strip().split('\n')
    data_file.close()

    all_words.append({
        "word": word,
        f"{scrape_tag}": data
    })

with open(output_file, 'w') as output_file:
    json.dump(all_words, output_file, indent=4)
