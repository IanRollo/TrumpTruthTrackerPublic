import feedparser
from main_local import analyze_by_category, categorize
from email.utils import parsedate_to_datetime
import json
import os

FEED_URL = "https://trumpstruth.org/feed"

def backfill_posts():
    print("Backfilling 100 posts to local output...")

    feed = feedparser.parse(FEED_URL)
    entries = feed.entries[:100]
    backfilled = []

    for entry in entries:
        post_content = str(entry.title).strip()
        if post_content.startswith("[No Title]"):
            post_content = "Video/Image Post"
        link = entry.link
        timestamp = parsedate_to_datetime(entry.published)

        category_result = categorize(post_content)
        categories = category_result.get("categories", [])
        subcategories = category_result.get("subcategories", [])

        if not categories:
            continue

        alert_dict = analyze_by_category(post_content, categories)
        entry_data = {
            "post_content": post_content,
            "link": link,
            "timestamp": timestamp.isoformat(),
            "filtered": not any(result.get("notify") for result in alert_dict.values()),
            "categories": categories,
            "subcategories": subcategories,
            "notifications": {k: v["notify"] for k, v in alert_dict.items()},
            "reasons": {k: v.get("reason", "") for k, v in alert_dict.items()}
        }
        backfilled.append(entry_data)

    if not os.path.exists("output"):
        os.makedirs("output")
    with open("output/latest_posts.json", "w", encoding="utf-8") as f:
        json.dump(backfilled, f, indent=2)
    print("Backfilled data written to output/latest_posts.json")

if __name__ == "__main__":
    backfill_posts()
