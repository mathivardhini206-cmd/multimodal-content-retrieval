import requests


def search_visual(query):
    """
    Search Wikimedia Commons for a relevant image.
    """

    query = query.strip()

    if not query:
        return None

    url = "https://commons.wikimedia.org/w/api.php"

    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": 6,
        "gsrlimit": 1,
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": 600,
        "format": "json"
    }

    response = requests.get(
        url,
        params=params,
        headers={
            "User-Agent": "MultimodalContentUnderstanding/1.0"
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    pages = data.get("query", {}).get("pages", {})

    if not pages:
        return None

    page = next(iter(pages.values()))

    imageinfo = page.get("imageinfo", [])

    if not imageinfo:
        return None

    image = imageinfo[0]

    return {
        "query": query,
        "title": page.get("title", ""),
        "image_url": image.get("thumburl") or image.get("url")
    }