from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from sklearn.decomposition import LatentDirichletAllocation

BASE = Path(__file__).parent
OUT_DIR = BASE / "outputs"
MODEL_DIR = BASE / "models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_SEED = 42
MAX_ITER = 15
MAX_FEATURES = 3000
MIN_DF = 2
TOKEN_PATTERN = r"(?u)\b[^\W\d_]{2,}\b"
K_VALUES = [3, 4]

LT_STOP_WORDS = {
    "ir", "su", "dėl", "po", "kad", "kaip", "kurias", "kurie", "kuri", "kuris",
    "iš", "ant", "prie", "per", "apie", "nuo", "iki", "be", "bet", "ar", "tai",
    "yra", "buvo", "jo", "jos", "jų", "jie", "tas", "ta", "šis", "ši", "šie",
    "tik", "dar", "jau", "taip", "ne", "nes", "arba", "kas", "net", "labai",
}
BASE_STOP_WORDS = sorted(ENGLISH_STOP_WORDS | LT_STOP_WORDS)


def load_collection():
    docs = pd.read_csv(OUT_DIR / "sample_collection.csv")
    first20 = pd.read_csv(OUT_DIR / "initial_20_headlines.csv")
    return docs, first20


def build_vectorizer(stop_words, preprocessor=None):
    return CountVectorizer(
        lowercase=True,
        preprocessor=preprocessor,
        token_pattern=TOKEN_PATTERN,
        stop_words=list(stop_words),
        min_df=MIN_DF,
        max_features=MAX_FEATURES,
    )

def run_lda(name, k, docs, first20, stop_words=BASE_STOP_WORDS, preprocessor = None):
    print(f"\n{'=' * 60}\nRun {name}: {k} topics\n{'=' * 60}")

    vec = build_vectorizer(stop_words, preprocessor)
    X = vec.fit_transform(docs["text"])
    vocab = vec.get_feature_names_out()
    n_terms = np.asarray(X.sum(axis=1)).ravel()
    nonempty = n_terms > 0
    print(f"Vocabulary size: {len(vocab)}")
    print(f"Documents with no retained terms: {(~nonempty).sum()} of {len(docs)}")

    lda = LatentDirichletAllocation(
        n_components=k, max_iter=MAX_ITER,
        learning_method="batch", random_state=MODEL_SEED,
    )
    lda.fit(X[nonempty])

    weights = np.full((len(docs), k), np.nan)
    weights[nonempty] = lda.transform(X[nonempty])

    doc_topics = docs.copy()
    doc_topics["n_terms"] = n_terms
    doc_topics["dominant_topic"] = pd.NA
    doc_topics.loc[nonempty, "dominant_topic"] = weights[nonempty].argmax(axis=1)
    for t in range(k):
        doc_topics[f"topic_{t}"] = weights[:, t].round(3)

    topic_rows = []
    for t, comp in enumerate(lda.components_):
        top_words = [vocab[i] for i in comp.argsort()[::-1][:10]]
        size = (doc_topics["dominant_topic"] == t).sum()
        reps = doc_topics[f"topic_{t}"].dropna().nlargest(3).index
        print(f"\nTopic {t} ({size} headlines as dominant topic)")
        print("  Top words:", ", ".join(top_words))
        for i in reps:
            print(f"  [{doc_topics.at[i, f'topic_{t}']:.2f}] {doc_topics.at[i, 'text']}")
        topic_rows.append({
            "topic": t, "size": size, "top_words": ", ".join(top_words),
            "rep_1": doc_topics.at[reps[0], "text"],
            "rep_2": doc_topics.at[reps[1], "text"] if len(reps) > 1 else "",
        })

    cols = ["orig_row", "n_terms", "dominant_topic"] + [f"topic_{t}" for t in range(k)]
    check20 = first20.merge(doc_topics[cols], on="orig_row", how="left")
    print(f"\nYour 20 headlines (run {name}):")
    print(check20.drop(columns=["orig_row"]).to_string(index=False))
 
    pd.DataFrame(topic_rows).to_csv(OUT_DIR / f"run_{name}_topics.csv", index=False, encoding="utf-8-sig")
    doc_topics.to_csv(OUT_DIR / f"run_{name}_doc_topics.csv", index=False, encoding="utf-8-sig")
    check20.to_csv(OUT_DIR / f"run_{name}_initial20.csv", index=False, encoding="utf-8-sig")
    joblib.dump({"vectorizer": vec, "lda": lda}, MODEL_DIR / f"run_{name}.joblib")
    return vec, lda, doc_topics


if __name__ == "__main__":
    docs, first20 = load_collection()
    for name, k in zip(["A", "B"], K_VALUES):
        run_lda(name, k, docs, first20)