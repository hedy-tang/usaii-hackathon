import pandas as pd

from data_models import CLAIMS, to_dict_list

from embedding_engine import embed_claims
from contradiction_engine import detect_contradictions

from feature_engine import build_features
from confidence_engine import train_confidence_model

from explanation_engine import explain_all_claims

from graph_engine import (
    build_graph,
    get_top_risky_claims,
    summarize_graph
)

from event_engine import build_event_map


# =========================================================
# MAIN PIPELINE
# =========================================================

def run_pipeline():

    print("\n========================================")
    print("CRISIS INFORMATION INTELLIGENCE SYSTEM")
    print("========================================")

    # =====================================================
    # STEP 1 — LOAD CLAIMS
    # =====================================================

    print("\n[1] Loading claims...")

    claims = to_dict_list(CLAIMS)

    print(f"Loaded {len(claims)} claims.")

    # =====================================================
    # STEP 2 — GENERATE EMBEDDINGS
    # =====================================================

    print("\n[2] Generating embeddings...")

    embeddings = embed_claims(claims)

    # attach embeddings to claims
    for i, c in enumerate(claims):
        c["embedding"] = embeddings[i]

    print("Embeddings generated.")

    # =====================================================
    # STEP 3 — DETECT CONTRADICTIONS
    # =====================================================

    print("\n[3] Detecting contradictions...")

    contradictions = detect_contradictions(
        claims,
        embeddings
    )

    print("\n=== CONTRADICTIONS ===")

    if not contradictions:
        print("No contradictions detected.")

    for c in contradictions:

        print(
            f"\n[{c['strength']}]"
            f"\nA: {c['claim_a']['claim']}"
            f"\nB: {c['claim_b']['claim']}"
            f"\nSimilarity: {round(c['similarity'], 3)}"
            f"\nNLI Score: {round(c['nli_score'], 3)}"
            f"\nFinal Score: {round(c['contradiction_confidence'], 3)}"
        )

    # =====================================================
    # STEP 4 — FEATURE ENGINEERING
    # =====================================================

    print("\n[4] Building ML features...")

    features = build_features(
        claims,
        contradictions,
        embeddings
    )

    feature_df = pd.DataFrame(features)

    print("Feature matrix shape:", feature_df.shape)

    # =====================================================
    # STEP 5 — TRAIN CONFIDENCE MODEL
    # =====================================================

    print("\n[5] Training confidence model...")

    model = train_confidence_model(feature_df)

    print("Confidence model trained.")

    # =====================================================
    # STEP 6 — ASSIGN CONFIDENCE SCORES
    # =====================================================

    print("\n[6] Scoring claims...")

    for i in range(len(claims)):

        row = pd.DataFrame([feature_df.iloc[i]])

        score = float(model.predict(row)[0])

        # clamp into probability range
        score = max(0.0, min(1.0, score))
        
        claims[i]["confidence_score"] = float(score)

    # =====================================================
    # STEP 7 — ADD CONTRADICTION COUNTS
    # =====================================================

    print("\n[7] Enriching contradiction metadata...")

    for c in claims:

        count = sum(
            1 for x in contradictions
            if (
                    x["claim_a"]["claim"] == c["claim"]
                    or x["claim_b"]["claim"] == c["claim"]
            )
        )

        c["contradiction_count"] = count

    # =====================================================
    # STEP 8 — PRINT CLAIM SCORES
    # =====================================================

    print("\n=== CLAIM CONFIDENCE SCORES ===")

    for c in claims:

        print(
            f"\nClaim: {c['claim']}"
            f"\nConfidence Score: {round(c['confidence_score'], 3)}"
            f"\nContradictions: {c['contradiction_count']}"
            f"\nSource: {c['source_type']}"
        )

    # =====================================================
    # STEP 9 — GENERATE EXPLANATIONS
    # =====================================================

    print("\n[8] Generating explanations...")

    claims = explain_all_claims(claims)

    print("\n=== EXPLANATIONS ===")

    for c in claims:

        print(f"\nClaim: {c['claim']}")
        print(c["explanation"])

    # =====================================================
    # STEP 10 — BUILD GRAPH
    # =====================================================

    print("\n[9] Building reasoning graph...")

    graph = build_graph(
        claims,
        contradictions
    )

    graph_summary = summarize_graph(graph)

    print("\n=== GRAPH SUMMARY ===")

    for k, v in graph_summary.items():
        print(f"{k}: {v}")

    # =====================================================
    # STEP 11 — TOP RISKY CLAIMS
    # =====================================================

    print("\n=== TOP RISKY CLAIMS ===")

    risky = get_top_risky_claims(graph)

    for node, score in risky:

        print(
            f"\nNode: {node}"
            f"\nRisk Score: {round(score, 3)}"
        )

    # =====================================================
    # STEP 12 — EVENT DETECTION
    # =====================================================

    print("\n=== EVENTS DETECTED ===")

    events = build_event_map(
        claims,
        embeddings
    )

    if not events:
        print("No clustered events detected.")

    for k, v in events.items():

        print(f"\nEvent {k}:")

        for item in v:
            print(" -", item["claim"])

    # =====================================================
    # COMPLETE
    # =====================================================

    print("\n========================================")
    print("PIPELINE COMPLETE")
    print("========================================")

    return {
        "claims": claims,
        "contradictions": contradictions,
        "graph": graph,
        "events": events,
        "model": model
    }


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    run_pipeline()
