import networkx as nx
from sklearn.cluster import DBSCAN
import numpy as np


def build_event_clusters(embeddings, eps=0.7):

    clustering = DBSCAN(
        eps=eps,
        min_samples=1,
        metric="cosine"
    )

    labels = clustering.fit_predict(embeddings)

    return labels


def build_event_map(claims, embeddings):

    labels = build_event_clusters(embeddings)

    events = {}

    for i, label in enumerate(labels):

        if label == -1:
            continue

        if label not in events:
            events[label] = []

        events[label].append(claims[i])

    return events
