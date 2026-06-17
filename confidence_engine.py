# =========================================================
# RULE-BASED CONFIDENCE ENGINE
# =========================================================

# Replaces RandomForest + synthetic labels
# with deterministic scoring logic.


# =========================================================
# SINGLE CLAIM SCORE
# =========================================================

def compute_confidence(claim):

    score = 0.5

    # ============================================
    # SOURCE TYPE
    # ============================================

    source = claim.get(
        "source_type",
        "unknown"
    )

    if source == "official":

        score += 0.25

    elif source == "news":

        score += 0.1

    elif source == "social":

        score -= 0.1

    # ============================================
    # CERTAINTY
    # ============================================

    certainty = claim.get(
        "certainty",
        "low"
    )

    if certainty == "high":

        score += 0.15

    elif certainty == "medium":

        score += 0.05

    else:

        score -= 0.05

    # ============================================
    # CONTRADICTIONS
    # ============================================

    contradiction_count = claim.get(
        "contradiction_count",
        0
    )

    score -= (
            contradiction_count * 0.12
    )

    # ============================================
    # CONTRADICTION SEVERITY
    # ============================================

    contradiction_severity = claim.get(
        "contradiction_severity",
        0.0
    )

    score -= (
            contradiction_severity * 0.15
    )

    # ============================================
    # CLAMP SCORE
    # ============================================

    score = max(
        0.0,
        min(1.0, score)
    )

    return round(score, 3)


# =========================================================
# SCORE ALL CLAIMS
# =========================================================

def score_claims(claims):

    enriched = []

    for claim in claims:

        claim["confidence_score"] = (
            compute_confidence(claim)
        )

        enriched.append(claim)

    return enriched