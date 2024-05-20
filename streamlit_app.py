import base64
import requests
import os
import re
import streamlit as st
from PIL import Image
from spell_checker import spell_check
from authenticate import *

#Authenticate user
if not check_password():
    st.stop()

st.title("Handwriting Recognition System with Spelling Mistakes Detection")
st.write("Upload an image of hand-written text")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
      return base64.b64encode(image_file.read()).decode('utf-8')

def image_to_text(image_path, prompt):  
  # Getting the base64 string
  base64_image = encode_image(image_path)

  #OpenAI api key
  api_key = os.environ['OPENAI_API_KEY']

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }

  payload = {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 512
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  json_resp = response.json()
  text = json_resp['choices'][0]['message']['content']
  return text

prompt=f"""
  The images are of children's hand written assignments. \
  You are a hand writting recognition (HWR) expert and your job is to find \
  out what is written in the images to help with grading the assignments. \
  If the image appears to be rotated, deal with appropriately. \
  Handle newlines in recongnized text as and when they appear in images. \
  Recognize the text verbatim, do not auto corect the spelling mistakes. \
  Do not add anything extra text of your own in the output, just the recognized text.
  """

#upload image 
uploaded_file = st.sidebar.file_uploader("Upload an image", type=['png', 'jpg'])

# If user attempts to upload a file.
if uploaded_file is not None:
    #display image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")
    #get filepath
    file_path = os.path.join(os.getcwd(), uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    #get text
    with st.spinner('Recognizing text ...'):
        text = image_to_text(file_path, prompt)
        st.markdown(text)
        spelling_mistakes = spell_check(text,50,4)
        st.write(spelling_mistakes)
