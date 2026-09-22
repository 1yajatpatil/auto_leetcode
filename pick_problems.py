#!/usr/bin/env python3
"""Fetch today's batch of LeetCode problems and write them to state/problems_today.json.

Run this first each day. It does NOT mark problems as sent -- that only
happens after send_digest.py successfully emails the digest, so a failed
send doesn't burn through fresh problems.
"""
import json
import sys

import config
import state
from leetcode_api import pick_random_problems


def main():
    excluded = state.load_sent_slugs()
    picked = pick_random_problems(config.PROBLEM_COUNT, config.EASY_RATIO, excluded)

    if len(picked) < config.PROBLEM_COUNT:
        print(
            f"WARNING: only found {len(picked)}/{config.PROBLEM_COUNT} unsent problems "
            f"(pool may be running low after {len(excluded)} already sent).",
            file=sys.stderr,
        )

    enriched = []
    for q in picked:
        enriched.append(
            {
                "titleSlug": q["problem_slug"],
                "title": q["title"],
                "difficulty": q["difficulty"],
                "frontendQuestionId": q.get("frontend_id", ""),
                "link": f"https://leetcode.com/problems/{q['problem_slug']}/",
                "description": q.get("description", ""),
                "examples": q.get("examples", []),
                "constraints": q.get("constraints", []),
                "hints": q.get("hints", []),
                "topics": q.get("topics", []),
            }
        )

    with open(config.PROBLEMS_TODAY_FILE, "w") as f:
        json.dump(enriched, f, indent=2)

    print(f"Picked {len(enriched)} problems -> {config.PROBLEMS_TODAY_FILE}")
    for p in enriched:
        print(f"  [{p['difficulty']}] {p['title']} - {p['link']}")


if __name__ == "__main__":
    main()
