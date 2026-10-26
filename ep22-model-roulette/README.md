# You pick Opus 5.5. Which model answered? A 10-minute canary you can run yourself (Oct 24, 2026)

In the Short I say what a lot of us feel: you choose Opus 5.5, and you can't see what actually answers. Maybe it's
Sonnet, you never know. That part is my guess, not a fact, and I say on camera there's no way to prove it.

What you *can* do is stop guessing from one bad answer. This folder has the small test I run on my own model:
the same fixed prompts, checked by code, logged every day. If your model changes, the log changes.

## 1. What is actually known (with sources)

| | Source |
|---|---|
| Anthropic says it doesn't make the model worse when it's busy: "To state it plainly: We never reduce model quality due to demand, time of day, or server load." | Anthropic, "A postmortem of three recent issues", Sep 17, 2025: https://www.anthropic.com/research/a-postmortem-of-three-recent-issues |
| Anthropic does send some requests to another model, on purpose and visibly: requests flagged by Opus 5.5's safeguards for higher-risk cybersecurity "can fall back to Opus 4.8", biology or frontier-model development requests "go to Opus 5". | The New Stack, Sep 28, 2026: https://thenewstack.io/claude-sonnet-cyber-safeguards/ |
| In Claude Code, the default model on Pro, Max, Team, Enterprise and the API is Opus 5.5. A switch to a fallback model on overload only happens if you set a fallback chain (`--fallback-model`), and Claude Code shows a notice when it switches. | Claude Code docs, "Model configuration": https://code.claude.com/docs/en/model-config |
| Users do claim routing, in both directions: "Are requests already being routed to a new Opus 5.5 checkpoint…?" (@kimmonismus, Oct 11, 2026) and "wait is it just me or is Opus 5.5 dumber" (@trq212, Oct 24, 2026). Neither is proof. | x.com/kimmonismus/status/2109300315669565612, x.com/rileybrown/status/2113854968511766682 |

## 2. What I found when I tested my own job (Oct 21, 2026)

Someone on X asked if Opus 5.5 had dropped in quality. So I took one real Claude Code job from the day before (my
Shorts picker: it reads a transcript and picks which lines to keep) and re-ran it with the same prompt, the same
input, `claude-opus-5-5`, effort medium: 10 times per input, on two inputs. A second model (Codex) scored all 11
answers per input blind, without knowing which was yesterday's.

- Every run reported `claude-opus-5-5`.
- Yesterday's answer ranked 3.5th and 5th out of 11. No sign of a nerf on that job.
- The same input, sent the same way on the same morning, scored anywhere from **4 to 8 out of 10**.

That last number is the point: one bad answer after a good one is what normal variation looks like.
Full write-up: https://jaminlabs.com/notes/did-opus-5-5-get-nerfed/

## 3. Run your own canary (10 minutes to set up, 1 minute a day)

You need the Claude Code CLI signed in, and Python 3.

1. Download [`canary.py`](canary.py) into an empty folder.
2. Open it and set `MODEL` and `EFFORT` to what you normally use. Leave the prompts alone from now on: the test only
   means something if it never changes.
3. Run it:
   ```
   python3 canary.py run          # 4 fixed prompts x 3 runs, appends to canary.jsonl
   python3 canary.py report       # one line per day
   ```
4. Run it every day at the same time (cron, launchd, or just when you start work).

Every line in `canary.jsonl` records: the time, your CLI version, the model you asked for, **the model IDs the CLI
says it used**, tokens per model, whether the code check passed, and the seconds it took.

**Read it like this:**
- Look at the pass rate and seconds over a week, not one run. Compare today against the spread of earlier days.
- If a model ID you never asked for writes your answers, that's worth a screenshot. A second ID by itself isn't (see
  below).
- If the pass rate drops for several days in a row on the same CLI version, re-run your oldest saved input 5+ times
  before you call it a nerf.
- What it can't do: prove which weights answered. The model ID is what the provider reports. The canary shows you
  changes in behaviour, which is the part you can actually measure.

## 4. My first runs (Oct 24, 2026, 4:43 PM KST, Claude Code 2.1.305, `claude-opus-5-5`, effort low)

- First run: 7 of 8 passed. One answer to "how many r's" came back with its working ("strawberry: r at 3,8,9 → 3 …")
  instead of the number only, so the code check failed it. Same prompt, next run: "6". That's the variation from
  section 2, in miniature.
- Second run (the log in [`example-log-2026-10-24.jsonl`](example-log-2026-10-24.jsonl)): 8 of 8, median 4.5 s.
- Surprise: almost every call listed **two** model IDs, `claude-opus-5-5` and `claude-haiku-5-5`. The token split
  explains it: Opus wrote the answer (5–76 output tokens), and Haiku was a small side call by Claude Code itself
  (~1,200 tokens in, 19–200 out). So a smaller model *does* show up in your usage log, just not as the one answering.
  You only see this if you log it.
