from textblob import TextBlob
import nltk
import json
import requests
from pathlib import Path
from datetime import datetime
from time import sleep
import re
import os

import ImageUtil
import VoiceUtil
import VideoUtil
import SubtitleUtil

def LoadConfig(text):    
    with open('config.json', 'r') as f:
        config = json.load(f)
    paragraphs=text.split('\n')
    if paragraphs[0].startswith("!") and paragraphs[0].strip().endswith("!"):
        match = re.search(r'(?<=!)(.*?)(?=!)', paragraphs[0])
        styles= match.group(1).split(",")
        
        for s in styles:
            if s.lower() in config["styles"].keys():
                for k in config["styles"][s].keys():
                    config[k]=config["styles"][s][k]
        del paragraphs[0]
    config["paragraphs"]=paragraphs    
    return config

def BackupText(text, config):
    path="output\\" + text[:10].replace(":","_").replace(" ","_").replace("\n","_") +"_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    os.makedirs(path)
    filename = "Gen_" + datetime.now().strftime("%m_%d_%Y%H_%M_%S")+ "_.txt"
    with open(path + "\\" + filename, 'w', encoding='utf-8') as outfile:
            if "text_prompt" in config.keys():
                outfile.write(config["text_prompt"] + "\n")
            outfile.write(text + "\n")
    return path
   
def Generate(text, config):
    VoiceUtil.setup(config)
    ind=0
    imageFiles=[]
    audioFiles=[]
    path=BackupText(text, config)
    paragraphs = config["paragraphs"]
    subtitle=["",0]
    for para in paragraphs:
        if para.strip():
            print(para + "\n")
            imagepath=ImageUtil.generate_image(para, ind, path, config)
            imageFiles.append(imagepath)
            voicepath=VoiceUtil.create_dialogue(para, path, ind, config)
            audioFiles.append(voicepath)
            subtitle= SubtitleUtil.updateSubtitle(subtitle, voicepath, para, ind)
            ind=ind+1
    with open(path + "\\" + "final.srt", 'w', encoding='utf-8') as outfile:
        outfile.write(subtitle[0])
    VideoUtil.combine_videos(path, imageFiles, audioFiles, config)            
