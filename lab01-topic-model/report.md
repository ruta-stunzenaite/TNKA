# Laboratory 1 — Editor's recommendation

Name:  Rūta Stunžėnaitė
Date:  2026-09-25

# Lab 1 — LDA Topic Modelling of News Headlines

**Summary of work, results and conclusions**

---

## Summary

An LDA topic model was trained on 1,000 unique headlines to test whether it could organise headlines into clear, news-based topics for an editor. Three controlled runs were compared: 3 topics (A), 4 topics (B), and 4 topics with appended filler phrases removed (C). Run C was selected as the final model.

The main finding is that the model groups **headline templates, not news subjects**. Every copy of a template (the same sentence with different numbers, cities or filler endings) is assigned to the same topic, and each topic is an arbitrary bundle of several templates from different subjects. English and Lithuanian versions of the same story end up in different topics in 10 of 15 translation pairs. Removing filler phrases cleaned the topic vocabulary but did not change how headlines were grouped. The model is **not ready for the editor** without human review.

---

## 1. Objective

The editor wants headlines grouped into topics that are:

- clear and distinguishable,
- based on news content rather than place names or repeated templates,
- able to reflect that a headline may belong to several topics.

The task was to build a working LDA workflow, compare two topic counts, test one preprocessing decision, and judge the result using concrete headlines.

---

## 2. Data

| Step | Documents |
| --- | ---: |
| Original rows in `headlines_train.csv` | 50,000 |
| After removing missing/empty text | 50,000 |
| After removing exact duplicates (after stripping whitespace) | 4,845 |
| Random sample used in all runs (seed 42) | 1,000 |

Only the `text` column was used; `label` and `is_clickbait` were dropped immediately after loading.

About 90% of the rows were exact duplicates. The remaining unique headlines are still highly repetitive: roughly 25 base sentences in English and Lithuanian, varied by a leading number (e.g. "86"), a city in brackets (e.g. "(Kaunas)") and optional filler endings (e.g. "as markets react", "analitikų teigimu"). This is a teaching dataset and does not represent real news.

For the initial analysis, 20 headlines (H01–H20) were drawn at random from the sample (seed 7), each with its original row number as a stable ID.

---

## 3. Method

### 3.1 Preprocessing (original)

| Choice | Setting | Reason |
| --- | --- | --- |
| Lowercasing | yes | "Apple" and "apple" count as one word |
| Tokens | letters only, ≥2 characters: `(?u)\b[^\W\d_]{2,}\b` | Removes punctuation and the leading numbers, which carry no content |
| Stop words | scikit-learn English list + 42 Lithuanian function words | Both languages appear in the data |
| `min_df` | 2 | A word in only one headline cannot link headlines together |
| `max_features` | 3,000 | Suggested cap; had no effect (vocabulary was 213 words) |
| Empty documents | counted, excluded from fitting and assignment | No evidence means no topic; none occurred (minimum 3 retained words) |

### 3.2 Model

scikit-learn `LatentDirichletAllocation` on a word-count document–term matrix: batch learning, `max_iter=15`, `random_state=42`, other parameters at their defaults. Topic weights for each headline come from `lda.transform`. Representative headlines are those with the highest weight for a topic.

### 3.3 Runs

| Run | Topics | Preprocessing | Vocabulary | Empty docs |
| --- | ---: | --- | ---: | ---: |
| A | 3 | Original | 213 | 0 |
| B | 4 | Original | 213 | 0 |
| C | 4 | Original + filler phrases removed | 205 | 0 |

All other settings, the document collection and the seed were identical across runs.

---

## 4. Initial analysis (before modelling)

The 20 headlines were grouped manually into **tech, sports and finance**, with several marked ambiguous (e.g. clickbait headlines such as H08 "She did X — what happens next will shock you" with no identifiable subject). The full analysis is in `initial-analysis.md` and was not changed afterwards.

Predicted modelling problems:

1. City names would link unrelated headlines.
2. Templates would produce topics per template rather than per subject.
3. English and Lithuanian versions of the same story would split (Messi example).
4. Mixed-language filler could leave headlines with no retained words.

---

## 5. Results

### 5.1 Topic count: A (3) vs B (4)

Both runs produced mixed topics (top words in Appendix A).

- **A:** clickbait was mixed with Apple news (topic 1) and with Messi and machine-learning headlines (topic 2). Topic sizes were uneven (224 / 337 / 439).
- **B:** topics were more balanced (191 / 251 / 328 / 230). One topic's top words were dominated by Apple/iPhone terms, but that topic also contained 196 non-Apple headlines (finance, a Lithuanian sports template, start-up and computer-tips headlines), so it was not a clean topic.
- Filler words appeared among the top words in both runs (e.g. `markets`, `analysts`).

**Provisional choice: 4 topics.** It is closest to the three manual groups plus clickbait, and B's topics were more balanced than A's. Neither run produced clean subject-based topics.

### 5.2 Preprocessing test: removing filler phrases (C)

**Issue observed.** Six appended phrases occurred across all subjects: "dėl rinkos reakcijos" (52 headlines), "analitikų teigimu" (47), "po pranešimo" (40), "as markets react" (29), "analysts say" (24), "after report" (18).

**Change.** These phrases were removed as whole phrases before tokenisation. Words like `markets` were deliberately not made stop words, because they also occur in genuine finance headlines.

**Prediction.** Filler words would leave the top words and filler-bearing headlines would move to their content topics (e.g. H15, a sports contract story ending in "as markets react"). A possible cost was losing attribution information ("analysts say").

**Observed.**

| Aspect | Result |
| --- | --- |
| Vocabulary | 8 words removed: `analitikų, pranešimo, react, reakcijos, report, rinkos, say, teigimu`. `markets` and `analysts` remained, as they also occur in real templates |
| Top words | Filler-specific words no longer appear |
| Headline assignment | **No meaningful change.** In A, B and C alike, every headline follows its template. H15 was already in the same topic as H16 (the same story without the filler) in all three runs |
| Unexpected outcome | Templates were reshuffled between topics. For example, "Coach explains new defensive tactics" moved from the Messi/clickbait topic (B) to the English-clickbait topic (C), without becoming more coherent |
| Incomplete list | Other fillers remain: "amid concerns" (34), "Find out why" (32), "in a surprise move" (29), "— Number 5 is shocking" (20) |

**Conclusion.** The prediction was supported for the vocabulary but **not supported for the grouping**. The filler words (2–3 per headline) are too weak to override the template's 5–9 shared content words. The change is kept because it makes top words easier to read without any observed loss in grouping, but it does not fix the underlying problem.

---

## 6. Final model (Run C, 4 topics)

Names are based on top words, representative headlines and the templates each topic contains (Appendix B). All topics are mixed.

| Topic | Name | Top words | Representative headlines (by weight) |
| --- | --- | --- | --- |
| 0 | Mixed: finance, security & Lithuanian tech/sports | procesus, mašininio, kodo, mokymosi, pagreitina, bibliotekos, atviro, laimėjo, komanda, vietos | "Central bank cuts rates, markets rally on dovish guidance amid concerns (Madrid)"; "Central bank cuts rates, markets rally on dovish guidance in a surprise move (Vilnius)" |
| 1 | Mixed: consumer tech, start-ups & clickbait | won, believe, happened, triukais, paprastais, pagreitinti, kompiuterį, ai, million, platform | "90 „Apple“ pristatė naują iPhone … dėl rinkos reakcijos (New York)"; "75 „Apple“ pristatė naują iPhone … (New York)" |
| 2 | Mixed: markets, football & Apple | inflation, concerns, amid, messi, new, falls, market, stock, iphone, apple | "Apple unveils a new iPhone … amid concerns (Kaunas)"; "Investors hedge inflation risk using index-linked bonds amid concerns" |
| 3 | Mostly English clickbait (+ English sports & ML) | new, forever, change, life, trick, open, machine, learning, libraries, workflows | "Startuolis pritraukė 50 mln. USD DI platformos plėtrai in a surprise move (New York)"; "Šis triukas pakeis jūsų gyvenimą amžiams — Number 5 is shocking (New York)" |

In topic 0, the top words point to Lithuanian tech and sports while the representative headlines are finance. This disagreement is itself evidence that the topic mixes unrelated material.

---

## 7. Comparison with the initial analysis

| Headline(s) | Manual group | Model (C) | Discussion |
| --- | --- | --- | --- |
| H04 / H06 (coach explains tactics, LT / EN) | sports / sports | topic 0 (0.89) / topic 3 (0.89) | Disagreement: the same story in two languages shares almost no words |
| H15 / H16 (star signs contract, with / without "as markets react") | finance / sports | both topic 1 | The manual label for H15 was itself influenced by the filler; the model groups the two versions together because they share the template |
| H12 / H17 ("10 reasons you should never buy this gadget") | tech | topic 3 | The model groups these with other clickbait templates. Arguably it captures the headline *style* better than the manual subject label; neither is automatically correct |
| H10 / H18 (stock market falls / earnings beat expectations) | finance / finance | topic 2 / topic 0 | Finance is split across two topics, each shared with unrelated subjects |

**Predictions revisited.**

| Prediction | Outcome |
| --- | --- |
| City names link unrelated headlines | Not supported: no city appears in any top-10 list; cities are spread across all topics |
| Templates drive topics | Supported in a stronger form: templates are never split, and each topic bundles several templates |
| Language versions split | Supported overall (10 of 15 translation pairs split), but not for the predicted Messi example (both versions in topic 2) |
| Filler may leave empty documents | Not supported: no empty documents; filler added misleading words instead |

---

## 8. Failure cases

| Headline | Model output | Why it fails the editor | Remedy / ambiguity |
| --- | --- | --- | --- |
| **H04** "Treneris aiškino naują gynybos taktiką po rungtynių" vs **H06** "Coach explains new defensive tactics after the game" | H04 → topic 0 (0.892); H06 → topic 3 (0.892) | **Language split:** the editor would receive the same story under two different topics | Translate to one language before modelling, or model each language separately |
| **H05** "Star player signs a multi-year contract with club" | topic 3 (0.906), a topic dominated by "This trick will change your life", "10 reasons…", "Top 7 secrets…" | **Template bundling:** genuine sports news is filed with clickbait | Reduce template repetition (deduplicate after removing numbers/cities), use more varied data, or flag clickbait separately |
| **H08** "She did X — what happens next will shock you — Read more" | topic 0 (0.847), a topic mostly about finance and security; 4 retained words | **Misleading confidence:** a headline with no news content gets a high weight for a news-like topic | Inherently ambiguous; show a warning when retained words are few or non-informative, and let the editor decide |

---

## 9. Recommendation

**Chosen model:** 4 topics with filler phrases removed (Run C).

**Evidence:** four topics gave more balanced groups than three; removing fillers produced cleaner top words with no observed loss in grouping.

**Accepted trade-off:** the phrase list is hand-built from this dataset and incomplete, and it discards attribution phrases ("analysts say") that could be informative in real news. The removal did not improve grouping.

**Overall judgement:** the model is **not ready** to organise headlines for the editor. It reproduces the dataset's templates and languages rather than news subjects, and its high topic weights (typically 0.87–0.91) give a false impression of certainty.

**Still requires human judgement:**

- naming and interpreting mixed topics,
- recognising the same story across languages,
- separating clickbait from news,
- assigning headlines that legitimately belong to several topics,
- deciding what to do with headlines that have little or no content.

---

## 10. Limitations

- The dataset is synthetic and template-based; results do not indicate performance on real news.
- The comparison is exploratory: one seed, three runs, no tuning, no stability or generalisation claims.
- Some topic reshuffling between runs may be caused by refitting on a changed vocabulary rather than by the preprocessing decision itself.

---

## 11. Reproducibility

| Item | Value |
| --- | --- |
| Scripts | `Stage_1.py` → `Stage_2.py` → `Stage_3.py`; `predict.py` for new headlines |
| Seeds | sample 42, selection of 20 headlines 7, LDA 42 |
| LDA | batch, `max_iter=15`, defaults otherwise |
| Vectorizer | see Section 3.1 |
| Packages | see `requirements.txt` |

`predict.py` loads the fitted vectorizer and model (`models/run_C.joblib`), analyses new headlines without retraining, prints the retained words and topic weights, and reports "insufficient evidence" when no vocabulary words remain.

---

## 12. AI use

AI assistance (Claude) was used after the initial analysis for environment setup, code writing and review, identifying the filler phrases and template structure, topic-name suggestions and drafting this summary. Counts and examples were checked against the output CSV files. Two AI claims were corrected after checking the outputs: that run B contained a clean Apple topic, and that filler removal moved H15 to a different group. The initial analysis was written without AI.

---

## Appendix A — Top words for runs A and B

**Run A (3 topics)**

| Topic | Size | Top words |
| --- | ---: | --- |
| 0 | 224 | amid, concerns, inflation, market, stock, falls, markets, naują, nacionalinį, vietos |
| 1 | 337 | iphone, apple, believe, won, new, happened, ai, camera, features, unveils |
| 2 | 439 | messi, new, life, forever, trick, change, analysts, pagreitina, kodo, bibliotekos |

**Run B (4 topics)**

| Topic | Size | Top words |
| --- | ---: | --- |
| 0 | 191 | amid, concerns, markets, inflation, stock, market, falls, naują, gynybos, rungtynių |
| 1 | 251 | believe, won, happened, shock, happens, did, kompiuterį, paprastais, pagreitinti, triukais |
| 2 | 328 | messi, new, life, forever, trick, change, pagreitina, mašininio, kodo, procesus |
| 3 | 230 | ai, record, analysts, new, iphone, apple, camera, features, advanced, unveils |

## Appendix B — Templates per topic in run C

Headlines grouped by their base sentence (leading number, city and filler ignored); counts are headlines assigned to that topic.

| Topic | Templates |
| --- | --- |
| 0 (288) | Atviro kodo bibliotekos… (34), She did X… (33), Vietos komanda laimėjo… (33), Treneris aiškino… (32), Didelė saugumo spraga… (29), Major security breach… (29), Earnings beat expectations… (29), Analysts predict record profits… (25), Central bank cuts rates… (23), Ji padarė X… (21) |
| 1 (210) | You won't believe… (38), Kaip pagreitinti kompiuterį… (33), Start-up raises $50 million… (30), Žvaigždė pasirašė… (28), Local team wins… (27), „Apple“ pristatė… (27), How to speed up… (27) |
| 2 (242) | Stock market falls… (37), Apple unveils… (34), Messi įmušė… (32), Investors hedge… (29), Messi scores… (27), Perėjimų gandai… (25), 10 priežasčių… (22), Top 7 paslaptys… (19), Negalėsite patikėti… (17) |
| 3 (260) | This trick will change… (47), Open-source libraries… (34), 10 reasons you should… (33), Coach explains… (31), Top 7 secrets… (27), Star player signs… (25), Startuolis pritraukė… (24), Transfer rumors… (23), Šis triukas pakeis… (16) |

Every template appears in exactly one topic.