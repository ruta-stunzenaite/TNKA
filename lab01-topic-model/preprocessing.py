import re

FILLER_PHRASES = [
    "as markets react", "dėl rinkos reakcijos", "analitikų teigimu",
    "analysts say", "after report", "po pranešimo",
]
FILLER_RE = re.compile("|".join(re.escape(p) for p in FILLER_PHRASES))


def remove_fillers(text):
    return FILLER_RE.sub(" ", text.lower())