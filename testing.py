import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

user_prompt = "Ninja Cat in kimono"
response=openai.Image.create(
    prompt=user_prompt,
    n=1,
    size="1024x1024"
)

image_url=response['data'][0]['url']  #0 means 1st image
print(image_url)
