# AI Video StoryGen
Uses GPT, TTS, and Stable Diffusion (AUTOMATIC1111) to automatically generate videos
## Features
- Can either parse existing text or generate new text using GPT API
- Uses the AUTOMATIC1111 API to generate images based on the text of the story
- Adds subtitles to images
- Currently supports pyttsx3 or ElevenLabs AI to generate audio
- Will automatically detect speaker (if text is in transcript format)
- Combines generated audio and images using FFMPEG to create a video 
## Installation and Running
- Make sure  Automatic1111 API is enabled and that its running
- copy config.example.json, rename it to config.json and add your keys
- Run GenerateVideoFromGPT.py if you want to generate using a GPT prompt in gptprompt.txt
- Run GenerateVideoFromText.py if you want to generate using existing text

Here is an example output:
[![example](https://img.youtube.com/vi/lm_peWz93a4/maxresdefault.jpg)](https://www.youtube.com/watch?v=lm_peWz93a4)

This is still in development. I'm still not sure how I want to implement the UI.
