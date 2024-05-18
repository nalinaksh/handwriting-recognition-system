from textblob import TextBlob
import spacy
import os

# Load the English NER model
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
