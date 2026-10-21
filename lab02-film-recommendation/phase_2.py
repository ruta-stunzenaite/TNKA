import sys

import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from phase_1 import SEED, load_and_clean, pick_queries, split_list

K = 5
GENERIC_THRESHOLD = 0.20
STOP_WORDS = sorted(ENGLISH_STOP_WORDS | {"film", "films"})
TFIDF_PARAMS = dict(
    lowercase=True,
    token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b",
    stop_words=STOP_WORDS,
    ngram_range=(1, 1),
    min_df=2,
    max_features=None,
    sublinear_tf=False,
    norm="l2",
)


def generic_genres(df, threshold=GENERIC_THRESHOLD):
    counts = df["genres"].apply(split_list).explode().value_counts()
    share = counts / len(df)
    return share[share > threshold]


def build_text(df, drop_genres=frozenset()):
    def row_text(row):
        genres = [g for g in split_list(row["genres"]) if g not in drop_genres]
        subjects = split_list(row["subjects"])
        return " ; ".join(genres + subjects)
    return df.apply(row_text, axis=1)


class Recommender:
    def __init__(self, df, name, drop_genres=frozenset()):
        self.df = df
        self.name = name
        self.drop_genres = frozenset(drop_genres)
        self.text = build_text(df, self.drop_genres)
        self.vectorizer = TfidfVectorizer(**TFIDF_PARAMS)
        self.X = self.vectorizer.fit_transform(self.text)
        self.empty_text = int((self.text.str.strip() == "").sum())
        self.empty_vector = int((self.X.getnnz(axis=1) == 0).sum())
        self._index = {t.casefold(): i for i, t in enumerate(df["title"])}

    def find(self, title):
        return self._index.get(" ".join(str(title).split()).casefold())

    def _rank(self, qvec, exclude=None, k=K):
        if qvec.nnz == 0:
            return None
        sims = cosine_similarity(qvec, self.X).ravel()
        if exclude is not None:
            sims[exclude] = -1.0
        order = np.lexsort((self.df["movie_id"].to_numpy(), -self.df["sitelinks"].to_numpy(), -sims))
        order = [i for i in order if sims[i] > 0][:k]
        out = self.df.iloc[order][["title", "year", "director", "genres", "subjects", "sitelinks"]].copy()
        out.insert(1, "similarity", np.round(sims[order], 3))
        return out.reset_index(drop=True)

    def recommend(self, title, k=K):
        idx = self.find(title)
        if idx is None:
            raise KeyError(f"Pavadinimo '{title}' rinkinyje nėra")
        return self._rank(self.X[idx], exclude=idx, k=k)

    def recommend_text(self, text, k=K):
        cleaned = " ; ".join(g for g in split_list(text) if g not in self.drop_genres)
        return self._rank(self.vectorizer.transform([cleaned]), k=k)


def popularity_baseline(df, title=None, k=K):
    top = df.sort_values(["sitelinks", "movie_id"], ascending=[False, True])
    if title is not None:
        top = top[top["title"].str.casefold() != str(title).casefold()]
    out = top.head(k)[["title", "year", "director", "genres", "subjects", "sitelinks"]].copy()
    out.insert(1, "similarity", np.nan)
    return out.reset_index(drop=True)


def build_models(df):
    generic = generic_genres(df)
    model_b = Recommender(df, "B · pradinis TF-IDF")
    model_c = Recommender(df, "C · be bendrinių žanrų", drop_genres=set(generic.index))
    return model_b, model_c, generic


_DEFAULT = {}


def recommend(title, k=K, model="B"):
    if not _DEFAULT:
        df = load_and_clean(verbose=False)
        b, c, _ = build_models(df)
        _DEFAULT.update(B=b, C=c)
    return _DEFAULT[model].recommend(title, k)


def short(s, n=60):
    s = str(s)
    return s if len(s) <= n else s[: n - 1] + "…"


def print_table(title, res):
    print(f"  {title}")
    if res is None or len(res) == 0:
        print("    (tuščias tekstinis laukas — įrodymų nepakanka)")
        return
    for i, r in res.iterrows():
        sim = "  —  " if pd.isna(r["similarity"]) else f"{r['similarity']:.3f}"
        print(f"    {i + 1}. {sim}  {short(r['title'], 42):<42} ({r['year']})  {short(r['director'] or '—', 22)}")


def main():
    df = load_and_clean()
    model_b, model_c, generic = build_models(df)

    print(f"\nVersijos: Python {sys.version.split()[0]} | pandas {pd.__version__} | scikit-learn {sklearn.__version__} | numpy {np.__version__}")
    print(f"Sėkla: {SEED}")
    print("Tekstinis laukas: genres + subjects (be pavadinimo ir režisieriaus)")
    print(f"TF-IDF: {', '.join(f'{k}={v}' for k, v in TFIDF_PARAMS.items() if k != 'stop_words')}, stop_words=english+{{film, films}}")
    print(f"\nC pakeitimas: pašalinti žanrai, esantys > {GENERIC_THRESHOLD:.0%} filmų:")
    for g, s in generic.items():
        print(f"    {g:<20} {s:.1%}")
    for m in (model_b, model_c):
        print(f"\n{m.name}: žodynas {len(m.vectorizer.vocabulary_)} žodžių | tuščias tekstinis laukas: {m.empty_text} | nulinis vektorius: {m.empty_vector}")

    queries = pick_queries(df)

    summary = []
    for _, q in queries.iterrows():
        print("\n" + "=" * 90)
        hard = "  [SUNKI]" if q["hard_rule"] else ""
        print(f"{q['query']}: {q['title']}{hard}")
        row = df.iloc[model_b.find(q["title"])]
        print(f"  žanrai: {row['genres'] or '—'}\n  temos:  {row['subjects'] or '—'}")
        print(f"  C tekstas: {model_c.text.iloc[model_b.find(q['title'])] or '(tuščia)'}")
        print("-" * 90)
        a = popularity_baseline(df, q["title"])
        b = model_b.recommend(q["title"])
        c = model_c.recommend(q["title"])
        print_table("A · populiarumo bazinis", a)
        print_table(model_b.name, b)
        print_table(model_c.name, c)
        both = 0 if b is None or c is None else len(set(b["title"]) & set(c["title"]))
        print(f"  B ir C bendrų rekomendacijų: {both}/5")
        summary.append((q["query"], both))

    print("\n" + "=" * 90)
    print("Suvestinė: kiek B ir C rekomendacijų sutampa (iš 5)")
    for name, both in summary:
        print(f"  {name:<6} {both}")


if __name__ == "__main__":
    main()
