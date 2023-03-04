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
import GenerateVideo

text=Path('storyprompt.txt').read_text(encoding="utf-8")
config = GenerateVideo.LoadConfig(text)
GenerateVideo.Generate(text,config)

      
