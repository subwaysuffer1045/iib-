from slugify import slugify as _slugify
import uuid

def make_slug(text: str) -> str:
    base = _slugify(text, max_length=200, word_boundary=True)
    if not base:
        base = "item"
    return f"{base}-{str(uuid.uuid4())[:8]}"

def make_company_slug(name: str) -> str:
    return _slugify(name, max_length=200, word_boundary=True) or f"company-{str(uuid.uuid4())[:8]}"
