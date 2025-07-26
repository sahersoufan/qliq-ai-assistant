def clean_metadata(metadata: dict) -> dict:
    cleaned = {}
    for k, v in metadata.items():
        if isinstance(v, list):
            cleaned[k] = ", ".join(map(str, v))
        elif isinstance(v, (str, int, float, bool)) or v is None:
            cleaned[k] = v
        else:
            cleaned[k] = str(v)
    return cleaned
