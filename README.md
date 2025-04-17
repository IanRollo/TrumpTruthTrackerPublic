# TrumpTruthTracker (Local Version)

This tool analyzes Donald Trump's Truth Social posts, categorizes them by topic, and determines whether each post warrants attention based on structured instructions. This version runs entirely locally and outputs results to disk. Please note - This package is to demonstrate how the categorization and analysis features work, and allow you to use them for your own purposes. However, the actual working package contains a lot more stuff than here, which has to be omitted here for security reasons. Therefore, this repo probably won't really be maintained.

---

## 🔍 Features

- Parses Trump's latest posts from [https://trumpstruth.org](https://trumpstruth.org)
- Categorizes posts into multiple topic areas using OpenAI
- Evaluates whether each post is likely to be noteworthy ("notify")
- Saves all analysis results to local JSON files
- Includes a backfill mode for reviewing historical posts

---

## 🛠️ Setup

### Requirements

- Python 3.10+
- An OpenAI API key (required for classification)

### Installation

```bash
git clone https://github.com/yourusername/TrumpTruthTracker.git
cd TrumpTruthTracker
pip install -r requirements.txt
```

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=sk-...
```

---

## 🚀 Usage

### Analyze the Most Recent Post

```bash
python main.py
```

This will:
- Fetch the most recent post from Trump's feed
- Categorize it using `Instructions/*.txt`
- Write the result to `output/latest_posts.json`

---

### Backfill 100 Posts

```bash
python backfill_local.py
```

This will:
- Parse the latest 100 posts from the RSS feed
- Classify each and generate a full archive in `output/latest_posts.json`

---

## 📁 Project Structure

```
TrumpTruthTracker/
├── Instructions/             # Categorization logic per category
├── output/                   # Where results are saved locally
├── main_local.py             # Analyze the most recent post
├── backfill_local.py         # Analyze the latest 100 posts
├── categorizeinstructions.txt
└── README.md                 # This file
```

---

## 💡 Notes

- This repo does not send emails, store user data, or connect to any external backend.
- All categorization is done using OpenAI API calls.
- Use this for educational, research, or hobbyist analysis.

---

## 📖 License

MIT-ish. Use it, remix it, launch a rocket with it. Like NASA though, not the Houthis.
