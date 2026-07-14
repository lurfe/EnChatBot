import re

def normalize(text):

  text = text.lower()

  text = re.sub(r"\s+", " ", text)

  return text.strip()