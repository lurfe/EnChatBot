from backend.services.schemas import ConversationState, Message
from backend.config import MAX_HISTORY

class MemoryService:

    def __init__(self):

        self.state = ConversationState()

    #########################################

    def add_message(self, role, text):

      self.state.history.append(
          Message(
              role=role,
              content=text
          )
      )

      self.trim()

    #########################################

    def add_user(self, text):

      self.add_message("user", text)

    #########################################

    def add_assistant(self, text):
      
      self.add_message("assistant", text)

    #########################################

    def set_last_correction(self, correction):

        self.state.last_correction = correction

    #########################################

    def get_last_correction(self):

        return self.state.last_correction

    #########################################

    def get_history(self):

        return self.state.history.copy()

    #########################################

    def formatted_history(self):

      text = []

      for message in self.state.history:

          text.append(

              f"{message.role}: {message.content}"

          )

      return "\n".join(text)

    #########################################

    def set_last_intent(self, route):
      self.state.last_intent = route

    #########################################

    def get_last_intent(self):
      return self.state.last_intent

    #########################################

    def clear(self):

        self.state = ConversationState()

    #########################################

    def trim(self):

        if len(self.state.history) > MAX_HISTORY:

            self.state.history = self.state.history[-MAX_HISTORY:]

    #########################################

    def is_follow_up(self):

      return self.state.last_correction is not None