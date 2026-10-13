from app.core.config import settings

CURRENT_HINTS = ("today","current","currently","latest","right now","this week","this year","who is the","who's the","chief minister","prime minister","president of","news","price today","weather","as of 202","result today","score today","recently","updated")

def looks_time_sensitive(text: str) -> bool:
    text = text.casefold()
    return any(h in text for h in CURRENT_HINTS)

def search_web(query: str, limit: int = 5) -> str:
    if not settings.enable_web_search: return ""
    try:
        from ddgs import DDGS
        results = DDGS().text(query, max_results=limit)
        return "\n".join(f"- {x.get('title','')}\n  {x.get('body','')}\n  Source: {x.get('href','')}" for x in results if x.get("title") or x.get("body"))
    except Exception:
        return ""
