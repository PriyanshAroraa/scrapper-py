import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque

def scrape_all_urls(start_urls, max_pages_per_site=5):
    all_text = ""

    for start_url in start_urls:
        visited = set()
        queue = deque([start_url])
        pages_crawled = 0

        while queue and pages_crawled < max_pages_per_site:
            url = queue.popleft()
            if url in visited:
                continue

            try:
                print(f"🔗 Scraping: {url}")
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")

                # Get visible text
                text = soup.get_text(separator=' ', strip=True)
                all_text += f"\n\n🔹 {url}\n{text}\n"

                # Extract internal links
                for a in soup.find_all("a", href=True):
                    link = a["href"]
                    full_url = urljoin(url, link)
                    if full_url.startswith(start_url):
                        queue.append(full_url)

                visited.add(url)
                pages_crawled += 1

            except Exception as e:
                print(f"⚠️ Failed: {url} → {e}")

    return all_text
