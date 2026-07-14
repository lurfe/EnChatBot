from backend.services.schemas import Task
from backend.services.enums import Route
from backend.logger import logger


class Router:

    def __init__(self, memory):

        self.memory = memory

        self.followups = {

            "why",
            "why?",
            "how",
            "how?",
            "explain",
            "explain.",
            "can you explain"

        }

        self.greetings = {

            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"

        }

    ##################################################

    def normalize(self, text):

        return " ".join(
            text.lower().split()
        )

    ##################################################

    def needs_grammar(self, correction):

        if correction is None:
            return False

        return correction.changed

    ##################################################

    def is_follow_up(self, text):

        return (

            text in self.followups

            and

            self.memory.is_follow_up()

        )

    ##################################################

    def is_greeting(self, text):

        return text in self.greetings

    ##################################################

    def route(
        self,
        user_message,
        correction
    ):

        logger.info("Router evaluating request...")

        text = self.normalize(user_message)

        ##################################################

        if self.needs_grammar(correction):

            task = Task(
                route=Route.GRAMMAR,
                grammar=True,
                explanation=True,
                conversation=False,
                reason="Grammar correction detected."
            )

            self.memory.set_last_intent(task.route)

            logger.info("Selected route: GRAMMAR")

            return task

        ##################################################

        if self.is_follow_up(text):

            task = Task(
                route=Route.EXPLAIN,
                explanation=True,
                reason="Follow-up question."
            )

            self.memory.set_last_intent(task.route)

            logger.info("Selected route: EXPLAIN")

            return task

        ##################################################

        if self.is_greeting(text):

            task = Task(
                route=Route.CONVERSATION,
                conversation=True,
                reason="Greeting."
            )

            self.memory.set_last_intent(task.route)

            logger.info("Selected route: CONVERSATION")

            return task

        ##################################################

        task = Task(
            route=Route.CONVERSATION,
            conversation=True,
            reason="Default conversation."
        )

        self.memory.set_last_intent(task.route)

        logger.info("Selected route: CONVERSATION")

        return task