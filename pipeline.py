from data_models import CLAIMS, to_dict_list

from embedding_engine import embed_claims
from contradiction_engine import detect_contradictions

from confidence_engine import score_claims

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
    # STEP 4 — ENRICH CONTRADICTION METADATA
    # =====================================================

    print("\n[4] Enriching contradiction metadata...")

    for c in claims:

        related = [
            x for x in contradictions
            if (
                    x["claim_a"]["claim"] == c["claim"]
                    or x["claim_b"]["claim"] == c["claim"]
            )
        ]

        c["contradiction_count"] = len(related)

        if related:

            avg_severity = sum(
                x["contradiction_confidence"]
                for x in related
            ) / len(related)

            c["contradiction_severity"] = round(
                avg_severity,
                3
            )

        else:

            c["contradiction_severity"] = 0.0

    # =====================================================
    # STEP 5 — COMPUTE CONFIDENCE SCORES
    # =====================================================

    print("\n[5] Computing confidence scores...")

    claims = score_claims(claims)

    # =====================================================
    # STEP 6 — PRINT CLAIM SCORES
    # =====================================================

    print("\n=== CLAIM CONFIDENCE SCORES ===")

    for c in claims:

        print(
            f"\nClaim: {c['claim']}"
            f"\nConfidence Score: {round(c['confidence_score'], 3)}"
            f"\nContradictions: {c['contradiction_count']}"
            f"\nContradiction Severity: {round(c['contradiction_severity'], 3)}"
            f"\nSource: {c['source_type']}"
        )

    # =====================================================
    # STEP 7 — GENERATE EXPLANATIONS
    # =====================================================

    print("\n[6] Generating explanations...")

    claims = explain_all_claims(claims)

    print("\n=== EXPLANATIONS ===")

    for c in claims:

        print(f"\nClaim: {c['claim']}")
        print(c["explanation"])

    # =====================================================
    # STEP 8 — BUILD GRAPH
    # =====================================================

    print("\n[7] Building reasoning graph...")

    graph = build_graph(
        claims,
        contradictions
    )

    graph_summary = summarize_graph(graph)

    print("\n=== GRAPH SUMMARY ===")

    for k, v in graph_summary.items():
        print(f"{k}: {v}")

    # =====================================================
    # STEP 9 — TOP RISKY CLAIMS
    # =====================================================

    print("\n=== TOP RISKY CLAIMS ===")

    risky = get_top_risky_claims(graph)

    for node, score in risky:

        print(
            f"\nNode: {node}"
            f"\nRisk Score: {round(score, 3)}"
        )

    # =====================================================
    # STEP 10 — EVENT DETECTION
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
        "events": events
    }


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    run_pipeline()