from transformers import pipeline
import nltk
from nltk.corpus import words
import os

# Use a pipeline as a high-level helper
pipe = pipeline("token-classification", model="nalinaksh/bert-finetuned-ner")

# Download NLTK data if not already downloaded
nltk.download('words')
nltk.download('punkt')
# Load the English words corpus
english_words = set(words.words())

#function to identify words that are in ner category, so these should not be checked for spelling mistakes
def find_ners(text):
  ners = []
  entities = pipe(text)
  for entity in entities:
    ners.append(entity['word'])
  return ners

def spell_check(text):
    # Tokenize the input text
    tokens = nltk.word_tokenize(text.lower())
    
    # Filter out non-alphabetic tokens
    tokens = [word for word in tokens if word.isalpha()]
    # ner words to be ignored
    ners = find_ners(text)
    # Spell check each token
    misspelled_words = []
    for token in tokens:
      if token not in ners:
        if token not in english_words:
          misspelled_words.append(token)
    
    return misspelled_words  
