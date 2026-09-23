import re
from stage_2 import load_collection, run_lda

PROVISIONAL_K = 4

FILLER_PHRASES = [
    "as markets react", "dėl rinkos reakcijos", "analitikų teigimu",
    "analysts say", "after report", "po pranešimo",
]
FILLER_RE = re.compile("|".join(re.escape(p) for p in FILLER_PHRASES))


def remove_fillers(text):
    return FILLER_RE.sub(" ", text.lower())


if __name__ == "__main__":
    docs, first20 = load_collection()
    run_lda("C", PROVISIONAL_K, docs, first20, preprocessor=remove_fillers)