Only the `text` column was used; `label` and `is_clickbait` were removed
immediately after loading and not viewed.

Cleaning steps:
1. Removed missing text values.
2. Stripped whitespace from the start and end of each text.
3. Removed texts that were empty after stripping.
4. Removed exact duplicates (case-sensitive, after stripping).

| Step | Documents |
| --- | ---: |
| Original rows | 50000 |
| After removing empty text | 50000 |
| After removing exact duplicates | 4845 |
| Sample used for all runs | 1000 (seed 42) |

## Selection of 20 headlines

20 headlines were selected with a random draw from the 1,000-document
sample (pandas `sample`, seed 7). Each headline has an ID (H01–H20) and its original row number in
headlines_train.csv (`orig_row`).

| ID | orig_row | Full text | Proposed group(s) | Ambiguity/reason |
| --- | ---: | --- | --- | --- |
| H01 | 17568 | 86 This trick will change your life forever (Kaunas) | finance/tech | a trick in which area? |
| H02 | 3734 | How to speed up your computer with simple tweaks (Madrid) | tech | computer |
| H03 | 9103 | 60 Kaip pagreitinti kompiuterį paprastais triukais (New York) | tech | kompiuteris |
| H04 | 11889 | 98 Treneris aiškino naują gynybos taktiką po rungtynių | sports | treneris, rungtynės |
| H05 | 9488 | 32 Star player signs a multi-year contract with club | sports | player, club |
| H06 | 26496 | 2 Coach explains new defensive tactics after the game | sports | coach |
| H07 | 29197 | 61 Atviro kodo bibliotekos pagreitina mašininio mokymosi procesus | tech | ML |
| H08 | 45270 | 45 She did X — what happens next will shock you — Read more | sports/finance/tech | did what in which area? |
| H09 | 34547 | 44 „Apple“ pristatė naują iPhone su pažangia kamera ir DI funkcijomis (Berlin) | tech | iPhone |
| H10 | 24439 | 32 Stock market falls amid inflation concerns dėl rinkos reakcijos | finance | inflation, rinka |
| H11 | 20061 | 65 Atviro kodo bibliotekos pagreitina mašininio mokymosi procesus | tech | ML |
| H12 | 23362 | 2 10 reasons you should never buy this gadget | tech | gadget |
| H13 | 29762 | 96 Top 7 paslaptys, kurias įmonės nenori, kad žinotumėte (London) | finance/tech | kieno įmonės? |
| H14 | 18305 | 11 Major security breach affects millions of users worldwide analitikų teigimu | tech | security breach |
| H15 | 17599 | Žvaigždė pasirašė daugiametę sutartį su klubu as markets react (Madrid) | finance | market |
| H16 | 41312 | 9 Žvaigždė pasirašė daugiametę sutartį su klubu (Paris) | sports | sutartis, klubas |
| H17 | 10905 | 3 10 reasons you should never buy this gadget | tech | gadget |
| H18 | 13032 | 44 Earnings beat expectations as revenue grows in cloud segment | finance | revenue |
| H19 | 445 | Top 7 secrets companies don't want you to know (London) | finance/tech | which companies, what area? |
| H20 | 5242 | 45 Perėjimų gandai: jaunas puolėjas gali kainuoti rekordą | sports | puolėjas |

