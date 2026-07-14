from __future__ import annotations
from difflib import SequenceMatcher

import time

import torch

from backend.config import (
    DEVICE,
    MAX_LENGTH,
    NUM_BEAMS
)

from backend.logger import logger

from backend.services.schemas import (
    CorrectionResult
)

from backend.services.edits import EditExtractor

from backend.utils.helpers import normalize


class GrammarService:

    def __init__(self, model, tokenizer):

        logger.info("Loading GrammarService...")

        self.model = model
        self.tokenizer = tokenizer

        self.model.to(DEVICE)
        self.model.eval()

        self.extractor = EditExtractor()

        logger.info("GrammarService ready.")

    ####################################################

    @torch.no_grad()
    def _generate(self, sentence: str):

        inputs = self.tokenizer(

            "grammar: " + sentence,

            return_tensors="pt",

            truncation=True,

            max_length=MAX_LENGTH

        ).to(DEVICE)

        outputs = self.model.generate(

            **inputs,

            max_length=MAX_LENGTH,

            num_beams=NUM_BEAMS,

            early_stopping=True,

            length_penalty=0.8,

            repetition_penalty=1.2,

            no_repeat_ngram_size=3,

            return_dict_in_generate=True

        )

        corrected = self.tokenizer.decode(

            outputs.sequences[0],

            skip_special_tokens=True

        )

        return corrected

    ####################################################

    def _confidence(

        self,

        original: str,

        corrected: str

    ) -> float:

        if normalize(original) == normalize(corrected):

            return 1.0

        original_words = len(original.split())

        corrected_words = len(corrected.split())

        ratio = SequenceMatcher(

            None,

            normalize(original),

            normalize(corrected)

        ).ratio()

        return round(ratio,2)


    ####################################################

    def correct(

        self,

        sentence: str

    ) -> CorrectionResult:

        start = time.perf_counter()

        corrected = self._generate(sentence)

        changed = (

            normalize(sentence)

            !=

            normalize(corrected)

        )

        edits = self.extractor.extract(

            sentence,

            corrected

        )

        confidence = self._confidence(

            sentence,

            corrected

        )

        elapsed = round(

            time.perf_counter() - start,

            4

        )

        result = CorrectionResult(

            original=sentence,

            corrected=corrected,

            changed=changed,

            confidence=confidence,

            processing_time=elapsed,

            edits=edits

        )

        logger.info(

            "Original : %s",

            sentence

        )

        logger.info(

            "Corrected: %s",

            corrected

        )

        logger.info(

            "Edits    : %d",

            len(edits)

        )

        logger.info(

            "Time     : %.3fs",

            elapsed
        )

        return result