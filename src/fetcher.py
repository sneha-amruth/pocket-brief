"""
Fetches raw stories from RSS feeds and Reddit.
Returns a dict of { section: [{ title, summary, url, source }] }
"""

import feedparser
import praw
import os
from datetime import datetime, timedelta, timezone

# ─── Source config ────────────────────────────────────────────────────────────

RSS_SOURCES = {
    "geopolitics": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://www.thehindu.com/news/international/feeder/default.rss",
        "https://feeds.feedburner.com/ndtvnews-top-stories",
        "https://theprint.in/feed/",
    ],
    "ai_tech": [
        "https://techcrunch.com/feed/",
        "https://www.theverge.com/rss/index.xml",
        "https://www.wired.com/feed/rss",
        "https://venturebeat.com/feed/",
        "https://www.technologyreview.com/feed/",
        "https://lobste.rs/rss",
        "https://news.ycombinator.com/rss",
    ],
    "worth_knowing": [
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://feeds.feedburner.com/ndtvnews-top-stories",
    ],
}

REDDIT_SOURCES = {
    "geopolitics": ["geopolitics", "worldnews", "CredibleDefense", "india", "economics"],
    "ai_tech": ["MachineLearning", "artificial", "programming", "technology"],
    "worth_knowing": ["todayilearned", "science"],
}


# ─── Fetchers ─────────────────────────────────────────────────────────────────

def fetch_rss(url: str, hours: int = 24) -> list[dict]:
    """Fetch stories from a single RSS feed published in the last `hours` hours."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    stories = []
    feed = feedparser.parse(url)
    for entry in feed.entries:
        published = entry.get("published_parsed")
        if published:
            pub_dt = datetime(*published[:6], tzinfo=timezone.utc)
            if pub_dt < cutoff:
                continue
        stories.append({
            "title": entry.get("title", "").strip(),
            "summary": entry.get("summary", "").strip(),
            "url": entry.get("link", ""),
            "source": feed.feed.get("title", url),
        })
    return stories


def fetch_reddit(reddit: praw.Reddit, subreddit: str, limit: int = 10) -> list[dict]:
    """Fetch top posts from a subreddit over the past 24 hours."""
    stories = []
    for post in reddit.subreddit(subreddit).top(time_filter="day", limit=limit):
        stories.append({
            "title": post.title.strip(),
            "summary": post.selftext[:300].strip() if post.selftext else "",
            "url": post.url,
            "source": f"r/{subreddit}",
        })
    return stories


def deduplicate(stories: list[dict]) -> list[dict]:
    """Remove stories with duplicate URLs, keeping the first occurrence."""
    seen = set()
    unique = []
    for story in stories:
        url = story.get("url", "")
        if url and url not in seen:
            seen.add(url)
            unique.append(story)
    return unique


def fetch_all() -> dict[str, list[dict]]:
    """Fetch all sources, deduplicate within each section, and return raw stories."""
    results: dict[str, list[dict]] = {
        "geopolitics": [],
        "ai_tech": [],
        "worth_knowing": [],
    }

    # RSS
    for section, urls in RSS_SOURCES.items():
        for url in urls:
            try:
                stories = fetch_rss(url)
                results[section].extend(stories)
                print(f"[fetcher] {section} — {len(stories):>3} stories from {url}")
            except Exception as e:
                print(f"[fetcher] RSS failed ({url}): {e}")

    # Reddit — only runs if credentials are present in the environment
    reddit_id = os.environ.get("REDDIT_CLIENT_ID")
    reddit_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    if reddit_id and reddit_secret and not reddit_id.startswith("your-"):
        try:
            reddit = praw.Reddit(
                client_id=reddit_id,
                client_secret=reddit_secret,
                user_agent=os.environ.get("REDDIT_USER_AGENT", "pocket-brief/1.0"),
            )
            for section, subreddits in REDDIT_SOURCES.items():
                for sub in subreddits:
                    try:
                        stories = fetch_reddit(reddit, sub)
                        results[section].extend(stories)
                        print(f"[fetcher] {section} — {len(stories):>3} stories from r/{sub}")
                    except Exception as e:
                        print(f"[fetcher] Reddit failed (r/{sub}): {e}")
        except Exception as e:
            print(f"[fetcher] Reddit client failed: {e}")
    else:
        print("[fetcher] Reddit credentials not set — skipping Reddit sources")

    # Deduplicate within each section by URL
    for section in results:
        before = len(results[section])
        results[section] = deduplicate(results[section])
        dupes = before - len(results[section])
        if dupes:
            print(f"[fetcher] {section} — removed {dupes} duplicate(s)")

    return results


# ─── Standalone test ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    print("=" * 50)
    print("PHASE 1 — Fetching raw stories")
    print("=" * 50 + "\n")

    raw = fetch_all()

    print()
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    for section, stories in raw.items():
        print(f"\n[{section.upper()}] {len(stories)} stories")
        for s in stories[:5]:  # preview first 5
            print(f"  • {s['title'][:80]} ({s['source']})")
        if len(stories) > 5:
            print(f"  ... and {len(stories) - 5} more")
