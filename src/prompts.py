class MeaningsPrompt:
    def __init__(self, word):
        self.word = word

    def get_prompt(self):
        return [
            self.system(),
            self.user()
        ]

    def system(self):
        prompt = '''
            You will be given a word and your task is to provide the type of the word (eg. noun, verb, adjective etc.) and the meaning of the word in json format.
            {
                "word": "word here",
                "type": "type of the word here",
                "meaning": "meaning of the word here"
            }
        '''
        return {
            'role': 'system',
            'content': prompt
        }
    
    def user(self):
        prompt = f'''
            the word is {self.word}.
        '''

        return {
            'role': 'user',
            'content': prompt
        }

class SynonymsAndAntonymsPrompt:
    def __init__(self, word):
        self.word = word

    def get_prompt(self):
        return [
            self.system(),
            self.user()
        ]

    def system(self):
        prompt = '''
            You will be given a word and your task is to provide the list of top 3 synonyms and  top 3 antonyms in json format as below. 
            {
                "word": "word here",
                "synonyms": ["first", "second", "third"],
                "antonyms": ["first", "second", "third"]
            }
        '''
        return {
            'role': 'system',
            'content': prompt
        }
    
    def user(self):
        prompt = f'''
            the word is {self.word}.
        '''

        return {
            'role': 'user',
            'content': prompt
        }


class MnemonicsPrompt:
    def __init__(self, word):
        self.word = word

    def get_prompt(self):
        return [
            self.system(),
            self.user()
        ]

    def system(self):
        prompt = '''
            You will be given a word and your task is to provide 2 mnemonics for that word,
            first should be using the Loci (Memory Palace) Technique,
            second should be using visualization or emotional connection theme pattern.
            give me the response in following json format,
            and don't include the type of mnemonic, just give me the mnemonic in the specified key
            {
                "word": "word here",
                "mnemonics": [
                    {
                        "mnemonicId": 1,
                        "mnemonic": "first mnemonic here"
                    },
                    {
                        "mnemonicId": 2,
                        "mnemonic": "second mnemonic here"
                    }
                ]
            }
        '''
        return {
            'role': 'system',
            'content': prompt
        }
    
    def user(self):
        prompt = f'''
            the word is {self.word}.
        '''

        return {
            'role': 'user',
            'content': prompt
        }

class StoryPrompt:
    def __init__(self, word):
        self.word = word

    def get_prompt(self):
        return [
            self.system(),
            self.user()
        ]

    def system(self):
        prompt = '''
            I will give you a word and you have to write a story using that. The story should include all the important elements,
            - Strong Opening, Well-Defined Characters, Clear Setting, Conflict or Tension, Plot Structure, Pacing, Dialogue, Theme, Twist or Surprise, Economy of Language, Resolution, Emotional Resonance. 
            The story should not be larger than 250 words.  The exact word should be used in story multiple times.
            The response should follow the mentioned json format
            {
                "word": "word here",
                "story": "story here"
            }
        '''
        return {
            'role': 'system',
            'content': prompt
        }
    
    def user(self):
        prompt = f'''
            the word is {self.word}.
        '''

        return {
            'role': 'user',
            'content': prompt
        }

class UsagePrompt:
    def __init__(self, word):
        self.word = word

    def get_prompt(self):
        return [
                self.system(),
                self.user()
        ]

    def system(self):
        prompt = '''
            I will give you a word and you have to give a list of 2-4 sentences where the given word is used. 
            The response should follow the given JSON format,
            {
                "word": "word here",
                "usage": [
                    "first sentence",
                    "second sentence",
                    "third sentence"
                ]
            }
        '''
        return {
            'role': 'system',
            'content': prompt
        }

    def user(self):
        prompt = f'''
            the word is {self.word}
        '''
        return {
            'role': 'system',
            'content': prompt
        }

class QuestionsPrompt:
    def __init__(self, word):
        self.word = word

    def get_prompt(self):
        return [
                self.system(),
                self.user()
        ]

    def system(self):
        prompt = '''
            I am creating a quiz for students to check the knowledge of their vocabulary. 
            I will give you a word and you hav to give me a multiple choice single answer question whose answer will be the given word
            You response should follow the given JSON format,
            {
                "word": "word here",
                "question": {
                    "question": "question here",
                    "options": ["list of four options here"],
                    "correctAnswer": "correct answer here"
                } 
                
            }

            For example,
            {
                "word": "catalyst",
                "question": {
                  "question": "The new project acted as a __________ for change, sparking innovation and driving progress in the industry.",
                  "options": ["barrier", "trigger", "catalyst", "obstacle"],
                  "correctAnswer": "catalyst"
                }
            }

        '''
        return {
            'role': 'system',
            'content': prompt
        }

    def user(self):
        prompt = f'''
            the word is {self.word}
        '''
        return {
            'role': 'system',
            'content': prompt
        }

class TagPrompt:
    def __init__(self, word):
        self.word = word

    def get_prompt(self):
        return [
                self.system(),
                self.user()
        ]

    def system(self):
        prompt = '''
            I will give a word and you have to help me categorize them into top 3 categories.
            The categories should not be about the word type such as verb, adjective etc.
            Your response should follow JSON format as specified,
            {
                "word": "word here",
                "tags": ["first tag", "second tag", "third tag"]
            }

            for example,
            {
                "word": "catalyst",
                "tags": ["Chemistry", "Reaction", "Motivation"]
            }
        '''
        return {
            'role': 'system',
            'content': prompt
        }

    def user(self):
        prompt = f'''
            the word is {self.word}
        '''
        return {
            'role': 'system',
            'content': prompt
        }
    
class DifficultyScorePrompt:
    def __init__(self, word):
        self.word = word

    def get_prompt(self):
        return [
            self.system(),
            self.user()
        ]

    def system(self):
        prompt = '''
            I am creating English Word Learning App.
            You will be given a word and your task is to give me an integer value (in string format) in the range of 1 to 5 (inclusive) which represents the difficulty of the word
            Return your response in the following json format
            {
                "word": "word here",
                "difficultyScore": "integer score here"
            }
        '''
        return {
            'role': 'system',
            'content': prompt
        }
    
    def user(self):
        prompt = f'''
            the word is {self.word}.
        '''

        return {
            'role': 'user',
            'content': prompt
        }
