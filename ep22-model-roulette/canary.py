#!/usr/bin/env python3
"""Model canary: send the same small, code-checked prompts to your model every day and log what came back.

You can't see which weights answered a hosted request. You CAN keep a fixed test and watch it over time:
  - which model ID the API reported for every call (Claude Code: `modelUsage` in `claude -p --output-format json`)
  - how many of the fixed checks passed
  - how long each answer took and how many tokens it used

    python3 canary.py run              # 4 prompts x 3 runs, appends to canary.jsonl next to this file
    python3 canary.py run --n 5        # more runs per prompt (more runs = a fairer picture)
    python3 canary.py report           # one line per day: pass rate, models seen, median seconds

Needs the Claude Code CLI (`claude`) signed in. Uses your plan's quota: 4 x 3 short answers per run.
Change MODEL / EFFORT below to what you normally use, then never change the prompts (that is the point).
"""
import datetime as dt
import json
import pathlib
import statistics
import subprocess
import sys
import time

MODEL = "claude-opus-5-5"
EFFORT = "low"
LOG = pathlib.Path(__file__).resolve().parent / "canary.jsonl"

# Fixed prompts with answers code can check. Don't edit them once you start logging.
CHECKS = [
    {"id": "sort",
     "prompt": "Sort these numbers from smallest to largest. Answer with a JSON array only, nothing else: "
               "[42, -7, 3.5, 100, 0, 3.25, -12, 8]",
     "ok": lambda a: json.loads(a.strip().strip("`").removeprefix("json").strip()) == [-12, -7, 0, 3.25, 3.5, 8, 42, 100]},
    {"id": "letters",
     "prompt": "How many times does the letter r appear in the words 'strawberry raspberry'? Answer with the number only.",
     "ok": lambda a: a.strip().rstrip(".") == "6"},
    {"id": "time",
     "prompt": "A train leaves at 09:47 and the trip takes 2 hours 38 minutes. When does it arrive? Answer HH:MM only.",
     "ok": lambda a: a.strip().rstrip(".") == "12:25"},
    {"id": "dates",
     "prompt": "List every date in this text in ISO format (YYYY-MM-DD), in the order they appear, as a JSON array "
               "only: 'We shipped on March 3, 2026, slipped to 04/15/2026 (US format), and closed the ticket on "
               "the 1st of June 2026.'",
     "ok": lambda a: json.loads(a.strip().strip("`").removeprefix("json").strip()) == ["2026-03-03", "2026-04-15", "2026-06-01"]},
]


def ask(prompt):
    args = ["claude", "-p", "--model", MODEL, "--effort", EFFORT, "--output-format", "json",
            "--tools", "", "--no-session-persistence"]
    t0 = time.monotonic()
    r = subprocess.run(args, input=prompt, capture_output=True, text=True, timeout=300)
    secs = round(time.monotonic() - t0, 1)
    if r.returncode:
        return {"error": (r.stderr or r.stdout)[-300:], "seconds": secs}
    resp = json.loads(r.stdout)
    usage = resp.get("modelUsage") or {}
    return {"answer": resp.get("result", ""), "seconds": secs,
            "models": sorted(usage),                                   # the model IDs the CLI says it used
            "canonical": sorted({v.get("canonicalModel", k) for k, v in usage.items()}),
            # tokens per model: which one wrote your answer, which one was a side call
            "tokens": {k: {"in": v.get("inputTokens", 0) + v.get("cacheReadInputTokens", 0)
                                  + v.get("cacheCreationInputTokens", 0), "out": v.get("outputTokens", 0)}
                       for k, v in usage.items()}}


def run(n):
    version = subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip()
    with LOG.open("a") as f:
        for i in range(n):
            for c in CHECKS:
                rec = {"at": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "cli": version,
                       "requested": MODEL, "effort": EFFORT, "check": c["id"], "run": i + 1, **ask(c["prompt"])}
                try:
                    rec["pass"] = "error" not in rec and bool(c["ok"](rec["answer"]))
                except Exception:
                    rec["pass"] = False
                f.write(json.dumps(rec) + "\n")
                print(f'{rec["check"]:8s} run {i + 1}: {"PASS" if rec["pass"] else "FAIL"}  {rec["seconds"]:5.1f}s  '
                      f'models={rec.get("models")}  answer={str(rec.get("answer", rec.get("error")))[:60]!r}')


def report():
    days = {}
    for line in LOG.read_text().splitlines():
        r = json.loads(line)
        days.setdefault(r["at"][:10], []).append(r)
    for day, rs in sorted(days.items()):
        models = sorted({m for r in rs for m in r.get("models", [])})
        secs = [r["seconds"] for r in rs if "error" not in r]
        print(f'{day}  pass {sum(r["pass"] for r in rs)}/{len(rs)}  models {models}  '
              f'median {statistics.median(secs) if secs else 0:.1f}s  errors {sum("error" in r for r in rs)}')


if __name__ == "__main__":
    if sys.argv[1:2] == ["run"]:
        run(int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 3)
    elif sys.argv[1:2] == ["report"]:
        report()
    else:
        print(__doc__)
