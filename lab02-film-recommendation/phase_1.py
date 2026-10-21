"""Phase 1: clean titles and pick 5 query books reproducibly."""
import pandas as pd

DATA_FILE = "books_gutenberg_4000.csv"
SEED = 42
N_QUERIES = 5


def normalise_title(titles: pd.Series) -> pd.Series:
    """Trim ends and collapse repeated whitespace inside titles."""
    return (
        titles.astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )


def clean_titles(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Drop empty and duplicate titles; return cleaned data and counts."""
    df = df.copy()
    df["title"] = normalise_title(df["title"])
    counts = {"before": len(df)}

    is_empty = df["title"].isna() | (df["title"] == "")
    counts["empty"] = int(is_empty.sum())
    df = df[~is_empty]

    is_duplicate = df.duplicated(subset="title", keep="first")
    counts["duplicates"] = int(is_duplicate.sum())
    df = df[~is_duplicate].reset_index(drop=True)

    counts["after"] = len(df)
    return df, counts


def main() -> None:
    raw = pd.read_csv(DATA_FILE)
    books, counts = clean_titles(raw)

    print("=== Cleaning ===")
    print(f"Rows before:        {counts['before']}")
    print(f"Empty titles:       {counts['empty']}")
    print(f"Duplicate titles:   {counts['duplicates']}")
    print(f"Rows after:         {counts['after']}")

    queries = books.sample(N_QUERIES, random_state=SEED)
    print(f"\n=== Query books: df.sample({N_QUERIES}, random_state={SEED}) ===")
    print(queries[["book_id", "title", "author"]].to_string(index=False))



if __name__ == "__main__":
    main()