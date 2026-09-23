import sys
from pathlib import Path
import numpy as np
import joblib
import preprocessing

BASE = Path(__file__).parent
MODEL_PATH = BASE / "models" / "run_C.joblib"

TOPIC_NAMES = {
    0: "mixed: tech/sports",
    1: "mixed: clickbait/tech",
    2: "mixed: mostly finance/tech",
    3: "mixed: clickbait/ML",
}

def analyse(headlines, vec, lda):
    X = vec.transform(headlines)
    vocab = vec.get_feature_names_out()
    for i, text in enumerate(headlines):
        row = X[i]
        print(f"\nHeadline: {text}")
        if row.sum() == 0:
            print("  No vocabulary terms retained -> insufficient evidence, no topic assigned.")
            continue
        terms = [f"{vocab[j]}({c})" for j, c in zip(row.indices, row.data)]
        print("  Retained terms:", ", ".join(terms))
        weights = lda.transform(row)[0]
        for t in np.argsort(weights)[::-1]:
            print(f"  Topic {t} – {TOPIC_NAMES.get(t, '?')}: {weights[t]:.3f}")


if __name__ == "__main__":
    model = joblib.load(MODEL_PATH)
    vec, lda = model["vectorizer"], model["lda"]

    headlines = sys.argv[1:]
    if not headlines:
        print("Type headlines, one per line. Empty line to finish.")
        while (line := input("> ").strip()):
            headlines.append(line)
    analyse(headlines, vec, lda)