from textblob import TextBlob
import spacy
import os
import subprocess

# Define a function to download the English model
def download_model():
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])

# Check if the model is already installed
if "en_core_web_sm" not in spacy.util.get_installed_models():
    # If not installed, download the model
    download_model()

# Load the English model
nlp = spacy.load("en_core_web_sm")

#function to identify words that are in ner category, so these should not be checked for spelling mistakes
def find_ners(text):
  ners = []
  doc = nlp(text)
  # Extract named entities
  for ent in doc.ents:
    ners.append(ent.text)
  return ners

def spell_check(text):
    # Create a TextBlob object
    blob = TextBlob(text)
    ignore_words = find_ners(text)
    # Get a list of misspelled words
    candidate_words = [word for word in blob.words if word not in ignore_words]
    misspelled_words = [word for word in candidate_words if word.lower() not in blob.correct()]
    
    return misspelled_words
