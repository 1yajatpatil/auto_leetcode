#!/usr/bin/env python3
"""Send today's digest email and mark today's problems as sent.

Expects state/problems_today.json (from pick_problems.py) and
state/email_body.html (the full composed HTML digest, containing the
explanations for each problem) to already exist.
"""
import json
import sys
from datetime import date

import config
import state
from emailer import send_email


def main():
    if not config.PROBLEMS_TODAY_FILE.exists():
        sys.exit(f"{config.PROBLEMS_TODAY_FILE} not found -- run pick_problems.py first.")
    if not config.EMAIL_BODY_FILE.exists():
        sys.exit(f"{config.EMAIL_BODY_FILE} not found -- write the composed HTML digest there first.")

    with open(config.PROBLEMS_TODAY_FILE) as f:
        problems = json.load(f)
    with open(config.EMAIL_BODY_FILE) as f:
        html_body = f.read()

    subject = f"LeetCode Daily Practice - {date.today().isoformat()} ({len(problems)} problems)"
    send_email(subject, html_body)

    state.append_sent(problems)
    state.log_history(
        f"Sent digest with {len(problems)} problems: " + ", ".join(p["title"] for p in problems)
    )

    print(f"Sent digest for {len(problems)} problems to {config.RECIPIENT_EMAIL} and updated state.")


if __name__ == "__main__":
    main()
