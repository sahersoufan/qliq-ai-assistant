from domain.services.query_classifier_service import QueryClassifierService

FAQ_KEYWORDS = ["how", "where", "can i", "help", "guide", "policy", "rules", "refer", "support", "change", "update"]
PRODUCT_KEYWORDS = ["buy", "price", "product", "deal", "recommend", "item", "accessory", "tech", "headphones", "gadget"]
GIG_KEYWORDS = ["gig", "job", "task", "opportunity", "apply", "project", "review", "influencer", "freelance", "sponsorship"]

CATEGORY_PRIORITIES = [
    ("FAQ", FAQ_KEYWORDS),
    ("Product", PRODUCT_KEYWORDS),
    ("Gig", GIG_KEYWORDS)
]


class RuleBasedQueryClassifierService(QueryClassifierService):
    def predict(self, query: str) -> str:
        query = query.lower()
        for label, keywords in CATEGORY_PRIORITIES:
            if any(keyword in query for keyword in keywords):
                return label
        return "General"


if __name__ == "__main__":
    classifier = RuleBasedQueryClassifierService()
    test_queries = [
        "How do I update my password?",
        "Show me trending electronics",
        "What gigs pay over $500?",
        "Hello, what can you do?"
    ]

    for q in test_queries:
        label = classifier.predict(q)
        print(f"Query: {q}\nPredicted (Rule-based): {label}\n")
