from sentence_transformers import SentenceTransformer

# =========================================================
# SINGLE SOURCE OF TRUTH FOR EMBEDDINGS
# =========================================================

_model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding_model():
    return _model


def embed_texts(texts):
    return _model.encode(texts, convert_to_numpy=True)
