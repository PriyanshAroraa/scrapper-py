import requests
import os

def get_search_results(query, max_results=5):
    api_key = os.getenv("GOOGLE_API_KEY")
    cse_id = os.getenv("GOOGLE_CSE_ID")

    if not api_key or not cse_id:
        raise ValueError("Missing GOOGLE_API_KEY or GOOGLE_CSE_ID in .env")

    print(f"🔍 Searching Google for: {query}")
    
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
        "num": max_results
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("items", []):
            link = item.get("link")
            if link:
                results.append(link)

        print(f"✅ Google CSE returned {len(results)} URLs")
        return results

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching search results: {e}")
        return []
