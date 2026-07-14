from backend.services.grammar import GrammarService
from backend.services.memory import MemoryService
from backend.services.router import Router
from backend.logger import logger

class Pipeline:

    def __init__(

        self,

        grammar,

        explanation,

        conversation,

        memory

    ):

      self.memory = memory

      self.grammar = grammar

      self.explanation = explanation

      self.conversation = conversation

      self.router = Router(self.memory)

    ########################################################

    def process(self, user_message):

        # log
        logger.info("=" * 60)
        logger.info(f"User: {user_message}")

        # Store user message
        self.memory.add_user(user_message)

        # Run grammar correction
        correction = self.grammar.correct(user_message)
      
        # Save latest correction
        self.memory.set_last_correction(correction)

        # log correction

        logger.info(f"Corrected: {correction.corrected}")
        logger.info(f"Changed: {correction.changed}")
        logger.info(f"Confidence: {correction.confidence}")

        # Decide what to do
        task = self.router.route(
            user_message,
            correction
        )

        # log routing

        logger.info(f"Route: {task.route.value}")
        logger.info(f"Reason: {task.reason}")

        # Execute task
        response = self.dispatch(
            task,
            correction,
            user_message
        )

        # log dispatch
        logger.info(f"Assistant: {response}")

        # Store assistant response
        self.memory.add_assistant(response)

        return {
            "response": response,
            "corrected": correction.corrected,
            "changed": correction.changed,
            "confidence": correction.confidence,
            "processing_time": correction.processing_time,
            "edits": [
                {
                    "rule": edit.rule.value,
                    "operation": edit.operation.value,
                    "original": edit.original,
                    "corrected": edit.corrected,
                    "original_start": edit.original_start,
                    "original_end": edit.original_end,
                    "corrected_start": edit.corrected_start,
                    "corrected_end": edit.corrected_end,
                }
                for edit in correction.edits
            ]
        }

    ########################################################

    def dispatch(
        self,
        task,
        correction,
        user_message
    ):

        if task.grammar and task.explanation:

            return {
                "corrected": self.handle_grammar(correction),
                "explanation": self.handle_explanation(correction)
            }

        if task.grammar:
            return self.handle_grammar(correction)

        if task.explanation:
            return self.handle_explanation(correction)

        if task.conversation:
            return self.handle_conversation(user_message)

        return self.handle_unknown()

    ########################################################

    def handle_grammar(self, correction):

        return correction.corrected

    ########################################################

    def handle_explanation(self, correction):

        return self.explanation.explain(correction)

    ########################################################

    def handle_conversation(self, user_message):

        return self.conversation.reply(
          user_message,
          self.memory
        )

    ########################################################

    def handle_unknown(self):

        return (
            "I'm not sure how to handle that request."
        )

    ########################################################

    def debug(self, user_message):

      correction = self.grammar.correct(user_message)

      task = self.router.route(
          user_message,
          correction
      )

      print("\n========== DEBUG ==========")

      print("Input:")
      print(user_message)

      print("\nCorrection:")
      print(correction)

      print("\nRoute:")
      print(task)

      print("\nEdits:")

      for edit in correction.edits:
          print(edit)

      print("===========================\n")