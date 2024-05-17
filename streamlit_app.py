import base64
import requests
import os
import re
import streamlit as st
from PIL import Image

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
      return base64.b64encode(image_file.read()).decode('utf-8')

def image_to_text(image_path):  
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
            "text": "The images are of children's hand written assignments. \
            You are a hand writting recognition (HWR) expert and your job is to find \
            out what is written in the images to help with grading the assignments. \
            If the image appears to be rotated, deal with appropriately. \
            Handle newlines in recongnized text as and when they appear in images. \
            Do not auto corect the spelling mistakes. \
            Also specify all the words that have spelling mistakes. \
            Answer should be in this format: \
            Handwritten text: \
            Spelling Errors: [list of words with spelling mistakes]"
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
    "max_tokens": 300
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  json_resp = response.json()
  text = json_resp['choices'][0]['message']['content']

  return text

def extract_spelling_errors(text):
    # Regular expression pattern to match the list of words inside square brackets
    pattern = r'\[([^\[\]]*)\]'
    
    # Find the list of words inside square brackets
    matches = re.findall(pattern, text)
    spelling_errors = []
    # Check if there are matches
    if matches:
        # Get the first match (assuming there's only one)
        words_list = matches[0]
        # Check if the list is not empty
        if words_list:
            # Split the list of words by comma and strip whitespace
            spelling_errors = [word.strip() for word in words_list.split(',')]
            # print("Spelling Errors:", spelling_errors)
    #     else:
    #         print("No spelling errors found.")
    # else:
    #     print("No spelling errors found.")
    return spelling_errors

# Function to highlight specific words in a paragraph
def highlight_text(text, words_to_highlight):
    for word in words_to_highlight:
        text = text.replace(word, f"<span style='background-color: yellow'>{word}</span>")
    return text

#upload image 
uploaded_file = st.sidebar.file_uploader("Upload an image", type=['png', 'jpg'])
file_path = os.path.join(os.getcwd(), uploaded_file.name)
with open(file_path, "wb") as f:
    f.write(uploaded_file.getbuffer())

# st.write(file_path)

# If user attempts to upload a file.
if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.image(image, caption="Uploaded Image")
  with st.spinner('Recognizing text ...'):
    text = image_to_text(file_path)
    spelling_errors = extract_spelling_errors(text)
    # st.write(text)
    # Highlighting the words in the paragraph
    highlighted_paragraph = highlight_text(text, spelling_errors)
    
    # Render the highlighted paragraph as HTML
    st.markdown(highlighted_paragraph, unsafe_allow_html=True)

    
