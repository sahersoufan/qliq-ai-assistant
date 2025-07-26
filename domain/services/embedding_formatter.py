def user_to_text(user: dict) -> str:
    return (
        f"{user.get('type', 'Unknown')} interested in "
        f"{', '.join(user.get('interests', []))} aiming to {user.get('goals', 'unknown goals')}"
    )

def product_to_text(product: dict) -> str:
    return (
        f"{product.get('name', 'Unnamed Product')} in category {product.get('category', 'Unknown')}. "
        f"{product.get('description', 'No description.')}"
    )

def gig_to_text(gig: dict) -> str:
    return (
        f"{gig.get('title', 'Untitled Gig')} about {gig.get('description', 'No description')} in "
        f"{gig.get('category', 'Unknown')}. Skills: {', '.join(gig.get('skills_required', []))}"
    )
