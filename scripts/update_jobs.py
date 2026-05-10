import json
import re
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup

MARKETING_KEYWORDS = [
    "marketing", "communication", "comunicazione", "social media",
    "digital", "content", "brand", "media", "copywriter", "crm",
    "ufficio stampa", "public relations", "eventi", "advertising"
]

DEGREE_KEYWORDS = [
    "laurea triennale", "laurea", "bachelor", "economia",
    "scienze della comunicazione", "marketing", "comunicazione"
]

JOB_HINTS = [
    "job",
    "jobs",
    "career",
    "careers",
    "lavora",
    "posizioni aperte",
    "offerte lavoro",
    "vacancy",
    "recruiting",
    "candidati",
]

EXCLUDED_KEYWORDS = [
    "bilancio",
    "comunicato",
    "news",
    "obbligazioni",
    "investitori",
    "media",
    "press",
    "finanziari",
    "risultati",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 JobWatchItaliaBot/1.0"
}


def load_sources():
    with open("sources.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("sources", [])


def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()


def is_probable_job_link(text, href):
    combined = f"{text} {href}".lower()
    return any(k in combined for k in JOB_HINTS)


def is_relevant(text):
    lower = text.lower()

    if any(k in lower for k in EXCLUDED_KEYWORDS):
        return False

    marketing = any(k in lower for k in MARKETING_KEYWORDS)
    degree = any(k in lower for k in DEGREE_KEYWORDS)
    job = any(k in lower for k in JOB_HINTS)

    return job and (marketing or degree)


def infer_category(text):
    lower = text.lower()
    if any(k in lower for k in MARKETING_KEYWORDS):
        return "marketing"
    if any(k in lower for k in DEGREE_KEYWORDS):
        return "triennale"
    return "generale"


def scrape_source(source):
    company = source["name"]
    start_url = source["url"]

    found = []
    visited = set()
    to_visit = [start_url]

    for _ in range(2):  # profondità leggera
        next_urls = []

        for url in to_visit:
            if url in visited:
                continue

            visited.add(url)

            try:
                res = requests.get(url, headers=HEADERS, timeout=20)
                if res.status_code >= 400:
                    continue
            except Exception:
                continue

            soup = BeautifulSoup(res.text, "html.parser")

            for a in soup.find_all("a", href=True):
                title = clean(a.get_text(" "))
                href = a["href"]
                full_url = urljoin(url, href)

                if not title or len(title) < 4:
                    continue

                parsed_start = urlparse(start_url)
                parsed_full = urlparse(full_url)

                if parsed_start.netloc not in parsed_full.netloc:
                    continue

                if is_probable_job_link(title, full_url):
                    next_urls.append(full_url)

                text_blob = f"{title} {full_url}"

                if is_probable_job_link(title, full_url) and is_relevant(text_blob):
                    found.append({
                        "title": title[:120],
                        "company": company,
                        "location": "Italia / da verificare",
                        "degree": "Possibile triennale / da verificare",
                        "url": full_url,
                        "category": infer_category(text_blob)
                    })

            time.sleep(1)

        to_visit = list(set(next_urls))[:15]

    return found


def deduplicate(jobs):
    seen = set()
    result = []

    for job in jobs:
        key = job["url"]
        if key not in seen:
            seen.add(key)
            result.append(job)

    return result


def main():
    sources = load_sources()
    all_jobs = []

    for source in sources:
        print(f"Scraping {source['name']}...")
        all_jobs.extend(scrape_source(source))

    all_jobs = deduplicate(all_jobs)

    output = {
        "updated_at": datetime.utcnow().isoformat(),
        "jobs": all_jobs
    }

    with open("data/jobs.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(all_jobs)} jobs")


if __name__ == "__main__":
    main()
