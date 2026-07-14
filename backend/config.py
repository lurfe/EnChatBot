from pathlib import Path
import torch

# ==========================================================
# Project Directories
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR / "models"
LOG_DIR = BASE_DIR / "logs"
TEMPLATE_DIR = BASE_DIR / "templates"

# Create required directories automatically
MODEL_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# Model Configuration
# ==========================================================

# Fine-tuned T5 grammar correction model
T5_MODEL_PATH = MODEL_DIR / "t5-gec"

# Llama model (Hugging Face name)
LLAMA_MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"

# ==========================================================
# Device Configuration
# ==========================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# ==========================================================
# Text Generation
# ==========================================================

MAX_LENGTH = 128
NUM_BEAMS = 5
NO_REPEAT_NGRAM_SIZE = 3

# ==========================================================
# Conversation Memory
# ==========================================================

MAX_HISTORY = 10

# ==========================================================
# Logging
# ==========================================================

LOG_FILE = LOG_DIR / "chatbot.log"
LOG_LEVEL = "INFO"