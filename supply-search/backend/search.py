"""
Powers the "smart search" box on the Supplier Search page.

Two layers, always applied together:

1. Hard filters - exact matches the user picked from dropdowns
   (Profession, Tag, Supplier, Type) are applied first, in SQL/Python,
   with no ambiguity.

2. Free-text query - the "search by description" box. A plain keyword
   is matched directly. But something like "GUI library" won't appear
   verbatim in any row, so before scoring we ask Claude to expand the
   query into a short list of related tags / profession / keywords
   that would plausibly describe that kind of product. Those expanded
   terms are then matched the same way a literal keyword would be,
   so a search for "GUI library" can surface an offering tagged
   Frontend / Software Engineer even though those words never appear
   in the search box.

If ANTHROPIC_API_KEY isn't set, or the API call fails for any reason,
we silently fall back to plain keyword matching on the original query -
the feature degrades gracefully instead of breaking search.
"""

import json
import os
import re

from config import ANTHROPIC_MODEL

_client = None


def _get_client():
    global _client
    if _client is None:
        try:
            import anthropic

            if os.environ.get("ANTHROPIC_API_KEY"):
                _client = anthropic.Anthropic()
            else:
                _client = False
        except Exception:
            _client = False
    return _client or None


def expand_query(query: str, known_tags: list[str], known_professions: list[str]) -> list[str]:
    """
    Ask Claude for extra search terms related to `query`, grounded in the
    tags/professions that actually exist in the data (so it doesn't
    invent tags nobody uses). Returns [] if the API is unavailable.
    """
    client = _get_client()
    if client is None or not query.strip():
        return []

    prompt = f"""A user searched a supplier/product catalog for: "{query}"

Known tags in the catalog: {", ".join(known_tags[:200])}
Known professions in the catalog: {", ".join(known_professions[:50])}

Which of the KNOWN tags/professions above are plausibly relevant to what
the user is looking for? Also list a few extra plain-English keywords
(synonyms, product-category terms) that might appear in a product name
or description for this kind of search.

Respond ONLY with a JSON array of strings, nothing else. Example:
["Frontend", "Software Engineer", "UI toolkit", "widget library"]"""

    try:
        resp = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(b.text for b in resp.content if b.type == "text").strip()
        text = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
        terms = json.loads(text)
        if isinstance(terms, list):
            return [str(t) for t in terms]
    except Exception:
        pass
    return []


def score_offering(offering: dict, terms: list[str]) -> int:
    """Simple count of how many search terms appear in the offering's text fields."""
    haystack = " ".join(
        str(offering.get(f, "")) for f in ("Offering Name", "Type", "Tags", "Supplier Name", "Profession")
    ).lower()
    score = 0
    for term in terms:
        if term.lower() in haystack:
            score += 1
    return score


def rank_offerings(offerings: list[dict], query: str, known_tags: list[str], known_professions: list[str]) -> list[dict]:
    """
    Returns offerings sorted by relevance to `query`. Offerings that match
    on the raw query OR an LLM-expanded term score higher and come first.
    Offerings with zero matches are dropped when a query is present.
    """
    if not query.strip():
        return offerings

    terms = [query] + expand_query(query, known_tags, known_professions)
    scored = [(score_offering(o, terms), o) for o in offerings]
    scored = [(s, o) for s, o in scored if s > 0]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [o for _, o in scored]
