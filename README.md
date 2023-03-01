# AI Video StoryGen
Uses ChatGPT, TTS, and Stable Diffusion (AUTOMATIC1111) to automatically generate videos
## Features
- Can either parse existing text or generate new text using ChatGPT API
- Uses the AUTOMATIC1111 API to generate images based on the text of the story
- Adds subtitles to images
- Currently supports pyttsx3 or ElevenLabs AI to generate audio
- Combines generated audio and images using FFMPEG to create a video 
## Installation and Running
Installation process is still a bit messy. 
- Make sure  Automatic1111 API is enabled and that its running
- copy config.example.json, rename it to config.json and add your keys
- Run GenerateVideoFromGPT.py if you want to generate using a GPT prompt in gptprompt.txt
- Run GenerateVideoFromText.py if you want to generate using existing text

This is obviously still pretty WIP, but I have a bunch more features I plan to add.
