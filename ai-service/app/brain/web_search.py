from app.core.config import settings

CURRENT_HINTS = ("today", "current", "currently", "latest", "right now", "this week", "this year", "who is the", "who's the", "chief minister", "prime minister", "president of", "news", "price today", "weather", "as of 202")


def looks_time_sensitive(text: str) -> bool:
    lower = text.casefold()
    return any(hint in lower for hint in CURRENT_HINTS)


def search_web(query: str, limit: int = 5) -> str:
    if not settings.enable_web_search:
        return ""
    try:
        from ddgs import DDGS
        results = DDGS().text(query, max_results=limit)
        snippets = []
        for item in results:
            title, body, href = item.get("title", ""), item.get("body", ""), item.get("href", "")
            if title or body:
                snippets.append(f"- {title}\n  {body}\n  Source: {href}")
        return "\n".join(snippets)
    except Exception:
        return ""
