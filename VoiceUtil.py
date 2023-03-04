import json
import requests
import random
import pyttsx3
import gender_guesser.detector as gender
import re

apiKey = ""
availableMaleVoices ={}
availableFemaleVoices = {}
voiceGender = {"domi":"female"}
voices = {}
narratorName = "narrator"

def setup(config):
    apiKey=config["elevenlabs_key"]
    voice_type=config["voice_type"]
    if config["voice_type"]=="ElevenLabs":
        api_url = "https://api.elevenlabs.io/v1/voices"
        headers = {
            'xi-api-key': apiKey
        }
        response = requests.get(api_url, headers=headers).json()
        for item in response["voices"]:
                if item["name"].lower() in config["voice_exclude"]:
                    continue
                elif item["name"].lower() in config["character_mappings"].keys():
                    for m in config["character_mappings"][item["name"].lower()]:
                        voices[m]=item["voice_id"]
                elif item["name"].lower() in voiceGender.keys():
                    if voiceGender[item["name"].lower()] == "female":
                        availableFemaleVoices[item["name"].lower()]=item["voice_id"]
                    else:
                        availableMaleVoices[item["name"].lower()]=item["voice_id"]                    
                else:
                    d = gender.Detector(case_sensitive=False)
                    if detect_gender(item["name"],d):
                        availableFemaleVoices[item["name"].lower()]=item["voice_id"]
                    else:    
                        availableMaleVoices[item["name"].lower()]=item["voice_id"]
    else:
        return

def detect_gender(text, detector):
    genderCheck = detector.get_gender(text.lower().split(" ")[0])
    if "female" in genderCheck:
        return True
    return False
    
def create_dialogue(text, path, ind, config):
    curVoice="None"
    line=text.split(":",maxsplit=1)
    if(len(line)>1):
        dialogue=line[1]        
        if config["voice_type"]=="ElevenLabs":
            #Don't voice bracketed text
            pattern = r"[\(\[].*?[\)\]]"
            dialogue= re.sub(pattern, '', dialogue)
            if line[0].lower() in voices:
                curvoice=voices[line[0].lower()]
            else:
                d = gender.Detector(case_sensitive=False)
                if detect_gender(line[0],d):
                    if len(availableFemaleVoices.keys())>0:
                        key = random.choice(list(availableFemaleVoices.keys()))
                        curvoice=voices[line[0].lower()]= availableFemaleVoices[key]
                        availableFemaleVoices.pop(key)
                    else:
                        curvoice=voices[line[0].lower()]=random.choice(list(voices.values()))
                else:
                    if len(availableMaleVoices.keys())>0:
                        key = random.choice(list(availableMaleVoices.keys()))
                        curvoice=voices[line[0].lower()]= availableMaleVoices[key]
                        availableMaleVoices.pop(key)
                    else:
                        curvoice=voices[line[0].lower()]=random.choice(list(voices.values()))
            return generate_voice_ElevenAI(path, ind, dialogue, curvoice, config["elevenlabs_key"])      
        else:
            return generate_voice_pyttsx3(path, ind, dialogue)
        
    else:
        #Need default if line has no speaker
        if config["voice_type"]=="ElevenLabs":
            if narratorName.lower() in voices.keys():
                return generate_voice_ElevenAI(path, ind, text, voices[narratorName.lower()], config["elevenlabs_key"])
            else:
                key = random.choice(list(availableMaleVoices.keys())) 
                curvoice=voices[narratorName.lower()]=availableMaleVoices[key]
                availableMaleVoices.pop(key)
                return generate_voice_ElevenAI(path, ind, text, curvoice, config["elevenlabs_key"])
        else:
            return generate_voice_pyttsx3(path, ind, text)
        
def generate_voice_pyttsx3(path, ind, dialogue):
        engine = pyttsx3.init()
        voice_path=path+ "\\audio_" + str(ind) + ".mp3"
        engine.save_to_file(dialogue, voice_path)
        engine.runAndWait()
        engine.stop()
        return voice_path

def generate_voice_ElevenAI(path, ind, dialogue, voice_id, apiKey):
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
