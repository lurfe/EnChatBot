from collections import Counter

from tqdm import tqdm

import numpy as np

from transformers import T5Tokenizer

#####################################################

MAX_LENGTH = 128

tokenizer = T5Tokenizer.from_pretrained("t5-base")

#####################################################

def validate(dataset):

    print("=" * 60)
    print("Dataset Validation")
    print("=" * 60)

    total = len(dataset)

    print(f"Examples: {total:,}")

    #################################################

    empty_src = 0
    empty_tgt = 0

    duplicates = set()

    duplicate_count = 0

    lengths = []

    truncated = 0

    #################################################

    for row in tqdm(dataset):

        src = row["src"].strip()

        tgt = row["tgt"].strip()

        #############################################

        if not src:

            empty_src += 1

        if not tgt:

            empty_tgt += 1

        #############################################

        pair = (src, tgt)

        if pair in duplicates:

            duplicate_count += 1

        else:

            duplicates.add(pair)

        #############################################

        tokens = tokenizer(

            src,

            add_special_tokens=True

        )["input_ids"]

        length = len(tokens)

        lengths.append(length)

        if length > MAX_LENGTH:

            truncated += 1

    #################################################

    print()

    print(f"Empty source : {empty_src:,}")

    print(f"Empty target : {empty_tgt:,}")

    print(f"Duplicates   : {duplicate_count:,}")

    print()

    print(f"Average length : {np.mean(lengths):.2f}")

    print(f"Median length  : {np.median(lengths):.2f}")

    print(f"Maximum length : {max(lengths)}")

    print()

    print(

        f"Need truncation: "

        f"{truncated:,} "

        f"({100*truncated/total:.2f}%)"

    )

    print("=" * 60)