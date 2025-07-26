# domain/services/classifier_evaluation_service.py

from typing import List, Literal

Label = Literal["FAQ", "Product", "Gig", "General"]


class ClassifierEvaluationService:
    def __init__(self, ml_classifier, rule_classifier):
        self.ml = ml_classifier
        self.rule = rule_classifier

    def compare(self, queries: List[str]) -> dict:
        results = []
        match_count = 0

        for query in queries:
            ml_label: Label = self.ml.predict(query)
            rule_label: Label = self.rule.predict(query)
            is_match = ml_label == rule_label
            if is_match:
                match_count += 1

            results.append({
                "query": query,
                "ml_label": ml_label,
                "rule_based_label": rule_label,
                "match": is_match
            })

        match_rate = match_count / len(queries) if queries else 0.0

        return {
            "results": results,
            "match_rate": round(match_rate, 4)
        }
