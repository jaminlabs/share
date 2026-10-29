#!/usr/bin/env python3
"""Before you pay for a tool or a course, see whether someone already gave it away.

    python3 free_clone_finder.py "DataFast"
    python3 free_clone_finder.py "beehiiv" --top 15
    python3 free_clone_finder.py "claude video editor"

Searches public GitHub repositories whose name, description or README mentions the tool (plus the words
"alternative", "open source", "self-hosted" or "free") and prints, for each: stars, license, created and last push
dates, and the link. No account or token needed (GitHub allows about 10 searches a minute without one).
Python 3.8+, standard library only.

What to look at before you trust a result:
- license: MIT or Apache-2.0 means you may use it for free, including at work; "none" means you may not.
- last push: a repo nobody touched in months may not work with today's APIs.
- created: a copy made the same week as the paid launch is often a weekend project.
- stars are popularity, not quality: open the README and try it on something small first.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

API = "https://api.github.com/search/repositories"
HINTS = ["alternative", "open source", "self-hosted", "free"]


def search(query, per_page):
    url = API + "?" + urllib.parse.urlencode({"q": query, "sort": "stars", "order": "desc", "per_page": per_page})
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "User-Agent": "free-clone-finder"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r).get("items", [])


def main():
    ap = argparse.ArgumentParser(description="Find free, open-source alternatives to a paid tool on GitHub.")
    ap.add_argument("tool", help='the paid tool or course topic, e.g. "DataFast"')
    ap.add_argument("--top", type=int, default=10, help="how many repositories to show (default 10)")
    args = ap.parse_args()

    seen, rows = set(), []
    for hint in HINTS:
        q = f'"{args.tool}" "{hint}" in:name,description,readme'
        try:
            items = search(q, min(args.top, 30))
        except Exception as e:  # rate limit or network
            print(f"search '{hint}' failed: {e}", file=sys.stderr)
            continue
        for it in items:
            if it["full_name"] in seen:
                continue
            seen.add(it["full_name"])
            rows.append(it)
    rows.sort(key=lambda it: it.get("stargazers_count", 0), reverse=True)
    if not rows:
        print("Nothing found. Try a shorter name, or the category instead (\"newsletter\", \"web analytics\").")
        return
    print(f"Free / open-source candidates for {args.tool!r} (GitHub, sorted by stars):\n")
    for it in rows[:args.top]:
        lic = (it.get("license") or {}).get("spdx_id") or "none"
        print(f"{it.get('stargazers_count', 0):>7} stars  {lic:<12} created {it['created_at'][:10]}  "
              f"pushed {it['pushed_at'][:10]}  {it['html_url']}")
        if it.get("description"):
            print(f"{'':>15}{it['description'][:110]}")
    print("\nCheck the license and the last push before you build on any of these.")


if __name__ == "__main__":
    main()
