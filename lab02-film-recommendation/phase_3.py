import argparse
import difflib

import numpy as np

from phase_1 import describe, load_and_clean
from phase_2 import K, build_models, short

CHOSEN_MODEL = "B"
MIN_TOKENS = 2


def tokens_used(model, vec):
    inv = {i: w for w, i in model.vectorizer.vocabulary_.items()}
    return [inv[i] for i in vec.indices]


def show(res, model, vec):
    used = tokens_used(model, vec)
    print(f"  Žodžiai, kuriuos modelis atpažino ({len(used)}): {', '.join(sorted(used)) or '—'}")
    if res is None or len(res) == 0:
        print("  Tekstinis laukas tuščias modelio žodyne — įrodymų nepakanka rekomendacijai.")
        return
    if len(used) < MIN_TOKENS:
        print(f"  ĮSPĖJIMAS: atpažinta mažiau nei {MIN_TOKENS} žodžiai — rekomendacijos menkai pagrįstos.")
    sims = res["similarity"].to_numpy()
    if np.isclose(sims, sims[0]).all():
        print("  ĮSPĖJIMAS: visų rekomendacijų panašumas vienodas — tvarką lemia populiarumas, ne turinys.")
    for i, r in res.iterrows():
        print(f"   {i + 1}. {r['similarity']:.3f}  {short(r['title'], 40):<40} ({r['year']})  {short(r['director'] or '—', 22)}")
        print(f"              žanrai: {short(r['genres'], 75)}")
        if r["subjects"]:
            print(f"              temos:  {short(r['subjects'], 75)}")


def run_title(df, model, title, k, pause):
    idx = model.find(title)
    if idx is None:
        close = difflib.get_close_matches(title, df["title"].tolist(), n=5, cutoff=0.6)
        print(f"  '{title}' rinkinyje nerasta." + (f" Gal: {' | '.join(close)}" if close else ""))
        print("  Galite pateikti žanrus / temas su --text arba 'text:' režimu.")
        return
    describe(df.iloc[idx])
    print(f"  Modelio tekstas: {model.text.iloc[idx] or '(tuščia)'}")
    if pause:
        input("  Pasakykite prognozę, tada spauskite Enter...")
    show(model.recommend(title, k), model, model.X[idx])


def run_text(model, text, k, pause):
    cleaned = " ; ".join(p.strip() for p in text.split(";") if p.strip() and p.strip() not in model.drop_genres)
    vec = model.vectorizer.transform([cleaned])
    print(f"  Naujas kūrinys: {text}")
    if pause:
        input("  Pasakykite prognozę, tada spauskite Enter...")
    show(model.recommend_text(text, k), model, vec)


def main():
    p = argparse.ArgumentParser(description="Gynimas: rekomendacijos nematytiems kūriniams be permokymo")
    p.add_argument("titles", nargs="*", help="filmų pavadinimai iš rinkinio")
    p.add_argument("--text", action="append", default=[], help="naujas žanrų/temų sąrašas, atskirtas ';'")
    p.add_argument("--model", choices=["B", "C"], default=CHOSEN_MODEL)
    p.add_argument("--k", type=int, default=K)
    p.add_argument("--compare", action="store_true", help="parodyti ir kitą modelį")
    args = p.parse_args()

    df = load_and_clean(verbose=False)
    model_b, model_c, _ = build_models(df)
    models = {"B": model_b, "C": model_c}
    order = [args.model] + ([m for m in models if m != args.model] if args.compare else [])
    print(f"Modelis apmokytas vieną kartą ({len(df)} filmų). Naudojamas: {', '.join(models[m].name for m in order)}")

    jobs = [("title", t) for t in args.titles] + [("text", t) for t in args.text]
    interactive = not jobs

    def run(kind, value):
        for m in order:
            print("\n" + "=" * 90 + f"\n[{models[m].name}]")
            if kind == "title":
                run_title(df, models[m], value, args.k, interactive and m == order[0])
            else:
                run_text(models[m], value, args.k, interactive and m == order[0])

    if not interactive:
        for kind, value in jobs:
            run(kind, value)
        return

    print("Įveskite pavadinimą arba 'text: žanras ; tema ; ...'. Tuščia eilutė — pabaiga.")
    while True:
        line = input("\n> ").strip()
        if not line:
            break
        if line.lower().startswith("text:"):
            run("text", line[5:].strip())
        else:
            run("title", line)


if __name__ == "__main__":
    main()
