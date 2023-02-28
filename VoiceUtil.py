import json
import requests
import random
import pyttsx3

with open('ElevenLabs.txt', 'r') as infile:
    apikey = infile.read()
enable_elevenAI=False
availableVoices ={}
narratorVoice="Josh"
narratorName="narrator"
voices = {}


def getVoiceList():
    api_url = "https://api.elevenlabs.io/v1/voices"
    response = requests.get(api_url).json()
    for item in response["voices"]:
            if item["name"]==narratorVoice:
                voices[narratorName]=item["voice_id"]
            else:    
                availableVoices[item["name"]]=item["voice_id"]
                
def create_dialogue(line, text):
    curVoice="None"
    if(len(line)>1):
        dialogue=line[1]
        if line[0] in voices:
            curvoice=voices[line[0]]
        else:
            key = random.choice(list(availableVoices.keys())) 
            curvoice=voices[line[0]]= availableVoices[key]
            availableVoices.pop(key)
        return [text, curvoice]   
        
    else:
        if narratorName in voices:
            curvoice=voices[narratorName]
        else:
            key = random.choice(list(availableVoices.keys())) 
            curvoice=voices[narratorName]=availableVoices[key]
            availableVoices.pop(key)
        return [text, curvoice]
        
def generate_voice_pyttsx3(path, ind, dialogue):
        engine = pyttsx3.init()
        voice_path=path+ "\\audio_" + str(ind) + ".mp3"
        engine.save_to_file(dialogue, voice_path)
        engine.runAndWait()
        engine.stop()
        return voice_path

def generate_voice_ElevenAI(path, ind, dialogue, voice_id):
    url = 'https://api.elevenlabs.io/v1/text-to-speech/' + voice_id + '/stream'
    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': apiKey,
        'Content-Type': 'application/json'
    }
    data = {
        "text": dialogue,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        voice_path=path + "\\audio_" + str(ind) + ".mp3"
        with open(voice_path, 'wb') as f:
            f.write(response.content)
        return voice_path
    else:
        print('Error:', response.status_code, response.content.decode())
        return None
