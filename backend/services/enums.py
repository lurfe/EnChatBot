from enum import Enum

class GrammarRule(str, Enum):

    SUBJECT_VERB = "Subject-Verb Agreement"

    VERB_TENSE = "Verb Tense"

    ARTICLE = "Article"

    PREPOSITION = "Preposition"

    PRONOUN = "Pronoun"

    SINGULAR_PLURAL = "Singular / Plural"

    PUNCTUATION = "Punctuation"

    SPELLING = "Spelling"

    WORD_ORDER = "Word Order"

    CAPITALIZATION = "Capitalization"

    WORD_CHOICE = "Word Choice"

    AUXILIARY = "Auxiliary Verb"

    DETERMINER = "Determiner"

    CONJUNCTION = "Conjunction"

    FRAGMENT = "Sentence Fragment"

    RUN_ON = "Run-on Sentence"

    UNKNOWN = "Unknown"

class EditOperation(str, Enum):
  
    INSERT = "insert"

    DELETE = "delete"
    
    REPLACE = "replace"


class Route(str, Enum):

    GRAMMAR = "grammar"

    EXPLAIN = "explain"

    CONVERSATION = "conversation"

    BOTH = "both"

    UNKNOWN = "unknown"

    NONE = "none"