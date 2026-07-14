from logger import logger

def build_prompt(results):

    prompt = """
You are an English tutor.

For every corrected sentence:

1. Show the corrected sentence.

2. Explain each correction.

3. Give one extra example.

Ignore sentences that already have correct grammar.

"""

    for item in results:

        if not item["changed"]:
            continue

        prompt += f"""

Original:
{item['original']}

Corrected:
{item['corrected']}

Edits:
{item['edits']}

"""

    logger.info("---------- Prompt ----------")
    logger.info(prompt)

    return prompt