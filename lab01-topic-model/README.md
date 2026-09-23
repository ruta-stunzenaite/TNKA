# Lab 1 — Topic Model

## Setup
1. Place `headlines_train.csv` (from Lab01_Materials.zip) in `data/`.
2. Create and activate a virtual environment, then install packages:
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt

## Run
Run the scripts from the `lab01-topic-model` folder, in this order.

Stage 1 – data preparation and selection of 20 headlines:
   python stage_1.py

Stage 2 – runs A and B (two topic counts, same preprocessing):
   python stage_2.py

## Outputs
Stage 1:
- `outputs/sample_collection.csv` – the document collection used in all runs
- `outputs/initial_20_headlines.csv` – the 20 headlines for the initial analysis

Stage 2 (for each run X = A, B):
- `outputs/run_X_topics.csv` – top 10 words, size and representative headlines per topic
- `outputs/run_X_doc_topics.csv` – topic weights for every headline
- `outputs/run_X_initial20.csv` – model output for the initial 20 headlines
- `models/run_X.joblib` – fitted vectorizer and LDA model (not in the repository;
  recreated by running the script)

## Parameters and seeds

### Data
| Setting | Value |
| --- | --- |
| Sample size | 1000 |
| Sample seed | 42 |
| Seed for selecting 20 headlines | 7 |

### Preprocessing (original, used in runs A and B)
| Setting | Value |
| --- | --- |
| Lowercase | yes |
| Token pattern | `(?u)\b[^\W\d_]{2,}\b` (letters only, 2+ characters) |
| Stop words | scikit-learn English list + custom Lithuanian list (in `Stage_2.py`) |
| min_df | 2 |
| max_features | 3000 |
| Empty documents | counted and excluded from fitting and assignment |

### LDA (fixed for all runs)
| Setting | Value |
| --- | --- |
| Learning method | batch |
| max_iter | 15 |
| Model seed | 42 |
| Other parameters | scikit-learn defaults |

### Runs
| Run | Topic count | Preprocessing |
| --- | ---: | --- |
| A | 3 | Original |
| B | 4 | Original |
