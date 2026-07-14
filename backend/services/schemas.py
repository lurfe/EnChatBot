from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from backend.services.enums import (
    GrammarRule,
    EditOperation,
    Route
)


# ----------------------------------------
# Grammar Edit
# ----------------------------------------

@dataclass
class Edit:

    operation: EditOperation

    rule: GrammarRule = GrammarRule.UNKNOWN

    original: str = ""

    corrected: str = ""

    original_start: int = 0

    original_end: int = 0

    corrected_start: int = 0

    corrected_end: int = 0


# ----------------------------------------
# Grammar Result
# ----------------------------------------

@dataclass
class CorrectionResult:

    original: str

    corrected: str

    changed: bool

    confidence: float = 1.0

    processing_time: float = 0.0

    edits: List["Edit"] = field(default_factory=list)


# ----------------------------------------
# Chat Memory
# ----------------------------------------

@dataclass
class Message:

    role: str

    content: str

    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ConversationState:

    history: List[Message] = field(default_factory=list)

    last_correction: CorrectionResult | None = None

    last_intent: Route = Route.UNKNOWN

    last_response: str = ""


# ----------------------------------------
# Router Output
# ----------------------------------------

@dataclass
class Task:

    route: Route

    grammar: bool = False

    explanation: bool = False

    conversation: bool = False

    reason: str = ""