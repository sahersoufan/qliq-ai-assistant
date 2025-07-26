from infrastructure.vector_db.product_store import build_product_store
from infrastructure.vector_db.gig_store import build_gig_store
from infrastructure.vector_db.user_store import build_user_store

# Load once on startup
product_store = build_product_store()
gig_store = build_gig_store()
# user_store = build_user_store()  # Optional, for future user-to-user recs
