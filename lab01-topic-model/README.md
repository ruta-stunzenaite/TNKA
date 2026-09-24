# Lab 1 — LDA Topic Model for News Headlines

## Setup
1. Place `headlines_train.csv` (from Lab01_Materials.zip) in `data/`.
2. Create and activate a virtual environment, then install packages:

       python -m venv .venv
       .venv\Scripts\Activate.ps1
       python -m pip install -r requirements.txt

## Run
Run all commands from the `lab01-topic-model` folder, in this order:

| Step | Command | What it does |
| --- | --- | --- |
| 1 | `python stage_1.py` | Cleans the data, samples 1,000 headlines, selects the 20 headlines for the initial analysis |
| 2 | `python stage_2.py` | Runs A and B: two topic counts with the original preprocessing |
| 3 | `python stage_3.py` | Run C: selected topic count with filler phrases removed (final model) |
| 4 | `python predict.py "headline 1" "headline 2"` | Analyses new headlines with the fitted run C model (no retraining) |

Running `python predict.py` without arguments starts interactive mode: type one
headline per line and press Enter on an empty line to finish.

`predict.py` prints the retained vocabulary words and the topic weights for each
headline. If no vocabulary words remain, it reports that there is insufficient
evidence and assigns no topic.

## Files
| File | Purpose |
| --- | --- |
| `stage_1.py` | Data preparation |
| `stage_2.py` | Shared pipeline (`run_lda`) and runs A, B |
| `stage_3.py` | Run C |
| `preprocessing.py` | Filler-phrase removal used by run C and needed to load its model |
| `predict.py` | Inference on new headlines |
| `initial-analysis.md` | Initial analysis, written before modelling and unchanged |
| `report.md` | Report |

## Outputs
Stage 1:
- `outputs/sample_collection.csv` – the 1,000 headlines used in all runs
- `outputs/initial_20_headlines.csv` – the 20 headlines for the initial analysis

Stages 2 and 3 (for each run X = A, B, C):
- `outputs/run_X_topics.csv` – size, top 10 words and representative headlines per topic
- `outputs/run_X_doc_topics.csv` – retained word count, dominant topic and topic weights for every headline
- `outputs/run_X_initial20.csv` – model output for the initial 20 headlines
- `models/run_X.joblib` – fitted vectorizer and LDA model (not in the repository;
  recreated by running the scripts)

## Parameters and seeds

### Data
| Setting | Value |
| --- | --- |
| Rows: original / after removing empty / after removing duplicates | 50,000 / 50,000 / 4,845 |
| Sample size | 1,000 |
| Sample seed | 42 |
| Seed for selecting 20 headlines | 7 |

### Preprocessing (original, runs A and B)
| Setting | Value |
| --- | --- |
| Lowercase | yes |
| Token pattern | `(?u)\b[^\W\d_]{2,}\b` (letters only, 2+ characters) |
| Stop words | scikit-learn English list + custom Lithuanian list (in `stage_2.py`) |
| min_df | 2 |
| max_features | 3,000 (not reached; vocabulary 213 words) |
| Empty documents | counted and excluded from fitting and assignment (none occurred) |

### Change in run C
Six appended filler phrases are removed as whole phrases before tokenisation
(`preprocessing.py`): "as markets react", "dėl rinkos reakcijos",
"analitikų teigimu", "analysts say", "after report", "po pranešimo".
Vocabulary: 205 words.

### LDA (fixed for all runs)
| Setting | Value |
| --- | --- |
| Learning method | batch |
| max_iter | 30 |
| Model seed | 42 |
| Other parameters | scikit-learn defaults |

### Runs
| Run | Topic count | Preprocessing |
| --- | ---: | --- |
| A | 10 | Original |
| B | 4 | Original |
| C (final) | 4 | Filler phrases removed |

## Environment
- Python: 3.13.x
- pandas x.x.x, scikit-learn x.x.x, numpy x.x.x, joblib x.x.x (full list in `requirements.txt`)