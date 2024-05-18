from transformers import pipeline
import pyspellchecker
import re

# Use a pipeline as a high-level helper
pipe = pipeline("token-classification", model="nalinaksh/bert-finetuned-ner")
# Create a new spell checker
spellchecker = pyspellchecker.SpellChecker()

#function to identify words that are in ner category, so these should not be checked for spelling mistakes
def find_ners(text):
  ners = []
  entities = pipe(text)
  for entity in entities:
    ners.append(entity['word'])
  return ners

def find_spelling_errors(text):
  spelling_errors = []
  ignore_words = find_ners(text)
  words = re.split(r'W+', text)
  for word in words:
    if word not in ignore_words:
      if not spellchecker.spell(word):
        spelling_errors.append(word)
  return spelling_errors
  
  
