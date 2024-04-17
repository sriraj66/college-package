from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
from .models import *
from smcg.constants import IMAGE_PROMPT
from django.core.files.base import ContentFile
from smcg.models import CONTENTS

class GenerateImage:
    
    def __init__(self,id,key,content,extra) -> None:
        
        self.key = key
        
        self.client = OpenAI(api_key=self.key)

        self.prompt = IMAGE_PROMPT.format(content,extra)
        self.db = CONTENTS.objects.get(id=id)
    
    
    def download_image(self,url):
    
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                print(f"Image downloaded successfully.")
                return image
            else:
                print("Failed to download image: Status code", response.status_code)
        except Exception as e:
            print("An error occurred:", str(e))
            return False

    def combine_images(self, header_path):
        try:
            print("Combining images..")
            header_img = self.download_image(header_path)
            body_img = self.generate_image()

            header_height = 300
            header_width = int(header_img.width * (header_height / header_img.height))
            header_img = header_img.resize((header_width, header_height))

            body_width = header_img.width
            body_height = body_img.height * body_width // body_img.width
            body_img = body_img.resize((body_width, body_height))

            combined_height = header_height + body_height
            combined_img = Image.new("RGB", (header_width, combined_height))

            combined_img.paste(header_img, (0, 0))
            combined_img.paste(body_img, (0, header_height))

            image_stream = BytesIO()
            combined_img.save(image_stream, format="JPEG")
            image_stream.seek(0)

            django_file = ContentFile(image_stream.getvalue())

            self.db.output_image.save(f"{self.db.id}_.jpg", django_file)

            print(f"Images combined successfully.")
            return True
                
        except Exception as e:
            print("An error occurred while combining images:", str(e))
            return False
    
    def generate_image(self):
        
        response = self.client.images.generate(
            model="dall-e-3",
            prompt= self.prompt ,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        print(image_url)
        return self.download_image(image_url)