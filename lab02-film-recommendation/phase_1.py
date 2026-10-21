import sys
from pathlib import Path

import numpy as np
import pandas as pd

DATA_FILE = "movies_wikidata_4000.csv"
SEED = 42
N_INSPECT = 15
N_QUERIES = 5
N_HARD = 1
SEP = " ; "

def normalize_space(s):
    return s.fillna("").astype(str).str.replace(r"\s+", " ", regex=True).str.strip()


def split_list(value):
    if not isinstance(value, str) or not value.strip():
        return []
    return [p.strip() for p in value.split(";") if p.strip()]


def load_and_clean(path=DATA_FILE, verbose=True):
    if not Path(path).exists():
        sys.exit(f"Nerastas failas '{path}'. Įdėkite jį į darbinį katalogą: {Path.cwd()}")
    raw = pd.read_csv(path, encoding="utf-8")
    df = raw.copy()
    df["title"] = normalize_space(df["title"])
    for col in ["director", "genres", "subjects", "countries"]:
        df[col] = normalize_space(df[col])

    n_raw = len(df)
    empty_mask = df["title"] == ""
    n_empty = int(empty_mask.sum())
    df = df[~empty_mask]

    df = df.sort_values(["sitelinks", "movie_id"], ascending=[False, True])
    dup_mask = df["title"].str.casefold().duplicated(keep="first")
    n_dup = int(dup_mask.sum())
    df = df[~dup_mask].reset_index(drop=True)

    if verbose:
        print("=" * 70)
        print(f"Duomenų failas: {path}")
        print(f"Eilučių iš viso:                    {n_raw}")
        print(f"Pašalinta tuščių pavadinimų:        {n_empty}")
        print(f"Pašalinta pasikartojančių:          {n_dup}")
        print(f"Kūrinių po valymo:                  {len(df)}")
        print("-" * 70)
        print("Trūkstamos reikšmės po valymo:")
        for col in ["director", "genres", "subjects", "countries"]:
            print(f"  {col:<10} tuščia: {(df[col] == '').sum():>5}  ({(df[col] == '').mean():.1%})")
        print("=" * 70)
    return df


def hardness_mask(df):
    no_subjects = df["subjects"] == ""
    n_genres = df["genres"].apply(lambda v: len(split_list(v)))
    return no_subjects & (n_genres <= 2)


def describe(row, i=None):
    head = f"[{i}] " if i is not None else ""
    print(f"{head}{row['title']} ({row['year']}) | rež.: {row['director'] or '—'} | sitelinks: {row['sitelinks']}")
    print(f"     žanrai: {row['genres'] or '—'}")
    print(f"     temos:  {row['subjects'] or '—'}")
    print(f"     šalys:  {row['countries'] or '—'}")


def inspect_sample(df, n=N_INSPECT, seed=SEED):
    sample = df.sample(n=n, random_state=seed)
    print(f"\n{n} atsitiktinių filmų apžiūrai (sėkla {seed}):\n")
    for i, (_, row) in enumerate(sample.iterrows(), 1):
        describe(row, i)
    return sample


def pick_queries(df, seed=SEED, n=N_QUERIES, n_hard=N_HARD):
    rng = np.random.default_rng(seed)
    hard = hardness_mask(df)
    hard_idx = df.index[hard].to_numpy()
    easy_idx = df.index[~hard].to_numpy()
    chosen_easy = rng.choice(easy_idx, size=n - n_hard, replace=False)
    chosen_hard = rng.choice(hard_idx, size=n_hard, replace=False)
    q = df.loc[np.concatenate([chosen_easy, chosen_hard])].copy()
    q["hard_rule"] = [False] * (n - n_hard) + [True] * n_hard
    q.insert(0, "query", [f"Q{i}" for i in range(1, n + 1)])
    return q.reset_index(drop=True)


def main():
    df = load_and_clean()
    inspect_sample(df)

    hard = hardness_mask(df)
    print(f"\nSunkių kandidatų (nėra temų ir <= 2 žanrai): {int(hard.sum())}")
    q = pick_queries(df)
    print(f"\nUžklausų kūriniai (metodas: numpy default_rng({SEED}); {N_QUERIES - N_HARD} iš įprastų, {N_HARD} iš sunkių):\n")
    for _, row in q.iterrows():
        tag = "  <- SUNKI (taisyklė)" if row["hard_rule"] else ""
        print(f"{row['query']}{tag}")
        describe(row)
        print()

if __name__ == "__main__":
    main()
