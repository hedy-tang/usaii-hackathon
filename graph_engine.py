import networkx as nx
from collections import defaultdict


# =========================================================
# BUILD GRAPH (WEIGHTED)
# =========================================================

def build_graph(claims, contradictions):

    G = nx.Graph()

    # -----------------------------
    # Add nodes
    # -----------------------------
    for c in claims:
        node_id = f"{c['entity']}::{c['claim']}"

        G.add_node(
            node_id,
            claim=c["claim"],
            entity=c.get("entity"),
            confidence=c.get("confidence_score", 0.0),
            source=c.get("source_type"),
            contradiction_count=c.get("contradiction_count", 0),
        )

    # -----------------------------
    # Add weighted edges
    # -----------------------------
    for c in contradictions:

        a = f"{c['claim_a']['entity']}::{c['claim_a']['claim']}"
        b = f"{c['claim_b']['entity']}::{c['claim_b']['claim']}"

        weight = c.get("contradiction_confidence", 0.0)

        G.add_edge(
            a,
            b,
            relation="CONTRADICTION",
            weight=weight,
            similarity=c.get("similarity", 0.0),
            nli_score=c.get("nli_score", 0.0),
        )

    return G


# =========================================================
# RISK PROPAGATION (CORE UPGRADE)
# =========================================================

def compute_risk_scores(G):

    risk = {}

    for node in G.nodes():

        edges = G.edges(node, data=True)

        # local contradiction pressure
        local_risk = 0.0
        degree = 0

        for _, _, data in edges:
            if data.get("relation") == "CONTRADICTION":
                local_risk += data.get("weight", 0.0)
                degree += 1

        avg_local_risk = local_risk / degree if degree > 0 else 0.0

        risk[node] = avg_local_risk

    return risk


# =========================================================
# GLOBAL IMPORTANCE (PAGE RANK STYLE)
# =========================================================

def compute_influence_scores(G):

    # use contradiction weight as influence signal
    pr = nx.pagerank(G, weight="weight")

    return pr


# =========================================================
# FINAL RANKING (MOST IMPORTANT CLAIMS)
# =========================================================

def get_top_risky_claims(G, top_k=10):

    risk = compute_risk_scores(G)
    influence = compute_influence_scores(G)

    combined = []

    for node in G.nodes():

        combined_score = (
                0.6 * risk.get(node, 0.0) +
                0.4 * influence.get(node, 0.0)
        )

        combined.append((node, combined_score))

    combined.sort(key=lambda x: x[1], reverse=True)

    return combined[:top_k]


# =========================================================
# GRAPH SUMMARY
# =========================================================

def summarize_graph(G):

    return {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "avg_degree": sum(dict(G.degree()).values()) / max(G.number_of_nodes(), 1),
    }