from pathlib import Path
import joblib
from domain.services.query_classifier_service import QueryClassifierService


class SklearnQueryClassifierService(QueryClassifierService):
    def __init__(self):
        base_dir = Path(__file__).resolve().parents[2]
        model_path = base_dir / "infrastructure" / "ml" / "query_classifier_model.pkl"
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at: {model_path}")
        self.pipeline = joblib.load(model_path)

    def predict(self, query: str) -> str:
        return self.pipeline.predict([query])[0]


if __name__ == "__main__":
    classifier = SklearnQueryClassifierService()
    test_query = "How do I change my password?"
    label = classifier.predict(test_query)
    print(f"Predicted label: {label}")