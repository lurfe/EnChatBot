from backend.logger import logger


class ExplanationService:

    def __init__(self, llama):

        self.llama = llama

    ##################################################

    def explain(self, correction):

        if not correction.changed:

            return (
                "Your sentence is already grammatically correct."
            )

        prompt = self.build_prompt(correction)

        logger.info("Generating explanation...")
        logger.info(prompt)

        output = self.llama(

            prompt,

            max_tokens=256,

            temperature=0.4,

            stop=["User:", "Assistant:"]

        )

        return output["choices"][0]["text"].strip()

    ##################################################

    def build_prompt(self, correction):

        edits_text = []

        for i, edit in enumerate(correction.edits, start=1):

            edits_text.append(
                f"""
Change {i}

Operation: {edit.operation.value}

Grammar Rule: {edit.rule.value}

Original: "{edit.original}"

Corrected: "{edit.corrected}"
"""
            )

        edits_text = "\n".join(edits_text)

        prompt = f"""
You are an English grammar teacher.

Your task is to explain ONLY the corrections listed below.

Rules:

- Explain only the listed corrections.
- Do not mention grammar that was not corrected.
- Do not rewrite the sentence.
- Use simple English suitable for English learners.
- When possible, include the general grammar rule without using overly technical language.
- Explain each correction in 1-2 sentences.
- Total response must be under 100 words.

Original sentence:
{correction.original}

Corrected sentence:
{correction.corrected}

Corrections:
{edits_text}

Explain each change.
"""

        return prompt