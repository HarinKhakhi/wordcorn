from argparse import ArgumentParser
import json

import utils

# parsing arguments
parser = ArgumentParser()
parser.add_argument('--wordlist', help='input wordlist')
parser.add_argument('--data', help='path to directory where all files will be stored')
args = parser.parse_args()
wordlist_path = args.wordlist
data_path = args.data

# loading wordlist
wordlist = utils.get_wordlist(wordlist_path, is_test=False)
# wordlist = set(wordlist)

# loading data
data_file = open(data_path, 'r')
all_combined_data = json.load(data_file)
data_file.close()
all_combined = {}
for word_data in all_combined_data:
    if 'word' not in word_data.keys(): print(word_data)
    all_combined[word_data['word']] = word_data

# generating report
not_found = []
extra = []
fields = {}
for word_data in all_combined.values():
    word_fields = tuple(word_data.keys())
    fields[word_fields] = fields.get(word_fields, 0) + 1

    word = word_data['word']
    if word not in wordlist:
        extra.append(word)


for word in wordlist:
    if word not in all_combined:
        not_found.append(word)


print('='*10, 'Report', '='*10)
print(f'not_found: {len(not_found)} ({not_found[:5]})')
print(f'extra: {len(extra)} ({extra[:5]})')
print('shape of data:')
for field_shape, count in fields.items():
    print(field_shape, '->', count)
print('='*28)
