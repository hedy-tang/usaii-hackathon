# =========================================================
# DETERMINISTIC EXPLANATION ENGINE
# =========================================================

# No LLMs
# No hallucinations
# Fast + explainable


# =========================================================
# SINGLE EXPLANATION
# =========================================================

def explain_claim(claim):

    reasons = []

    # ============================================
    # SOURCE QUALITY
    # ============================================

    source = claim.get("source_type", "unknown")

    if source == "official":
        reasons.append(
            "Official source increases reliability."
        )

    elif source == "news":
        reasons.append(
            "News source provides moderate reliability."
        )

    elif source == "social":
        reasons.append(
            "Social media source is less reliable."
        )

    else:
        reasons.append(
            "Unknown source credibility."
        )

    # ============================================
    # CERTAINTY
    # ============================================

    certainty = claim.get("certainty", "low")

    if certainty == "high":
        reasons.append(
            "Claim reported with high certainty."
        )

    elif certainty == "medium":
        reasons.append(
            "Claim reported with moderate certainty."
        )

    else:
        reasons.append(
            "Claim reported with low certainty."
        )

    # ============================================
    # CONTRADICTIONS
    # ============================================

    contradiction_count = claim.get(
        "contradiction_count",
        0
    )

    if contradiction_count == 0:

        reasons.append(
            "No contradictions detected."
        )

    elif contradiction_count <= 2:

        reasons.append(
            f"Contradicted by {contradiction_count} related claims."
        )

    else:

        reasons.append(
            f"Strong conflict detected across {contradiction_count} claims."
        )

    # ============================================
    # TRUST LEVEL
    # ============================================

    score = claim.get(
        "confidence_score",
        0
    )

    if score >= 0.8:
        trust = "HIGH"

    elif score >= 0.6:
        trust = "MEDIUM"

    else:
        trust = "LOW"

    # ============================================
    # BUILD FINAL OUTPUT
    # ============================================

    explanation = (
            f"Trust Level: {trust}\n\n"
            + "\n".join(
        f"• {r}" for r in reasons
    )
    )

    return explanation


# =========================================================
# BATCH ENRICHMENT
# =========================================================

def explain_all_claims(claims):

    enriched = []

    for c in claims:

        explanation = explain_claim(c)

        enriched.append({
            **c,
            "explanation": explanation
        })

    return enriched