from textblob import TextBlob
import nltk
import json
import requests
from pathlib import Path
from datetime import datetime
from time import sleep
import re
import os
import subprocess
import win32api

import ImageUtil
import VoiceUtil
import VideoUtil

with open('config.json', 'r') as f:
    config = json.load(f)    
output=Path('storyprompt.txt').read_text(encoding="utf-8")
VoiceUtil.setup(config)
paragraphs=output.split('\n')
path="output\\" + output[:10].replace(":","_").replace(" ","_").replace("\n","_") +"_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
os.mkdir(path)
filename = "Gen_" + datetime.now().strftime("%m_%d_%Y%H_%M_%S")+ "_.txt"
with open(path + "\\" + filename, 'w', encoding='utf-8') as outfile:
        outfile.write(output)
ind=0
imageFiles=[]
audioFiles=[]
for para in paragraphs:
    if para.strip():
        print(para + "\n")
        imagepath=ImageUtil.generate_image(para, ind, path, config)
        imageFiles.append(imagepath)
        voicepath=VoiceUtil.create_dialogue(para, path, ind, config)
        audioFiles.append(voicepath)        
        ind=ind+1
VideoUtil.combine_videos(path, imageFiles, audioFiles)            
