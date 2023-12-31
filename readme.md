## Instructions
1. Create and start virtual environment using the following command
```bash
python -m venv env
source env/bin/activate
```

2. Install required dependencies 
```bash
pip install -r requirements.txt
```

3. run the api.py by passing the word you want to create story for
```bash
python api.py abeyance
```

## Info
- Prompt Used: create a short ghost story in around 100 words using the word "{word}". Keep all the words simple except "{word}"

### Calculations

- ChatGPT API (https://openai.com/pricing)
	- gpt-3.5-turbo expected cost: 
	```
		= TOTAL_WORDS * (
			INPUT_TOKEN/1000 * 0.0010
						+
			OUTPUT_TOKEN/1000 * 0.0020
		  )
		= 10,000 * (25/1000 * 0.0010 + 200/1000 * 0.0020)
		= 10,000 * (0.000025 + 0.0004)
		= 4.25 $
	```
	- gpt-4 expected cost:
	```
		= TOTAL_WORDS * (
			INPUT_TOKEN/1000 * 0.0010
						+
			OUTPUT_TOKEN/1000 * 0.0020
		  )
		= 10,000 * (25/1000 * 0.03 + 200/1000 * 0.006)
		= 10,000 * (0.00075 + 0.0012)
		= 19.5 $
	```

- Google API (https://cloud.google.com/vertex-ai/docs/generative-ai/pricing)
	- palm 2 for text expected cost:
	```
		= TOTAL_WORDS * (
				TOTAL_INPUT_CHAR/1000 * 0.0005 
								+
				TOTAL_OUTPUT_CHAR/1000 * 0.0005
		  )
		= 10,000 * (200/1000 * 0.0005 + 1000/1000 * 0.0005)
		= 10,000 * (0.0001 + 0.0005)
		= 6 $
	```
=> HuggingFace API (https://huggingface.co/pricing), 0.06$ per hour
