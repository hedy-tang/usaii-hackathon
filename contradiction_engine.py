import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

from config import *
from cache import cached_nli_call, set_nli_model


# ONLY NLI MODEL HERE
nli = pipeline(
    "text-classification",
    model="facebook/bart-large-mnli"
)

set_nli_model(nli)


def get_nli_score(a, b):
    return cached_nli_call(a, b)

# =========================================================
# MAIN ENGINE
# =========================================================

def detect_contradictions(claims, embeddings):

    contradictions = []
    sim = cosine_similarity(embeddings)
    n = len(claims)

    for i in range(n):
        for j in range(i + 1, n):

            a, b = claims[i], claims[j]

            if a["entity"] != b["entity"]:
                continue

            similarity = float(sim[i][j])
            nli_score = get_nli_score(a["claim"], b["claim"])

            # smart pruning
            # require claims to actually be about the same thing
            if similarity < 0.55:
                continue

            final = (
                    similarity * 0.6 +
                    nli_score * 0.4
            )

            if final >= FINAL_CONTRADICTION_THRESHOLD:

                contradictions.append({
                    "claim_a": a,
                    "claim_b": b,
                    "similarity": similarity,
                    "nli_score": nli_score,
                    "contradiction_confidence": final,
                    "strength": "HIGH" if final > 0.75 else "MEDIUM"
                })

    return contradictions