import openai

import requests
import json

def chatGPT(prompt):
    headers = {
        'Authorization': 'Bearer ' + openai.api_key,
        "content-type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    url = "https://api.openai.com/v1/chat/completions"
    response = requests.post(url, headers=headers, json=data).json()
    return response["choices"][0]["message"]["content"]
    
def gpt3_completion(prompt, engine='text-davinci-003', temp=1.1, top_p=1.0, tokens=4000, freq_pen=0.0, pres_pen=0.0, stop=['asdfasdf']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,         # use this for standard models
                #model=engine,           # use this for finetuned model
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            #save_gpt3_log(prompt, text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return None
            print('Error communicating with OpenAI:', oops)
            sleep(1)

def generateText(prompt, config):
    openai.api_key = config["open_ai_key"]
    if config["chatgpt_api"]:
        return chatGPT(prompt)
    else:
        return gpt3_completion(prompt)
        
