
import re
import requests


def search_visual(query):
    """
    Search Wikimedia Commons for a relevant image.
    """

    if not query or not query.strip():
        return None

    # Remove common question words to focus on the topic.
    stop_words = {
        "is", "are", "was", "were", "the", "a", "an",
        "this", "that", "it", "about", "what", "why",
        "how", "in", "of", "for", "to", "with",
        "do", "does", "can", "could", "would",
        "my", "your", "you", "me", "we"
    }

    cleaned_query = re.sub(r"[^\w\s'-]", " ", query)

    keywords = [
        word for word in cleaned_query.split()
        if word.lower() not in stop_words
    ]

    search_query = " ".join(keywords)

    if not search_query:
        search_query = query.strip()

    url = "https://commons.wikimedia.org/w/api.php"

    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": search_query,
        "gsrnamespace": 6,
        "gsrlimit": 10,
        "prop": "imageinfo",
        "iiprop": "url|mime",
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

    # Check multiple results instead of blindly taking the first.
    for page in pages.values():

        imageinfo = page.get("imageinfo", [])

        if not imageinfo:
            continue

        image = imageinfo[0]

        # Ignore PDFs and other non-image files.
        mime_type = image.get("mime", "")

        if not mime_type.startswith("image/"):
            continue

        image_url = (
            image.get("thumburl")
            or image.get("url")
        )

        if not image_url:
            continue

        return {
            "query": search_query,
            "title": page.get("title", ""),
            "image_url": image_url
        }

    return None
