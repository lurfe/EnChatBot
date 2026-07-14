from difflib import SequenceMatcher

from backend.services.schemas import Edit
from backend.services.enums import EditOperation
from backend.services.grammar_rules import GrammarRuleDetector


class EditExtractor:

    def __init__(self):

        self.detector = GrammarRuleDetector()

    ##################################################

    def extract(
        self,
        original: str,
        corrected: str
    ):

        edits = []

        original_words = original.split()
        corrected_words = corrected.split()

        matcher = SequenceMatcher(
            None,
            original_words,
            corrected_words
        )

        operation_map = {

            "replace": EditOperation.REPLACE,

            "insert": EditOperation.INSERT,

            "delete": EditOperation.DELETE

        }

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():

            if tag == "equal":
                continue

            original_text = " ".join(original_words[i1:i2])
            corrected_text = " ".join(corrected_words[j1:j2])

            if not original_text and not corrected_text:
                continue

            edit = Edit(

                operation=operation_map[tag],

                original=original_text,

                corrected=corrected_text,

                original_start=i1,

                original_end=i2,

                corrected_start=j1,

                corrected_end=j2

            )

            edit.rule = self.detector.detect(edit)

            edits.append(edit)

        return edits