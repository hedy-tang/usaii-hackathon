from typing import List, Dict
from embedding_model import embed_texts


def embed_claims(claims: List[Dict]):
    texts = [c["claim"] for c in claims]
    return embed_texts(texts)