from typing import Dict

from langchain_community.embeddings import SentenceTransformerEmbeddings

from domain.services.embedding_formatter import user_to_text
from domain.services.store_registery import product_store, gig_store
from infrastructure.repositories.user_repo_json import load_user_by_id


def recommend(user_id: str, top_k: int = 5) -> Dict[str, list]:
    user = load_user_by_id(user_id)
    if not user:
        return {"error": [f"User '{user_id}' not found."]}

    # Embed user profile
    user_text = user_to_text(user)
    embedder = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    user_vector = embedder.embed_documents([user_text])[0]

    # Search top_k similar items
    similar_products = product_store.similarity_search_by_vector(user_vector, k=top_k)
    similar_gigs = gig_store.similarity_search_by_vector(user_vector, k=top_k)

    # Return only basic fields for response
    return {
        "products": [doc.metadata for doc in similar_products],
        "gigs": [doc.metadata for doc in similar_gigs],
        "users": []  # Optional future feature
    }
