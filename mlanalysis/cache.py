from functools import lru_cache

# NOTE: model is injected from outside (IMPORTANT DESIGN FIX)
_nli_model = None


def set_nli_model(model):
    """
    Inject transformer pipeline once.
    """
    global _nli_model
    _nli_model = model


@lru_cache(maxsize=20000)
def cached_nli_call(text_a: str, text_b: str):

    global _nli_model

    if _nli_model is None:
        raise ValueError(
            "NLI model not initialized. Call set_nli_model() first."
        )

    # symmetry
    if text_a > text_b:
        text_a, text_b = text_b, text_a

    result = _nli_model({
        "text": text_a,
        "text_pair": text_b
    })

    # transformers compatibility fix
    if isinstance(result, list):
        result = result[0]

    label = result["label"].lower()
    score = float(result["score"])

    if "contradiction" in label:
        return score

    return 0.0
