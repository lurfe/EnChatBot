from __future__ import annotations

from backend.services.schemas import Edit
from backend.services.enums import GrammarRule

class GrammarRuleDetector:
    """
    Detect the grammatical rule associated with an edit.

    This is currently heuristic-based but is designed so
    a POS tagger or classifier can replace it later.
    """

    def __init__(self):

        self.rules = [

            self.subject_verb_agreement,

            self.article,

            self.preposition,

            self.plural,

            self.verb_tense,

            self.pronoun,

            self.punctuation,

            self.spelling

        ]

    #####################################################
    # Public
    #####################################################

    def detect(self, edit: Edit):

        for rule in self.rules:

            result = rule(edit)

            if result is not None:

                return result

        return GrammarRule.UNKNOWN

    #####################################################
    # Individual rule detectors
    #####################################################

    def subject_verb_agreement(self, edit):

        mapping = {

            ("has", "have"),

            ("have", "has"),

            ("is", "are"),

            ("are", "is"),

            ("was", "were"),

            ("were", "was"),

            ("does", "do"),

            ("do", "does")

        }

        if (

            edit.original.lower(),

            edit.corrected.lower()

        ) in mapping:

            return GrammarRule.SUBJECT_VERB

    #####################################################

    def article(self, edit):

        articles = {

            "a",

            "an",

            "the"

        }

        if (

            edit.original.lower() in articles

            or

            edit.corrected.lower() in articles

        ):

            return GrammarRule.ARTICLE

    #####################################################

    def preposition(self, edit):

        prepositions = {

            "in",

            "on",

            "at",

            "to",

            "of",

            "for",

            "with",

            "by",

            "from",

            "about",

            "into",

            "through",

            "during",

            "before",

            "after"

        }

        if (

            edit.original.lower() in prepositions

            or

            edit.corrected.lower() in prepositions

        ):

            return GrammarRule.PREPOSITION

    #####################################################

    def plural(self, edit):

        if (

            edit.original.endswith("s")

            !=

            edit.corrected.endswith("s")

        ):

            return GrammarRule.SINGULAR_PLURAL

    #####################################################

    def verb_tense(self, edit):

        IRREGULAR_VERBS = {

            ("go","went"),

            ("went","go"),

            ("eat","ate"),

            ("see","saw"),

            ("buy","bought"),

            ("come","came"),

            ("take","took"),

            ("run","ran"),

            ("make","made")
        }

        endings = (

            "ed",

            "ing"

        )

        if (

            edit.original.endswith(endings)

            or

            edit.corrected.endswith(endings)

        ):
            return GrammarRule.VERB_TENSE

        elif (edit.original.lower(),
              edit.corrected.lower()
          ) in IRREGULAR_VERBS:

            return GrammarRule.VERB_TENSE

    #####################################################

    def pronoun(self, edit):

        pronouns = {

            "i","me","my","mine",

            "you","your",

            "he","him","his",

            "she","her","hers",

            "it",

            "we","our",

            "they","them","their"

        }

        if (

            edit.original.lower() in pronouns

            or

            edit.corrected.lower() in pronouns

        ):

            return GrammarRule.PRONOUN

    #####################################################

    def punctuation(self, edit):

        punctuation = {

            ".",

            ",",

            "!",

            "?",

            ";",

            ":"

        }

        if (

            edit.original in punctuation

            or

            edit.corrected in punctuation

        ):

            return GrammarRule.PUNCTUATION

    #####################################################

    def spelling(self, edit):

        if len(edit.original) == len(edit.corrected):

            differences = sum(

                a != b

                for a, b in zip(

                    edit.original.lower(),

                    edit.corrected.lower()

                )

            )

            if differences <= 2:

                return GrammarRule.SPELLING

        return None