#!/usr/bin/env python3
"""What did editing one video cost you on flat AI plans? Count it from your plan meters.

  python3 cost_per_edit.py --plan Claude 200 31 33
  python3 cost_per_edit.py --plan Claude 200 31 33 --plan ChatGPT 200 24 25 --videos 2
  python3 cost_per_edit.py --plan Claude 200 31 33 --logs my-video-folder

How it counts:
- A flat plan has a weekly limit. Before you start editing, write down how much of this week's limit you have
  used (Claude Code: type /usage; Codex: /status). Write it down again when the video is done.
- The video's share of the plan = the points you used x the plan's price per week
  (price per month x 12 / 52). Example: a $200 plan is $46.15 a week, so 2 points of the weekly
  limit are $0.92.
- Several videos in the same stretch? Add --videos N and it splits the total.
- --logs TEXT (optional) also reads Claude Code's own session logs on this computer (~/.claude/projects)
  for every session that mentions TEXT (your video's folder or file name) and prints what the same calls
  would cost at API list prices, so you can see both numbers.

It only reads files on this computer. Nothing is sent anywhere. Standard library only (Python 3.8+).
"""
import argparse
import glob
import json
import os
import sys

# US dollars per million tokens: input, cache write, cache read, output. Checked October 2026; check
# https://www.anthropic.com/pricing and edit if they changed. Models not listed are reported as not priced.
PRICES = {
    "claude-opus-5-5": (4.00, 5.00, 0.20, 20.00),
    "claude-sonnet-5-5": (2.00, 2.50, 0.20, 10.00),
}
FIELDS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")
LOGS = os.path.expanduser("~/.claude/projects")


def plan_share(name, monthly, before, after):
    if not (0 <= before <= 100 and 0 <= after <= 100):
        sys.exit(f"{name}: percentages must be 0-100 (got {before} and {after})")
    if after < before:
        sys.exit(f"{name}: the meter went down ({before} -> {after}); the weekly limit probably reset while you "
                 f"worked. Split the job at the reset and add both parts.")
    per_week = monthly * 12 / 52
    used = after - before
    return used, per_week, used / 100 * per_week


def log_files(word):
    hits = set()
    for p in glob.glob(os.path.join(LOGS, "*", "*.jsonl")):
        with open(p, errors="replace") as f:
            if any(word in line for line in f):
                hits.add(p)
                hits.update(glob.glob(os.path.join(p[:-6], "subagents", "*.jsonl")))
    return sorted(hits)


def api_price(files):
    calls = {}
    for p in files:
        with open(p, errors="replace") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                m = d.get("message")
                if d.get("type") == "assistant" and isinstance(m, dict) and m.get("id") and m.get("usage"):
                    calls[m["id"]] = (m.get("model") or "?", m["usage"])  # one call can span several lines
    usd, tokens, unpriced = 0.0, 0, {}
    for model, u in calls.values():
        n = [int(u.get(k) or 0) for k in FIELDS]
        tokens += sum(n)
        price = next((v for k, v in PRICES.items() if model.startswith(k)), None)
        if price is None:
            unpriced[model] = unpriced.get(model, 0) + 1
        else:
            usd += sum(a * b for a, b in zip(n, price)) / 1e6
    return len(calls), tokens, usd, unpriced


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plan", nargs=4, action="append", metavar=("NAME", "USD_PER_MONTH", "BEFORE_%", "AFTER_%"),
                    help="one flat plan: its name, price per month, and the weekly-limit percent before and after")
    ap.add_argument("--videos", type=int, default=1, help="how many videos that stretch of work made (default 1)")
    ap.add_argument("--logs", metavar="TEXT", help="also price the Claude Code sessions that mention TEXT")
    a = ap.parse_args()
    if not a.plan and not a.logs:
        ap.error("give at least one --plan (or --logs)")
    if a.videos < 1:
        ap.error("--videos must be 1 or more")
    total = 0.0
    for name, monthly, before, after in a.plan or []:
        used, per_week, usd = plan_share(name, float(monthly), float(before), float(after))
        total += usd
        print(f"{name}: {used:g} point{'' if used == 1 else 's'} of the weekly limit x ${per_week:,.2f} a week = ${usd:,.2f}")
    if a.plan:
        print(f"plan share for this work: ${total:,.2f}" + (f", ${total / a.videos:,.2f} per video" if a.videos > 1 else ""))
    if a.logs:
        files = log_files(a.logs)
        if not files:
            print(f"no Claude Code session log mentions {a.logs!r}")
        else:
            n, tokens, usd, unpriced = api_price(files)
            print(f"same Claude Code calls at API list prices: {n} calls, {tokens / 1e6:,.1f}M tokens, ${usd:,.2f}"
                  + (f" (${usd / a.videos:,.2f} per video)" if a.videos > 1 else ""))
            if unpriced:
                print(f"  not priced (add them to PRICES): {unpriced}")
    print("Runs that keep no log (scripts, claude -p without a session) still move the meter, so the plan share "
          "counts them and the log price does not.")


if __name__ == "__main__":
    main()
