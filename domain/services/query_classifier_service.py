from abc import ABC, abstractmethod


class QueryClassifierService(ABC):
    @abstractmethod
    def predict(self, query: str) -> str:
        """Classify a query into one of the predefined categories."""
        pass
