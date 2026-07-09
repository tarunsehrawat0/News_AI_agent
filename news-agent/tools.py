import os
from datetime import datetime
from typing import List

import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

NEWSAPI_URL = "https://newsapi.org/v2/everything"


def fetch_latest_india_news() -> List[dict]:
    """Fetch the latest five India articles from NewsAPI."""
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        raise ValueError("Missing NEWSAPI_KEY in .env")

    params = {
        "q": 'India',
        "language": "hi",
        "sortBy": "publishedAt",
        "pageSize": 9,
        "apiKey": api_key,
    }
    response = requests.get(NEWSAPI_URL, params=params, timeout=20)
    response.raise_for_status()
    articles = response.json().get("articles", [])

    cleaned_articles = []
    for article in articles[:5]:
        cleaned_articles.append(
            {
                "title": article.get("title", "Untitled article"),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "publishedAt": article.get("publishedAt", ""),
            }
        )
    return cleaned_articles


def summarize_article(article: dict) -> str:
    """Create a short 2-3 line summary for one article using OpenAI."""
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-5")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY in .env")

    client = OpenAI(api_key=api_key)
    prompt = (
        "Summarize this AI news article in 2-3 short lines for a daily email. "
        "Keep it clear, neutral, and beginner-friendly. "
        "Make sure to include the most important information."
        "Send accurate information and avoid speculation. "
        "Use bullet points.\n\n"
        f"Title: {article.get('title', '')}\n"
        f"Description: {article.get('description', '')}\n"
        f"Link: {article.get('url', '')}"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def today_string() -> str:
    return datetime.now().strftime("%B %d, %Y")
