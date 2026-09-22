# maintainstreak

Daily email digest of LeetCode practice problems, to keep a genuine daily
streak going without a bot auto-submitting on your behalf.

Every day it:
1. Picks 7 problems you haven't been sent before (mix of Easy/Medium, no Hard, via `pick_problems.py`).
2. Writes a detailed explanation for each (intuition, step-by-step approach, complexity, full Python solution) -- done by Claude when this runs as a scheduled agent.
3. Emails the whole thing to you as one digest (`send_digest.py`), so you can read it on your commute and then paste + submit the code yourself.

It does **not** submit anything to LeetCode automatically. You stay the one
clicking submit, which is what keeps your streak/profile meaningful and
keeps this on the right side of LeetCode's anti-bot terms.

## One-time setup

1. **Install dependencies**
   ```bash
   cd /home/thechosenone/maintainstreak
   pip install -r requirements.txt
   ```
   On this machine (Kali, PEP 668 "externally managed environment"), if that
   errors, either use a venv (`python3 -m venv .venv && source .venv/bin/activate`)
   or `pip install --break-system-packages -r requirements.txt`.

2. **Generate a Gmail App Password for your sending account** (set as `SENDER_EMAIL` in `.env`)
   - Turn on 2-Step Verification on that account if it isn't already: https://myaccount.google.com/security
   - Go to https://myaccount.google.com/apppasswords, create an app password (name it e.g. "maintainstreak"), copy the 16-character code.
   - This is **not** the account's normal login password -- it's a separate, revocable credential scoped to SMTP.

3. **Create your `.env`**
   ```bash
   cp .env.example .env
   ```
   Fill in `LEETCODE_USERNAME`, `SENDER_EMAIL`, `RECIPIENT_EMAIL`, and `SMTP_APP_PASSWORD` -- none of these have defaults in `config.py` (this repo may be public, so nothing personal is hardcoded).

4. **Dry run** (does a real fetch + sends a real email, doesn't require the agent):
   ```bash
   python3 pick_problems.py
   ```
   This prints the 7 picked problems and writes `state/problems_today.json`. For a full manual test you'd also need to write `state/email_body.html` yourself and run `python3 send_digest.py` -- but normally both the explanation-writing and the send are done together by the scheduled agent run described below.

## Setting up the daily automation

This project is designed to be driven by a **scheduled Claude Code cloud
routine** (the `schedule` skill) so it runs daily without your laptop needing
to be on. Set one up with a prompt along these lines:

> Run in the repo root. Run `python3 pick_problems.py` to
> fetch today's problems into `state/problems_today.json`. Read that file,
> then for each problem write a detailed, commute-readable explanation:
> intuition/approach, a step-by-step walkthrough, time/space complexity, and
> a full working Python solution. Combine all problems into one clean HTML
> email body and save it to `state/email_body.html`. Then run
> `python3 send_digest.py` to send the digest and update state. Report how
> many problems were sent.

Pick a daily time (default suggestion: 7:30 AM local time, before a commute).
Ask me to set this up via the `schedule` skill and I'll create the routine
with whatever time you want.

## Tuning

All of these live in `.env` (uncomment to override the default in `config.py`):
- `PROBLEM_COUNT` -- how many problems per day (default 7)
- `EASY_RATIO` -- fraction that should be Easy vs Medium (default 0.4 = 40% easy / 60% medium)
- `RECIPIENT_EMAIL` / `SENDER_EMAIL` / `LEETCODE_USERNAME`

## State files (in `state/`)

- `sent_problems.json` -- every problem ever sent, so nothing repeats during the 6-month trial. **Committed to git** -- the cloud routine clones a fresh checkout every run, so this file must live in the repo (not `.gitignore`d) and gets committed + pushed back at the end of every run, or dedup would reset daily.
- `history.log` -- one line per successful send, for auditing the trial over time. Also committed back each run for the same reason.
- `problems_today.json` / `email_body.html` -- today's scratch files (regenerated each run). Git-ignored since they're transient.

**This means the cloud routine's job each day is:** clone repo -> run `pick_problems.py` -> write explanations + `email_body.html` -> run `send_digest.py` -> `git add state/sent_problems.json state/history.log && git commit && git push` so tomorrow's run sees today's state.

## Notes / limitations

- Uses LeetCode's public (undocumented) GraphQL API for problem lists and
  statements -- no login required, but it's unofficial and could change or
  get rate-limited. If `pick_problems.py` starts failing, that's the first
  place to check.
- `sent_problems.json` is the only "have I solved this" tracking -- it
  tracks what *this pipeline has emailed you*, not your real LeetCode solve
  history, so it won't dedupe against problems you solved before starting
  the trial or outside this pipeline.
