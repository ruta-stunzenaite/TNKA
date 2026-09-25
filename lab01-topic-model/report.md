# Laboratory 1 — Editor's recommendation

Name:  Rūta Stunžėnaitė
Date:  2026-09-25

## 1. Decisions and prediction

Why did you choose these two topic counts?

k-values 10 and 4 were chosen out of curiosity. Chose 10 because it exceeds acctual content topics and I wanted to see if LDA would classify more according to templates than acctual topics. 4 there chosen because I used 4 in intial analysis. 

Which single preprocessing issue did you test, why, and what benefit/cost did you predict before testing?

I tested how to handle **appended filler phrases**. 

**Predicted benefit:** filler words would disappear from the top words, and
headlines carrying fillers would move to their content topic

**Predicted cost:** attribution phrases such as "analysts say" can be genuine
information in real news, the phrase list is hand-built from this dataset and
may not generalise, and a real finance headline containing "as markets react"
would lose a relevant word.

## 2. Three-run comparison

| Run | Topic count | Preprocessing | Fixed settings / seed | Evidence of usefulness or problems |
| --- | --- | --- | --- | --- |
| A | 10 | Original | 1,000 headlines (sample seed 42); letters-only tokens, EN + LT stop words, min_df 2, max_features 3000 (vocabulary 213); batch LDA, max_iter 30, seed 42; 0 empty documents | Every topic is a bundle of 2–5 templates; no template is split. Several topics are mostly one language (topic 0: Lithuanian local-team, coach and start-up headlines; topic 6: Lithuanian security breach + Lithuanian clickbait), while others mix subjects (topic 4: stock market + Messi + analysts' profit forecasts; topic 5: computer tips + Lithuanian transfer rumours + central bank). Filler words form parts of topics (`markets` in topic 5, `rinkos, reakcijos` in topic 6), so H15 is split 0.63 / 0.28 and H10 0.68 / 0.23. More topics gave smaller bundles, not clearer ones. |
| B | 4 | Original | Same as A | All four topics are mixed, e.g. topic 2 (328 headlines) holds English clickbait ("This trick…", "10 reasons…"), both Messi templates, machine-learning headlines in both languages and English sports. The same story splits by language: H04 (LT coach) → topic 0, H06 (EN coach) → topic 2. Filler words among top words (`markets` in topic 0, `analysts` in topic 3). Chosen as provisional count: fewer, more balanced groups (191–328) are easier for an editor to review, and 10 topics did not separate subjects better. |
| C | 4 (from B) | Appended filler phrases removed ("as markets react", "dėl rinkos reakcijos", "analitikų teigimu", "analysts say", "after report", "po pranešimo") | Same as B; vocabulary 205 | Filler words removed from vocabulary and top words. Headlines with and without filler now get identical weights (H15 = H16 = 0.892). Grouping is still by template and still mixed; templates were reshuffled between topics without becoming more coherent. |

**Concrete headline evidence of the preprocessing effect**

- **Benefit, H15 vs H16:** H15 ("Žvaigždė pasirašė daugiametę sutartį su klubu
  *as markets react*") and H16 (the same story without the filler) were already
  in the same topic in B, but the filler changed H15's weights: 0.916 vs 0.891
  for H16 in B, and in the 10-topic run A it pulled 0.28 of H15's weight into a
  topic containing `markets`. In C both headlines get identical weights (0.892),
  so the filler no longer influences the result.
- **Prediction only partly supported:** I expected filler-bearing headlines to
  move to their content topic. In all runs, every headline already followed its
  template, because the 2–3 filler words cannot outweigh the template's shared
  content words. The effect was on weights and top words, not on grouping.
- **Unexpected outcome, reshuffled templates:** changing the vocabulary moved
  whole templates between topics without improving coherence. H05 ("Star player
  signs a multi-year contract with club") moved from a topic with stock-market
  and Lithuanian sports headlines (B, topic 0) to a topic dominated by English
  clickbait (C, topic 3). H14 (security breach) moved from a clickbait topic
  (B, topic 1) to a topic with finance and Lithuanian machine-learning
  headlines (C, topic 0).
- **Cost, lost information:** H14 ends in "analitikų teigimu" (according to
  analysts). This attribution is removed in C, reducing its retained words from
  9 to 7. In real news, the source of a claim can matter to an editor.

## 3. Final model and failure analysis

The final model is run C (4 topics, filler phrases removed). All four topics are
mixed; names, top words and two representative headlines per topic are in
Appendix B.

### Comparison with my initial grouping

| Headline(s) | My initial group | Model output (C) | Agreement? |
| --- | --- | --- | --- |
| H02 "How to speed up your computer…" / H03 "Kaip pagreitinti kompiuterį…" | tech / tech | both topic 1 (0.874 / 0.890) | **Agree:** both are in the topic containing consumer tech, and this translation pair stays together |
| H15 "Žvaigždė pasirašė… as markets react" / H16 same story without filler | finance / sports | both topic 1 (0.892 each) | **Partly:** the model correctly treats them as the same story, whereas my label for H15 was influenced by the filler "as markets react". But topic 1 is not a sports topic, so the model's topic doesn't match either of my labels |
| H12 "10 reasons you should never buy this gadget" | tech | topic 3 (0.812) | **Disagree:** the model groups it with clickbait templates. It captures the headline's *style* rather than its subject; neither view is automatically correct |
| H10 "Stock market falls amid inflation concerns…" / H18 "Earnings beat expectations…" | finance / finance | topic 2 (0.893) / topic 0 (0.906) | **Disagree:** finance is split across two topics, each shared with unrelated subjects (Messi and Apple in topic 2; security and Lithuanian machine learning in topic 0) |

### Failure cases

| Headline ID and text | Actual model output | Why it fails the editor's needs | Possible remedy or inherent ambiguity |
| --- | --- | --- | --- |
| **H04** "98 Treneris aiškino naują gynybos taktiką po rungtynių" and **H06** "2 Coach explains new defensive tactics after the game" | H04 → topic 0 (0.892); H06 → topic 3 (0.892) | **Language split:** the same story is filed under two different topics because the English and Lithuanian versions share no words. This happens for 10 of 15 translation pairs in the collection | Translate headlines into one language before modelling, or model each language separately |
| **H05** "32 Star player signs a multi-year contract with club" | topic 3 (0.906), a topic dominated by clickbait templates ("This trick will change your life forever", "10 reasons…", "Top 7 secrets…") | **Template bundling:** genuine sports news is grouped with clickbait. Each topic is a bundle of whole templates rather than a subject | Reduce template repetition in the training data, use more varied real headlines, or flag clickbait with a separate step so it doesn't share topics with news |
| **H08** "45 She did X — what happens next will shock you — Read more" | topic 0 (0.847), a topic mostly containing finance, security and Lithuanian machine-learning headlines; 4 retained words | **Misleading confidence:** a headline with no news content gets a high weight for a news topic. The weights mostly reflect how many words a headline has: all 6-word headlines get 0.892, all 7-word ones 0.906, whatever they are about | Inherently ambiguous, since there is no subject to find. The program could warn when a headline has few informative words, and the editor should decide |

The three cases cover three distinct kinds of problem: language, template
structure, and misleading confidence.

## Appendix A — Top words for all runs

**Run A (10 topics, original preprocessing)**

| Topic | Size | Top words |
| --- | ---: | --- |
| 0 | 89 | čempionatą, vietos, pratęsimuose, komanda, nacionalinį, laimėjo, taktiką, treneris, aiškino, gynybos |
| 1 | 131 | won, believe, happened, worldwide, users, major, millions, breach, affects, security |
| 2 | 124 | trick, forever, change, life, new, coach, defensive, explains, game, tactics |
| 3 | 87 | ai, new, apple, iphone, unveils, features, advanced, camera, million, scale |
| 4 | 89 | concerns, amid, analysts, inflation, stock, falls, market, messi, league, goal |
| 5 | 108 | markets, paprastais, kompiuterį, pagreitinti, triukais, simple, speed, tweaks, computer, rekordą |
| 6 | 46 | reakcijos, rinkos, spraga, saugumo, vartotojų, milijonus, didelė, paveikė, įvyko, negalėsite |
| 7 | 93 | shock, happens, did, reasons, buy, gadget, local, overtime, national, championship |
| 8 | 148 | procesus, mašininio, kodo, mokymosi, pagreitina, atviro, bibliotekos, įmušė, lygų, taurėje |
| 9 | 85 | workflows, source, machine, learning, open, libraries, accelerate, linked, investors, hedge |

**Run B (4 topics, original preprocessing)**

| Topic | Size | Top words |
| --- | ---: | --- |
| 0 | 191 | concerns, amid, markets, inflation, stock, market, falls, naują, gynybos, rungtynių |
| 1 | 251 | won, believe, happened, shock, happens, did, kompiuterį, paprastais, pagreitinti, triukais |
| 2 | 328 | messi, new, life, forever, trick, change, pagreitina, mašininio, kodo, procesus |
| 3 | 230 | ai, record, analysts, new, iphone, apple, camera, features, advanced, unveils |

**Run C (4 topics, filler phrases removed)**

| Topic | Size | Top words |
| --- | ---: | --- |
| 0 | 288 | procesus, mašininio, kodo, mokymosi, pagreitina, bibliotekos, atviro, laimėjo, komanda, vietos |
| 1 | 210 | won, believe, happened, triukais, paprastais, pagreitinti, kompiuterį, ai, million, platform |
| 2 | 242 | inflation, concerns, amid, messi, new, falls, market, stock, iphone, apple |
| 3 | 260 | new, forever, change, life, trick, open, machine, learning, libraries, workflows |

Topic numbers are arbitrary and do not correspond between runs.

## Appendix B — Final model (run C) topics

| Topic | Name | Top words | Representative headlines (highest weight) |
| --- | --- | --- | --- |
| 0 (288) | Mixed: finance, security & Lithuanian tech/sports | procesus, mašininio, kodo, mokymosi, pagreitina, bibliotekos, atviro, laimėjo, komanda, vietos | "Central bank cuts rates, markets rally on dovish guidance amid concerns (Madrid)"; "Central bank cuts rates, markets rally on dovish guidance in a surprise move (Vilnius)" |
| 1 (210) | Mixed: consumer tech, start-ups & clickbait | won, believe, happened, triukais, paprastais, pagreitinti, kompiuterį, ai, million, platform | "90 „Apple“ pristatė naują iPhone su pažangia kamera ir DI funkcijomis dėl rinkos reakcijos (New York)"; "75 „Apple“ pristatė naują iPhone su pažangia kamera ir DI funkcijomis (New York)" |
| 2 (242) | Mixed: markets, football & Apple | inflation, concerns, amid, messi, new, falls, market, stock, iphone, apple | "Apple unveils a new iPhone with advanced camera and AI features amid concerns (Kaunas)"; "Investors hedge inflation risk using index-linked bonds amid concerns" |
| 3 (260) | Mostly English clickbait (+ English sports & ML) | new, forever, change, life, trick, open, machine, learning, libraries, workflows | "Startuolis pritraukė 50 mln. USD DI platformos plėtrai in a surprise move (New York)"; "Šis triukas pakeis jūsų gyvenimą amžiams — Number 5 is shocking (New York)" |



## 4. Recommendation

**Chosen model and preprocessing:** 4 topics with appended filler phrases removed
(run C).

**Evidence for the choice:** 10 topics (run A) did not separate subjects more
clearly; it produced smaller bundles of 2–5 templates, some split by language
and some mixing unrelated subjects (e.g. stock market, Messi and analysts'
forecasts in one topic). With 4 topics, the groups are more balanced (210–288
headlines in run C) and fewer topics are easier for an editor to review.
Removing the filler phrases removed filler words from the vocabulary and top
words, and headlines with and without filler now receive identical weights
(H15 = H16 = 0.892), with no observed loss in grouping compared with run B.
Increasing max_iter from 15 to 30 did not change runs B and C, so the results
are not caused by too little training.

**Accepted trade-off:** the phrase list is hand-built from this dataset and
incomplete (fillers such as "amid concerns" and "in a surprise move" remain),
and it removes attribution that can matter in real news (H14 loses "analitikų
teigimu"). The change cleaned the topic vocabulary but did not make the
grouping more subject-based. All four final topics are mixed.

**Overall judgement:** the model is **not ready** to organise headlines for the
editor. It groups whole headline templates rather than news subjects, splits
the same story by language (H04 vs H06), mixes news with clickbait (H05), and
its topic weights mostly reflect headline length rather than fit, which makes
assignments look more certain than they are (H08: 0.847 with no news content).

**Still requires human judgement:**
- naming and interpreting mixed topics,
- recognising the same story in English and Lithuanian,
- separating clickbait from news,
- assigning headlines that belong to several topics,
- deciding what to do with headlines that have little or no content.

**Possible next steps (not tested):** translate headlines into one language or
model each language separately, reduce template repetition, flag clickbait
separately, and evaluate on more varied real headlines.

## 5. Sources and AI use

**Sources**
- scikit-learn documentation: `LatentDirichletAllocation` and `CountVectorizer`
  (https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html)
- pandas documentation (reading, cleaning and sampling data)
- Course materials: `assignment.md`, `report-template.md`, `headlines_train.csv`

No code was reused from other sources.

**AI tools and purposes**

I used Claude (Anthropic) for:
- setting up VS Code, the virtual environment, `.gitignore` and the GitHub repository;
- explaining the assignment steps and the meaning of settings (`min_df`,
  `max_features`, token pattern, `max_iter`);
- reviewing and correcting my data-preparation script (`stage_1.py`: file
  paths, stable IDs, dropping label columns, seeded selection of the 20
  headlines);
- formatting the empty 20-headline table and checking the initial analysis
  against the assignment's requirements (structure only; the groupings,
  ambiguity explanations and predictions are my own);
- writing the modelling code (`stage_2.py`, `stage_3.py`, `preprocessing.py`,
  `predict.py`);
- Drafting some of the report text.

The initial analysis (groupings, ambiguities and predictions) was written without
AI. The defence will be done without AI assistance.

## Defence preparation

Ensure your program can analyse instructor-provided headlines using the fitted vocabulary and model. Handle inputs with no retained terms. Be prepared to predict, run and explain; no separate new-text experiment or written defence answers are required beforehand.
