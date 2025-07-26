from typing import Dict

from langchain_community.embeddings import SentenceTransformerEmbeddings

from domain.services.audit_service import log_activity
from domain.services.embedding_formatter import user_to_text
from domain.services.store_registery import product_store, gig_store
from domain.utils.bias_detector import get_bias_warnings
from infrastructure.repositories.user_repo_json import load_user_by_id


def recommend(user_id: str, top_k: int = 5) -> Dict[str, list]:
    # Log recommendation request
    log_activity(user_id, "recommendation_request", {"top_k": top_k})
    
    user = load_user_by_id(user_id)
    if not user:
        log_activity(user_id, "recommendation_error", {"error": f"User '{user_id}' not found."})
        return {"error": [f"User '{user_id}' not found."]}

    # Embed user profile
    user_text = user_to_text(user)
    embedder = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    user_vector = embedder.embed_documents([user_text])[0]

    # Search top_k similar items
    similar_products = product_store.similarity_search_by_vector(user_vector, k=top_k)
    similar_gigs = gig_store.similarity_search_by_vector(user_vector, k=top_k)

    # Detect bias
    bias_warnings = get_bias_warnings({"products": similar_products, "gigs": similar_gigs})

    # Prepare results
    results = {
        "products": [doc.metadata for doc in similar_products],
        "gigs": [doc.metadata for doc in similar_gigs],
        "users": [],  # Optional future feature
        "bias_warnings": bias_warnings
    }
    
    # Log recommendation results
    log_activity(user_id, "recommendation_results", {
        "product_count": len(similar_products),
        "gig_count": len(similar_gigs),
        "bias_warnings_count": len(bias_warnings)
    })
    
    return results
