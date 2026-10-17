#!/usr/bin/env python3
"""Where am I on my AI plans this week? One snapshot for Claude, ChatGPT/Codex and Google (Antigravity).

Reads what your own tools already saved on this computer. Nothing is sent anywhere.
These are undocumented local files, so they can change without notice. If a line says
"not found", use the official usage page listed in README.md instead.

    python3 usage_snapshot.py          # Claude + Codex
    python3 usage_snapshot.py --agy    # also asks the Antigravity CLI (`agy -p /usage`)

The useful number is "by reset at this pace": used % divided by how much of the week
has passed. 8% used when 48% of the week is gone means about 17% by the end of the week.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import subprocess

WEEK = dt.timedelta(days=7)
# Next tier down has 1/4 of the quota: Claude Max $200 = 20x Pro, $100 = 5x Pro;
# Google AI Ultra $199.99 = 20x Pro, $99.99 = 5x Pro (official plan pages, Oct 17, 2026).
# OpenAI doesn't publish a ratio between ChatGPT Pro $200 and $100, so no hint for it.
TIER_DOWN = {"Claude": ("Max $100", 4), "Google (Antigravity)": ("Ultra $100", 4)}


def now():
    return dt.datetime.now(dt.timezone.utc)


def find(obj, key):
    """First value stored under `key` anywhere inside nested dicts/lists."""
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        obj = list(obj.values())
    if isinstance(obj, list):
        for v in obj:
            hit = find(v, key)
            if hit is not None:
                return hit
    return None


def row(plan, used, resets, window=WEEK, seen=None):
    left = resets - now()
    passed = max(0.0, min(1.0, 1 - left / window))
    pace = used / passed if passed >= 0.05 else None
    out = {"plan": plan, "used": used, "passed": passed * 100, "resets": resets, "pace": pace, "hint": "", "seen": seen}
    if pace is not None and plan in TIER_DOWN:
        name, ratio = TIER_DOWN[plan]
        fits = pace * ratio
        out["hint"] = (f"on {name} this week would be ~{fits:.0f}%: " +
                       ("it would fit" if fits < 80 else "too tight" if fits < 100 else "you'd run out"))
    return out


def claude():
    path = os.path.expanduser("~/.claude.json")
    try:
        data = json.load(open(path)).get("cachedUsageUtilization") or {}
    except (OSError, ValueError):
        return None
    week = (data.get("utilization") or data).get("seven_day")
    if not week or week.get("utilization") is None:
        return None
    seen = dt.datetime.fromtimestamp(data["fetchedAtMs"] / 1000, dt.timezone.utc) if data.get("fetchedAtMs") else None
    return row("Claude", float(week["utilization"]), dt.datetime.fromisoformat(week["resets_at"]), seen=seen)


def codex():
    files = sorted(glob.glob(os.path.expanduser("~/.codex/sessions/*/*/*/rollout-*.jsonl")), key=os.path.getmtime)
    for path in reversed(files[-20:]):
        last = None
        with open(path, errors="replace") as f:
            for line in f:
                if '"rate_limits"' in line:
                    last = line
        try:
            event = json.loads(last) if last else None
        except ValueError:
            continue
        prim = (find(event, "rate_limits") or {}).get("primary") if event else None
        if not prim or prim.get("used_percent") is None:
            continue
        window = dt.timedelta(minutes=prim.get("window_minutes") or 10080)
        resets = dt.datetime.fromtimestamp(prim["resets_at"], dt.timezone.utc)
        stamp = event.get("timestamp")
        seen = dt.datetime.fromisoformat(stamp.replace("Z", "+00:00")) if stamp else None
        return row("ChatGPT (Codex)", float(prim["used_percent"]), resets, window, seen=seen)
    return None


def antigravity():
    try:
        res = subprocess.run(["agy", "-p", "/usage"], capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.TimeoutExpired):
        return None
    m = re.search(r"Gemini Models\s+Weekly Limit Remaining\s+(\d+)%\s+(\S+)", res.stdout)
    if not m:
        return None
    resets = dt.datetime.fromisoformat(m.group(2).replace("Z", "+00:00"))
    return row("Google (Antigravity)", 100 - float(m.group(1)), resets, seen=now())


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--agy", action="store_true", help="also run `agy -p /usage` (Google AI Pro/Ultra)")
    a = ap.parse_args()
    checks = [("Claude", claude), ("ChatGPT (Codex)", codex)] + ([("Google (Antigravity)", antigravity)] if a.agy else [])
    print(f"Snapshot {dt.datetime.now().astimezone():%Y-%m-%d %H:%M %Z}\n")
    for name, fn in checks:
        r = fn()
        if not r:
            print(f"{name:22} not found (open the official usage page, see README.md)")
            continue
        pace = f"~{r['pace']:.0f}% by reset" if r["pace"] is not None else "too early in the week to tell"
        print(f"{name:22} {r['used']:5.0f}% used · {r['passed']:3.0f}% of the week gone · {pace}"
              f" · resets {r['resets'].astimezone():%a %H:%M}")
        if r["seen"] and now() - r["seen"] > dt.timedelta(hours=1):
            print(f"{'':22} (last saved {r['seen'].astimezone():%a %H:%M}; use the tool once to refresh)")
        if r["hint"]:
            print(f"{'':22} {r['hint']}")
    print("\nRule of thumb: keep the plan you run out of. A plan that ends the week far under its limit is a downgrade candidate.")


if __name__ == "__main__":
    main()
