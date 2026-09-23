from stage_2 import load_collection, run_lda
from preprocessing import remove_fillers

PROVISIONAL_K = 4

if __name__ == "__main__":
    docs, first20 = load_collection()
    run_lda("C", PROVISIONAL_K, docs, first20, preprocessor=remove_fillers)