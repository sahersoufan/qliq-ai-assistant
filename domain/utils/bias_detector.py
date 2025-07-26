from collections import Counter
from typing import List, Dict

from infrastructure.logging import logger

def detect_bias(results: List[Dict], field: str, threshold: float = 0.9) -> bool:
    """
    Checks if more than `threshold` proportion of results share the same value for a protected field.
    """
    values = [r.get(field) for r in results if field in r and r[field] is not None]
    if not values:
        return False

    _, count = Counter(values).most_common(1)[0]
    ratio = count / len(values)
    return ratio >= threshold

def get_bias_warnings(results_by_type: Dict[str, List[Dict]]) -> List[str]:
    warnings = []
    for key, results in results_by_type.items():
        for field in ["seller_type", "location", "gender"]:
            if detect_bias(results, field):
                warning = f"{key.title()} biased by {field}"
                warnings.append(warning)
                logger.warning(f"Bias detected: {warning}")
    return warnings
