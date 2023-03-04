import requests
from PIL import Image
import io
import base64


upscale=False
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
