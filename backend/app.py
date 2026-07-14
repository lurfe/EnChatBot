from fastapi import FastAPI
from pydantic import BaseModel

from transformers import (
  T5ForConditionalGeneration,
  T5Tokenizer
)

from llama_cpp import Llama

from backend.config import (
  T5_MODEL_PATH,
  LLAMA_MODEL_NAME
)

from backend.services.pipeline import Pipeline
from backend.services.grammar import GrammarService
from backend.services.explanation import ExplanationService
from backend.services.conversation import ConversationService


############################################
# Load model (only once)
############################################


print("Loading T5......")

tokenizer = T5Tokenizer.from_pretrained(
  T5_MODEL_PATH
)

t5 = T5ForConditionalGeneration.from_pretrained(
  T5_MODEL_PATH
)

print("Loading Llama.....")

llama = Llama(
  model_path=LLAMA_MODEL_NAME,
  n_ctx=4096,
  verbose=False
)

############################################
# Create service
############################################

grammar = GrammarService(
  t5,
  tokenizer
)

explanation = ExplanationService(
  llama
)

conversation = ConversationService(
  llama
)

pipeline = Pipeline(
  grammar=grammar,
  explanation=explanation,
  conversation=conversation
)

############################################
# FastAPI
############################################

app = FastAPI(
  title="English tutor API"
)


class ChatRequest(BaseModel):

  message: str


class EditResponse(BaseModel):
    rule: str
    operation: str
    original: str
    corrected: str
    original_start: int
    original_end: int
    corrected_start: int
    corrected_end: int


class ChatResponse(BaseModel):
    response: str
    corrected: str
    changed: bool
    confidence: float
    processing_time: float
    edits: list[EditResponse]

@app.get("/")
def home():

  return {
    "status": "running",
    "service": "English tutor Chatbot"
  }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    result = pipeline.process(
            request.message
    )

    return ChatResponse(**result)