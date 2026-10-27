#!/usr/bin/env python3
"""What did one video cost in AI? Reads Claude Code's own session logs and adds up every model call.

  python3 video_cost_meter.py --match my-video-folder
  python3 video_cost_meter.py --match my-video-folder --plan-monthly 200 --week-used 44
  python3 video_cost_meter.py path/to/session.jsonl other-session-folder/

It only reads files. Nothing is sent anywhere. Standard library only (Python 3.8+).

How it counts:
- Claude Code writes one JSONL file per session under ~/.claude/projects/<folder>/ (helpers it starts
  live in <session>/subagents/*.jsonl). One API call can appear on several lines, so each message id is
  counted once.
- "API price" = the tokens times the list price per million tokens in PRICES below. Check the current
  prices at https://www.anthropic.com/pricing and edit the table if they changed.
- On a flat monthly plan you don't pay per token. --plan-monthly and --week-used turn the API price into
  your share of the plan: this video's API price / everything you ran in the 7 days before it ended
  x the share of your weekly limit you used (Claude Code's /usage) x the plan's price per week.
  Runs that keep no log (claude -p --no-session-persistence) are not counted.
"""
import argparse
import datetime
import glob
import json
import os
import sys

# US dollars per million tokens: input, cache write (5 min), cache read, output. Checked October 2026.
PRICES = {
    "claude-opus-5-5": (4.00, 5.00, 0.20, 20.00),
    "claude-sonnet-5-5": (2.00, 2.50, 0.20, 10.00),
}
FIELDS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")
LOGS = os.path.expanduser("~/.claude/projects")


def stamp(s):
    try:
        return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


def files_in(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            out += glob.glob(os.path.join(p, "**", "*.jsonl"), recursive=True)
        elif p.endswith(".jsonl"):
            out.append(p)
    return sorted(set(out))


def read_calls(path, until=None):
    """{message id: (model, usage, time)} for one log file."""
    calls = {}
    with open(path, errors="replace") as f:
        for line in f:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            m = d.get("message")
            if d.get("type") != "assistant" or not isinstance(m, dict):
                continue
            t = stamp(d.get("timestamp"))
            if until and t and t > until:
                continue
            if m.get("id") and m.get("usage"):
                calls[m["id"]] = (m.get("model") or "?", m["usage"], t)
    return calls


def mentions(path, word):
    with open(path, errors="replace") as f:
        return any(word in line for line in f)


def sessions_matching(word):
    """Session logs that mention `word` (a folder or file name), plus their helpers' logs."""
    hits = set()
    for p in glob.glob(os.path.join(LOGS, "*", "*.jsonl")):
        if mentions(p, word):
            hits.add(p)
            hits.update(glob.glob(os.path.join(p[:-6], "subagents", "*.jsonl")))
    return sorted(hits)


def add_up(calls):
    tokens = {k: 0 for k in FIELDS}
    usd, unpriced = 0.0, {}
    for model, u, _ in calls.values():
        n = [int(u.get(k) or 0) for k in FIELDS]
        for k, v in zip(FIELDS, n):
            tokens[k] += v
        price = next((v for k, v in PRICES.items() if model.startswith(k)), None)
        if price is None:
            unpriced[model] = unpriced.get(model, 0) + 1
            continue
        usd += sum(a * b for a, b in zip(n, price)) / 1e6
    return tokens, usd, unpriced


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="session .jsonl files or folders (default: search with --match)")
    ap.add_argument("--match", help="count every session whose log mentions this text, e.g. your video's folder name")
    ap.add_argument("--until", help="ignore calls after this time, e.g. 2026-10-27T18:00:00+09:00 (when you hit upload)")
    ap.add_argument("--plan-monthly", type=float, help="your plan's price per month in USD, e.g. 200")
    ap.add_argument("--week-used", type=float, help="percent of your weekly limit used, from /usage, e.g. 44")
    a = ap.parse_args()
    files = files_in(a.paths) if a.paths else (sessions_matching(a.match) if a.match else [])
    if not files:
        sys.exit("No session logs found. Pass log files/folders, or --match <text that appears in the session>.")
    until = stamp(a.until) if a.until else None
    calls = {}
    for p in files:
        calls.update(read_calls(p, until))
    tokens, usd, unpriced = add_up(calls)
    times = sorted(t for _, _, t in calls.values() if t)
    print(f"sessions read: {len(files)}   model calls: {len(calls)}")
    if times:
        print(f"from {times[0]:%Y-%m-%d %H:%M} to {times[-1]:%Y-%m-%d %H:%M} UTC")
    for k in FIELDS:
        print(f"  {k:<28} {tokens[k] / 1e6:8.2f} M")
    print(f"API price (list prices in PRICES): ${usd:,.2f}")
    if unpriced:
        print(f"  not priced (add them to PRICES): {unpriced}")
    if a.plan_monthly and a.week_used and times:
        start = times[-1] - datetime.timedelta(days=7)
        week = {}
        for p in glob.glob(os.path.join(LOGS, "**", "*.jsonl"), recursive=True):
            if os.path.getmtime(p) < start.timestamp():
                continue
            week.update({k: v for k, v in read_calls(p, times[-1]).items() if v[2] and v[2] >= start})
        _, week_usd, _ = add_up(week)
        per_week = a.plan_monthly * 12 / 52
        if week_usd > 0:
            share = usd / week_usd * a.week_used / 100
            print(f"your 7 days before it: ${week_usd:,.2f} at API price; this video = {usd / week_usd:.1%} of that")
            print(f"share of your plan: {share:.2%} of a week's limit = ${share * per_week:,.2f} "
                  f"(plan ${a.plan_monthly:,.0f}/month = ${per_week:,.2f}/week)")


if __name__ == "__main__":
    main()
