import requests
import argparse
from nltk import sent_tokenize
from .contexts import ManualContexts, AwesomePrompts, CustomPrompt
from chatgpt_wrapper import ChatGPT
from chatgpt_wrapper.config import Config

'''
This function wraps user's petition question with the adequate context to better orient the response of the language model
'''

class Wrapper:

    def wrapper(self, query:str, key: str, context:str, model:str="text-davinci-003") -> str:
        ##### Contexts
        
        contexts = AwesomePrompts.dataset['act']
        contexts.extend(["doctor", "lawyer", "programmer"])
        contexts.extend(CustomPrompt.available_prompts)
        if not any(context==x for x in contexts):
            raise Exception("Sorry, that context is not implemented yet")
        if context=="doctor":
            context = ManualContexts.DoctorAdvice
        elif context=="lawyer":
            context = ManualContexts.Lawyer
        elif context=="programmer":
            context = ManualContexts.Programmer
        elif context.startswith('custom-'):
            custom_name = context[len('custom-'):]
            context = CustomPrompt(custom_name).prompt
        else:
            context = AwesomePrompts.dataset.filter(lambda x: x['act']==context)['prompt'][0]
            context = ' '.join(sent_tokenize(context)[:-1])
        
        ##### Models

        if model=="gpt-4": ### GPT-4
            config = Config()
            config.set('chat.model', 'gpt4')
            config.set('api.key', key)
            bot = ChatGPT(config)
            _, response, _ = bot.ask(context + " \"" + query+ "\"")
            
            return response

        else: #### Rest of Models
            url = 'https://api.openai.com/v1/completions'
            headers = {"Content-Type": "application/json; charset=utf-8", "Authorization":"Bearer "+key}
            myobj = {'model': model, 'prompt': context + " \"" + query+ "\"", "max_tokens":256, "temperature":0} # temperature is set to 0 by default since we want the most deterministic as possible responses
                                                                                                                        # max_tokens = 256 because we want a concrete explanation, better if it yes or no

            x = requests.post(url, headers =headers, json = myobj)
            
            return x.json()['choices'][0]['text']
