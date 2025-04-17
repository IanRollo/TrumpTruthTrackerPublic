import feedparser
from openai import OpenAI
import json
import datetime
import logging
import os
from email.utils import parsedate_to_datetime

logging.basicConfig(level=logging.INFO)

def categorize(post_content):
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    with open("categorizeinstructions.txt", "r", encoding="utf-8") as file:
        category_prompt = file.read()
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": category_prompt}]},
            {"role": "user", "content": [{"type": "input_text", "text": post_content}]}
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "category_tags",
                "strict": False,
                "schema": {
                    "type": "object",
                    "properties": {
                        "categories": {"type": "array", "items": {"type": "string"}},
                        "subcategories": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["categories"]
                }
            }
        },
        reasoning={}, tools=[], temperature=0.7, max_output_tokens=512, top_p=1, store=True
    )
    return json.loads(response.output_text)

def analyze_by_category(post_content, categories):
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    results = {}
    for category in categories:
        filename = f"Instructions/{category}.txt"
        if not os.path.exists(filename):
            continue
        with open(filename, "r", encoding="utf-8") as file:
            instructions = file.read()
        response = client.responses.create(
            model="gpt-4o",
            input=[
                {"role": "system", "content": [{"type": "input_text", "text": instructions}]},
                {"role": "user", "content": [{"type": "input_text", "text": post_content}]}
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": f"alert_{category}",
                    "strict": False,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "notify": {"type": "boolean"},
                            "reason": {"type": "string"},
                            "summary": {"type": "string"},
                            "title": {"type": "string"}
                        },
                        "required": ["notify", "reason", "summary", "title"]
                    }
                }
            },
            reasoning={}, tools=[], temperature=1, max_output_tokens=2048, top_p=1, store=True
        )
        try:
            output = json.loads(response.output_text)
            results[category] = output
        except Exception:
            continue
    return results

def main():
    feed = feedparser.parse("https://trumpstruth.org/feed")
    latest_entry = feed.entries[0]
    post_content = latest_entry.title if not latest_entry.title.startswith("[No Title]") else "Video/Image Post"
    post_link = latest_entry.link
    timestamp = parsedate_to_datetime(latest_entry.published)

    category_result = categorize(post_content)
    categories = category_result.get("categories", [])
    subcategories = category_result.get("subcategories", [])

    alert_dict = analyze_by_category(post_content, categories)
    entry = {
        "post_content": post_content,
        "link": post_link,
        "timestamp": timestamp.isoformat(),
        "filtered": not any(result.get("notify") for result in alert_dict.values()),
        "categories": categories,
        "subcategories": subcategories,
        "notifications": {k: v["notify"] for k, v in alert_dict.items()},
        "reasons": {k: v.get("reason", "") for k, v in alert_dict.items()}
    }

    if not os.path.exists("output"):
        os.makedirs("output")
    with open("output/latest_posts.json", "w", encoding="utf-8") as f:
        json.dump([entry], f, indent=2)
    print("Post analysis saved to output/latest_posts.json")

if __name__ == "__main__":
    main()
