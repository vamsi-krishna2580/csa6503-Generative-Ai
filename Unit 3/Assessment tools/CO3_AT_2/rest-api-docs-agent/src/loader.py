import os
import re
import json
import requests
from bs4 import BeautifulSoup

from .config import RAW_DATA_PATH


DOCUMENTS = [
    {
        "title": "GitHub REST API Documentation",
        "url": "https://docs.github.com/en/rest",
        "category": "overview",
    },
    {
        "title": "Getting Started with the REST API",
        "url": "https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api",
        "category": "usage",
    },
    {
        "title": "Authenticating to the REST API",
        "url": "https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api",
        "category": "authentication",
    },
    {
        "title": "Keeping API Credentials Secure",
        "url": "https://docs.github.com/en/rest/authentication/keeping-your-api-credentials-secure",
        "category": "authentication",
    },
    {
        "title": "API Versions",
        "url": "https://docs.github.com/en/rest/about-the-rest-api/api-versions",
        "category": "api",
    },
    {
        "title": "Rate Limits for the REST API",
        "url": "https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api",
        "category": "errors",
    },
    {
        "title": "Using Pagination",
        "url": "https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api",
        "category": "usage",
    },
    {
        "title": "Best Practices for Using the REST API",
        "url": "https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api",
        "category": "usage",
    },
    {
        "title": "Troubleshooting the REST API",
        "url": "https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api",
        "category": "errors",
    },
    {
        "title": "Issues REST API",
        "url": "https://docs.github.com/en/rest/issues/issues",
        "category": "endpoints",
    },
    {
        "title": "Repositories REST API",
        "url": "https://docs.github.com/en/rest/repos/repos",
        "category": "endpoints",
    },
    {
        "title": "Pull Requests REST API",
        "url": "https://docs.github.com/en/rest/pulls/pulls",
        "category": "endpoints",
    },
    {
        "title": "Users REST API",
        "url": "https://docs.github.com/en/rest/users/users",
        "category": "endpoints",
    },
    {
        "title": "Organizations REST API",
        "url": "https://docs.github.com/en/rest/orgs/orgs",
        "category": "endpoints",
    },
    {
        "title": "Releases REST API",
        "url": "https://docs.github.com/en/rest/releases/releases",
        "category": "endpoints",
    },
    {
        "title": "Contents REST API",
        "url": "https://docs.github.com/en/rest/repos/contents",
        "category": "endpoints",
    },
    {
        "title": "Branches REST API",
        "url": "https://docs.github.com/en/rest/branches/branches",
        "category": "endpoints",
    },
    {
        "title": "Search REST API",
        "url": "https://docs.github.com/en/rest/search/search",
        "category": "endpoints",
    },
    {
        "title": "GitHub Actions REST API",
        "url": "https://docs.github.com/en/rest/actions",
        "category": "endpoints",
    },
    {
        "title": "Comments REST API",
        "url": "https://docs.github.com/en/rest/issues/comments",
        "category": "endpoints",
    },
]


def clean_text(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(
        ["script", "style", "nav", "footer", "header", "noscript"]
    ):
        tag.decompose()

    main = soup.find("main")

    if main:
        text = main.get_text("\n", strip=True)
    else:
        text = soup.get_text("\n", strip=True)

    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def load_documents():
    os.makedirs(RAW_DATA_PATH, exist_ok=True)

    session = requests.Session()

    session.headers.update(
        {
            "User-Agent": "REST-API-Docs-Agent/1.0",
            "Accept": "text/html",
        }
    )

    documents = []

    for index, document in enumerate(DOCUMENTS, start=1):
        print(
            f"[{index}/{len(DOCUMENTS)}] "
            f"Downloading {document['title']}"
        )

        try:
            response = session.get(
                document["url"],
                timeout=30,
            )

            response.raise_for_status()

            text = clean_text(response.text)

            item = {
                "id": index,
                "title": document["title"],
                "url": document["url"],
                "category": document["category"],
                "content": text,
            }

            documents.append(item)

            filename = os.path.join(
                RAW_DATA_PATH,
                f"{index:02d}.json",
            )

            with open(
                filename,
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    item,
                    file,
                    indent=2,
                    ensure_ascii=False,
                )

            print(f"    Saved {len(text):,} characters")

        except Exception as error:
            print(
                f"    ERROR: {document['title']}: {error}"
            )

    print()
    print(
        f"Successfully loaded {len(documents)} "
        f"of {len(DOCUMENTS)} documents."
    )

    return documents