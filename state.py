import json
from datetime import datetime, timezone

import config


def load_sent_slugs():
    if not config.SENT_PROBLEMS_FILE.exists():
        return set()
    with open(config.SENT_PROBLEMS_FILE) as f:
        entries = json.load(f)
    return {e["slug"] for e in entries}


def append_sent(problems):
    entries = []
    if config.SENT_PROBLEMS_FILE.exists():
        with open(config.SENT_PROBLEMS_FILE) as f:
            entries = json.load(f)
    now = datetime.now(timezone.utc).isoformat()
    for p in problems:
        entries.append(
            {"slug": p["titleSlug"], "title": p["title"], "difficulty": p["difficulty"], "sent_at": now}
        )
    with open(config.SENT_PROBLEMS_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def log_history(message):
    now = datetime.now(timezone.utc).isoformat()
    with open(config.HISTORY_LOG_FILE, "a") as f:
        f.write(f"[{now}] {message}\n")
