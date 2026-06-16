from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


# =========================================================
# MODEL SETUP
# =========================================================

MODEL_NAME = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

device = "cuda" if torch.cuda.is_available() else "cpu"

model = model.to(device)
model.eval()


# =========================================================
# PROMPT BUILDER
# =========================================================

def build_prompt(claim):

    return f"""
You are a crisis intelligence analyst.

Analyze the claim below.

Return EXACTLY 3 bullet points:

- reliability assessment
- contradiction analysis
- risk interpretation

Claim: {claim.get('claim')}

Confidence Score: {round(claim.get('confidence_score', 0), 3)}

Contradiction Count: {claim.get('contradiction_count', 0)}

Source Type: {claim.get('source_type')}
"""


# =========================================================
# SINGLE EXPLANATION
# =========================================================

def explain_claim(claim):

    prompt = build_prompt(claim)

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(device)

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=120,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )

    explanation = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
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
