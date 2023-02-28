from textblob import TextBlob
import nltk
import json
import requests
import io
import base64
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw
import openai
from time import sleep
import re
import os
import subprocess
import win32api
import pyttsx3
import textwrap

with open('openaiapikey.txt', 'r') as infile:
    openai.api_key = infile.read()

def combinevideos(path, audioimagefiles):
    folder_path = "." + path
    output_filename = path + "\\" + "final.mp4"
    count = len(audioimagefiles)/4
    concat_command= "[0][1][2][3][4][5]concat=n=" + str(count) + ":v=1:a=1[vv][a];[vv]format=yuv420p[v]"
    ffmpeg_command = ["ffmpeg"] + audioimagefiles + ["-filter_complex"] + [concat_command] + ["-map", "[v]", "-map", "[a]", output_filename]
    # Run the FFmpeg command
    subprocess.run(ffmpeg_command, check=True, shell=True)

def add_subtitles(img, text):
    # Create an ImageDraw object and set the font and size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', size=20)

    text_width, text_height = font.getsize(text)
    max_width = (img.width * 2) - 10
    text_lines = textwrap.wrap(text, width=max_width // font.size)

    # Calculate y position for the bottom center of the image
    text_y = image.height - (text_height * len(text_lines)) - 20
    outline_color = (0, 0, 0, 255)
    outline_size = 2

    # Draw the text
    for line in text_lines:
        line_width, line_height = font.getsize(line)
        text_x = (image.width - line_width) // 2
        draw.text((text_x, text_y), line, font=font, align="center", stroke_width=outline_size, stroke_fill=outline_color)
        text_y += line_height
    return img    

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


prompt = Path('gptprompt.txt').read_text(encoding="utf-8")
output = gpt3_completion(prompt)
paragraphs=output.split('\n')
path="output\\" + prompt[:10].replace(":","_").replace(" ","_") +"_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
os.mkdir(path)
filename = "Gen_" + datetime.now().strftime("%m_%d_%Y%H_%M_%S")+ "_.txt"
with open(path + "\\" + filename, 'w', encoding='utf-8') as outfile:
        outfile.write(prompt + "\n")
        outfile.write(output)
ind=0
engine = pyttsx3.init()
files=[]
for para in paragraphs:
    if para.strip():
        print(para + "\n")
        payload = {
            "prompt": para + ", RAW Photo,  sharp, detailed, 256k film still from a color movie made in 1980, good lighting, good photography, sharp focus, movie still, film grain",
            "negative_prompt": "blurry, frame, topless",
            "steps": 60,
            "sampler_index": "DPM++ SDE Karras"
        }
        r = requests.post(url=f'http://127.0.0.1:7860/sdapi/v1/txt2img', json=payload).json()
        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
            imagepath=path + "\\" + "image_" + str(ind)  + '.png'
            image=add_subtitles(image, para)    
            image.save(imagepath)
            files.append("-i")
            files.append(imagepath)
            
        
        ind=ind+1
        line=para.split(":",maxsplit=1)
        if(len(line)>1):
            voice=line[1]
        else:
            voice=para
        voice_path=path+ "\\audio_" + str(ind) + ".mp3"
        files.append("-i")
        files.append(voice_path)
        engine.save_to_file(voice, voice_path)
        engine.runAndWait()

combinevideos(path, files)            
