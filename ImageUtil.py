import requests
from PIL import Image, ImageFont, ImageDraw
import io
import base64
import textwrap

upscale=False
def add_subtitles(image, text, fontsize):
    # Create an ImageDraw object and set the font and size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial.ttf', size=fontsize)

    text_width, text_height = font.getsize(text)
    max_width = (image.width * 2) - 10
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
    return image

def generate_image(para, ind, path, config):
        payload = {
            "prompt": para + config["prompt"],
            "negative_prompt": config["negative_prompt"],
            "steps": config["steps"],
            "width": config["image_width"],
            "height": config["image_height"],
            "sampler_index": config["sampler_index"]
        }
        r = requests.post(url=f'http://127.0.0.1:7860/sdapi/v1/txt2img', json=payload).json()
        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
            imagepath=path + "\\" + "image_" + str(ind)  + '.png'
            if config["upscale_enabled"]:
                image=upscale_image(image,config)
            image=add_subtitles(image, para, 40)    
            image.save(imagepath)
            return imagepath

def upscale_image(image, config):        
    with io.BytesIO() as buffer:
        image.save(buffer, format='PNG')
        payload = {
            "upscaling_resize": config["upscaling_resize"],
            "upscaler_1": config["upscaler_1"],
            "image": base64.b64encode(buffer.getvalue()).decode('utf-8')
        }
        r = requests.post(url=f'http://127.0.0.1:7860/sdapi/v1/extra-single-image', json=payload).json()
        return Image.open(io.BytesIO(base64.b64decode(r["image"].split(",",1)[0])))
