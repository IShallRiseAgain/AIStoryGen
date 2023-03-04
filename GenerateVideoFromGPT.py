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
import VideoUtil
import GenerateVideo

prompt = Path('gptprompt.txt').read_text(encoding="utf-8")
config = GenerateVideo.LoadConfig(prompt)
if config["paragraphs"]:
    prompt=config["paragraphs"][0]
else:
    prompt=""
if "text_prompt_prefix" in config.keys():
    prompt=config["text_prompt_prefix"] + prompt
if "text_prompt_suffix" in config.keys():
    prompt=prompt + config["text_prompt_suffix"]
print("generating text with prompt: " + prompt)
text = TextGenUtil.generateText(prompt, config)
config["paragraphs"]=text.split('\n')
config["text_prompt"]=prompt
GenerateVideo.Generate(text,config)
    
