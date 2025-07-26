from pathlib import Path
import joblib
from domain.services.query_classifier_service import QueryClassifierService
from infrastructure.logging import logger


class SklearnQueryClassifierService(QueryClassifierService):
    def __init__(self):
        try:
            base_dir = Path(__file__).resolve().parents[2]
            model_path = base_dir / "infrastructure" / "ml" / "query_classifier_model.pkl"
            
            if not model_path.exists():
                logger.error(f"Model file not found at: {model_path}")
                raise FileNotFoundError(f"Model not found at: {model_path}")
            
            try:
                self.pipeline = joblib.load(model_path)
                logger.info("Query classifier model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load model from {model_path}: {str(e)}")
                raise RuntimeError(f"Failed to load model: {str(e)}")
        except Exception as e:
            logger.error(f"Error initializing query classifier service: {str(e)}")
            raise

    def predict(self, query: str) -> str:
        try:
            if not query or not isinstance(query, str):
                logger.warning(f"Invalid query input: {query}")
                return "General"  # Default to General category for invalid inputs
                
            result = self.pipeline.predict([query])[0]
            logger.debug(f"Query classified as: {result}")
            return result
        except Exception as e:
            logger.error(f"Error predicting query classification: {str(e)}")
            logger.error(f"Query that caused the error: {query}")
            return "General"  # Fallback to General category on error


if __name__ == "__main__":
    classifier = SklearnQueryClassifierService()
    test_query = "How do I change my password?"
    label = classifier.predict(test_query)
    print(f"Predicted label: {label}")