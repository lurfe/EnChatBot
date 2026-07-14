import nltk
from logger import logger

nltk.download("punkt", quiet=True)

def split_sentence(text):

    logger.info("============== Sentence splitter ==============")

    sentences = nltk.sent_tokenize(text)

    for i, sentence in enumerate(sentences):
      logger.info(f"{i+1}. {sentence}")

    return sentences