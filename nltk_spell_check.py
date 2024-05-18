from transformers import pipeline
import nltk
import os
from textblob import TextBlob

# Use a pipeline as a high-level helper
pipe = pipeline("token-classification", model="nalinaksh/bert-finetuned-ner")

#function to identify words that are in ner category, so these should not be checked for spelling mistakes
def find_ners(text):
  ners = []
  entities = pipe(text)
  for entity in entities:
    ners.append(entity['word'])
  return ners

def spell_check(text):
    # Create a TextBlob object
    blob = TextBlob(text)
    
    # Get a list of misspelled words
    misspelled_words = [word for word in blob.words if word.lower() not in blob.correct()]
    
    return misspelled_words
