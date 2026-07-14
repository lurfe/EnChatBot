!pip install -q logger

import nltk
from logger import logger

nltk.download("punkt", quiet=True)

def split_sentence(text):
  return nltk.sent_tokenize(text)