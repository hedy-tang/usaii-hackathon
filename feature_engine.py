import numpy as np

SOURCE_MAP = {"official": 2, "social": 1, "unknown": 0}
CERTAINTY_MAP = {"high": 2, "medium": 1, "low": 0}


def build_features(claims, contradictions, embeddings):

    contradiction_map = {c["claim"]: [] for c in claims}

    for c in contradictions:
        a = c["claim_a"]["claim"]
        b = c["claim_b"]["claim"]
        contradiction_map[a].append(c["contradiction_confidence"])
        contradiction_map[b].append(c["contradiction_confidence"])

    features = []

    for i, c in enumerate(claims):

        scores = contradiction_map.get(c["claim"], [])
        emb = embeddings[i]

        features.append({
            "source_type": SOURCE_MAP.get(c["source_type"], 0),
            "certainty": CERTAINTY_MAP.get(c["certainty"], 1),

            "contradiction_count": len(scores),
            "contradiction_severity": np.mean(scores) if scores else 0.0,

            "embedding_variance": float(np.var(emb)),

            # 🔥 NEW SIGNAL
            "claim_volatility": len(scores) * (np.mean(scores) if scores else 0.0)
        })

    return features