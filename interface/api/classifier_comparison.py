# interface/api/classifier_comparison.py

from fastapi import APIRouter

from domain.services.classifier_evalution_service import ClassifierEvaluationService
from domain.services.rule_based_classifier import RuleBasedQueryClassifierService
from infrastructure.ml.sklearn_query_classifier_service import SklearnQueryClassifierService
from interface.schemas.classifiers_comparison_schema import ComparisonResponse

router = APIRouter()


@router.get("/", response_model=ComparisonResponse)
def compare_classifiers():
    test_queries = [
        "How do I update my profile?",
        "Show me trending electronics",
        "What gigs are available for content creators?",
        "Hello there!",
        "Can I link my social media accounts?",
        "Find me a laptop under $500",
        "Are there writing jobs?",
        "Tell me a joke",
        "Where can I read the refund policy?",
        "Suggest a ring light for creators"
    ]

    evaluation_service = ClassifierEvaluationService(
        ml_classifier=SklearnQueryClassifierService(),
        rule_classifier=RuleBasedQueryClassifierService()
    )

    result = evaluation_service.compare(test_queries)
    return ComparisonResponse(**result)
