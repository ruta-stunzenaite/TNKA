# Lab 1 — Topic Model

## Setup
1. Place `headlines_train.csv` from Lab01_Materials.zip in `data/`.
2. `python -m venv .venv`, activate, `pip install -r requirements.txt`

## Run
Stage 1 – data preparation and selection of 20 headlines:
   python Stage_1.py

Outputs:
- `outputs/sample_collection.csv` – the document collection used in all runs
- `outputs/initial_20_headlines.csv` – the 20 headlines for the initial analysis

## Parameters and seeds
| Setting | Value |
| --- | --- |
| Sample size | 1000 |
| Sample seed | 42 |
| Seed for selecting 20 headlines | 7 |