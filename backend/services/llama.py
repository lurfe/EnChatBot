from transformers import pipeline

from config import *

from logger import logger

chat = pipeline(
    "text-generation",
    model=LLAMA_MODEL
)


def explain(prompt):

    logger.info("---------- Sending to Llama ----------")

    response = chat(
        prompt,
        max_new_tokens=200,
        do_sample=False
    )[0]["generated_text"]

    logger.info("---------- Llama Response ----------")
    logger.info(response)

    return response