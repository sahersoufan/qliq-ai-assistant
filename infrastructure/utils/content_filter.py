# infrastructure/utils/content_filter.py

import re

from transformers import pipeline

# Load once at module level
classifier = pipeline("text-classification", model="unitary/toxic-bert", top_k=None)

TOXIC_LABELS = {"toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"}

THRESHOLD = 0.5


def is_clean_text(text: str) -> bool:
    """
    Returns False if toxic-bert detects any toxic content above threshold.
    """
    predictions = classifier(text)[0]  # Output is list of dicts
    for pred in predictions:
        if pred['label'] in TOXIC_LABELS and pred['score'] > THRESHOLD:
            return False
    return True


def sanitize_text(text: str) -> str:
    """
    Basic sanitization to remove profane/inappropriate phrases or symbols.
    """
    text = re.sub(r"\b(fuck|shit|bitch|asshole)\b", "****", text, flags=re.IGNORECASE)
    text = re.sub(r"[<>]{1,}", "", text)  # Remove HTML-like tags if any
    return text.strip()
