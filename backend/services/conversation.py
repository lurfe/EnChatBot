from backend.logger import logger


class ConversationService:

    def __init__(self, llama):

        self.llama = llama

    ####################################################

    def reply(
        self,
        user_message,
        memory
    ):

        prompt = self.build_prompt(
            user_message,
            memory
        )

        logger.info("Conversation prompt created.")

        output = self.llama(
            prompt,
            max_tokens=256,
            temperature=0.4,
            stop=["User:", "Assistant:"]
        )

        return output["choices"][0]["text"].strip()

    ####################################################

    def build_prompt(
        self,
        user_message,
        memory
    ):

        history = memory.formatted_history()

        prompt = f"""
You are an AI English tutor.

Your goals are:

- Help users improve their English.
- Answer English grammar questions.
- Answer vocabulary questions.
- Have natural conversations in English.
- Encourage the user to keep practicing.
- Be friendly and concise.
- If the user's English is imperfect, answer naturally without correcting it here (grammar correction is handled separately).

Conversation history:

{history}

User:

{user_message}

Assistant:
"""

        return prompt

    ####################################################

    def reply_about_correction(
        self,
        user_message,
        memory
    ):

        last = memory.get_last_correction()

        if last is None:

            return (
                "There is no previous correction to explain."
            )

        prompt = f"""
You are an English teacher.

The student is asking about a previous grammar correction.

Original sentence:
{last.original}

Corrected sentence:
{last.corrected}

Student's question:
{user_message}

Answer clearly in simple English.
"""

        output = self.llama(
            prompt,
            max_tokens=256,
            temperature=0.4,
            stop=["User:", "Assistant:"]
        )

        return output["choices"][0]["text"].strip()