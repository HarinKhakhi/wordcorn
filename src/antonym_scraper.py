import argparse
from os import makedirs
from os.path import join, isdir
import json

import requests
from bs4 import BeautifulSoup
import threading

##################### Configuration ####################
parser = argparse.ArgumentParser()
parser.add_argument('--output_dir')
parser.add_argument('--test', default=argparse.SUPPRESS)

args = parser.parse_args()
output_dir = join(args.output_dir, 'files')
output_file = join(args.output_dir, 'all_combined.json')
is_test = True if 'test' in args else False

total_threads = 10

if not isdir(output_dir):
    makedirs(output_dir)

get_url = lambda word: f'https://www.antonym.com/antonyms/{word}'
#########################################################

def get_antonyms(html):
    antonyms = []

    antonyms_wrapper = html.find('div', class_='main-column')
    antonyms_wrapper = html.find('div', class_='section-list-wrapper')
    for antonyms_li in antonyms_wrapper.find_all('li'):
        antonym = antonyms_li.get_text().strip()
        antonyms.append(antonym)

    return antonyms

def get_data(word):
    url = get_url(word)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    with open(join(output_dir, f'{word}.txt'), 'w') as output_file:
        data = get_antonyms(soup)
        for ele in data:
            output_file.write(ele + '\n')


wordlist_file = open('../wc-db/justwords.txt')
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
        "antonyms": data
    })

with open(output_file, 'w') as output_file:
    json.dump(all_words, output_file, indent=4)

