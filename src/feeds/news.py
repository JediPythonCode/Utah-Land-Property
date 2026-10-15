"""Pull local news and flag market-relevant anomalies."""
import feedparser
from datetime import datetime, timedelta, timezone

FEEDS = [
    ("KSL", "https://www.ksl.com/rss"),
    ("Deseret News", "https://www.deseret.com/feeds/rss/"),
    ("SL Tribune", "https://www.sltrib.com/arcio/rss/"),
]

MARKET_KEYWORDS = [
    "interest rate", "fed", "federal reserve", "mortgage",
    "unemployment", "job loss", "layoff", "recession",
    "zoning", "land use", "new construction", "permit",
    "property tax", "tax cap", "affordability", "housing",
    "amazon", "google", "microsoft", "short sale", "foreclosure",
]

def pull_news() -> list[dict]:
    articles = []
    for source, url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:15]:
                articles.append({
                    "title": entry.get("title", ""),
                    "source": source,
                    "when": entry.get("published", ""),
                    "url": entry.get("link", ""),
                })
        except Exception:
            continue
    return articles

def filter_anomalies(articles: list[dict]) -> list[dict]:
    now = datetime.now(timezone.utc)
    anomalies = []
    for a in articles:
        title_low = a["title"].lower()
        if any(kw in title_low for kw in MARKET_KEYWORDS):
            anomalies.append(a)
    return anomalies[:10]
