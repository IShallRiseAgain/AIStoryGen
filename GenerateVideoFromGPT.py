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
import TextGenUtil

def combine_videos(path, audioimagefiles):
    folder_path = "." + path
    output_filename = path + "\\" + "final.mp4"
    count = len(imagefiles)
    concat_command= "[0][1][2][3][4][5]concat=n=" + str(count) + ":v=1:a=1[vv][a];[vv]format=yuv420p[v]"
    ffmpeg_command = ["ffmpeg"] + generate_source_list() + ["-filter_complex"] + [concat_command] + ["-map", "[v]", "-map", "[a]", output_filename]
    # Run the FFmpeg command
    subprocess.run(ffmpeg_command, check=True, shell=True)
def generate_source_list():
    image_index=0
    sourceList = []
    for i in imagefiles:
        sourceList.append("-i")
        sourceList.append(i)
        sourceList.append("-i")
        sourceList.append(audiofiles[image_index])
    image_index=image_index+1
    return sourceList

prompt = Path('gptprompt.txt').read_text(encoding="utf-8")
output = TextGenUtil.gpt3_completion(prompt)
VoiceUtil.getVoiceList()
paragraphs=output.split('\n')
path="output\\" + output[:10].replace(":","_").replace(" ","_") +"_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
os.mkdir(path)
filename = "Gen_" + datetime.now().strftime("%m_%d_%Y%H_%M_%S")+ "_.txt"
with open(path + "\\" + filename, 'w', encoding='utf-8') as outfile:
        outfile.write(prompt)
        outfile.write(output)
ind=0
imagefiles=[]
audiofiles=[]
for para in paragraphs:
    if para.strip():
        print(para + "\n")
        imagepath=ImageUtil.generate_image(para, ind, path)
        imagefiles.append(imagepath)
        ind=ind+1
        line=para.split(":",maxsplit=1)
        result = VoiceUtil.create_dialogue(line, para)
        if VoiceUtil.enable_elevenAI:
            voicepath=VoiceUtil.generate_voice_ElevenAI(path, ind, result[0], result[1])
            audiofiles.append(voicepath)
        else:
            voicepath=VoiceUtil.generate_voice_pyttsx3(path, ind, result[0])
            audiofiles.append(voicepath)
combinevideos(path, files)            
