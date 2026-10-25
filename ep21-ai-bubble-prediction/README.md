# Are you using AI like the top 1%? (Oct 24, 2026)

In the Short I make a prediction: AI money could have a rough few months, and the people who gain are the ones who
build their own system and hand it whole tasks. The 80-90% and top-1% numbers are my guess, not data. This folder
gives you the real numbers behind the Short, a 2-minute self-check, and the project card I actually use to hand
tasks to my AI.

## 1. The numbers behind the Short

| On screen | Source |
|---|---|
| Anthropic: distiller data down 90 to 99% | Anthropic, "Strengthening our defenses against distillation attacks", Oct 12, 2026: "reduced the amount of data harvested by distillers by around 90 to 99%". Same post: "We've turned away meaningful revenue and trillions of tokens' worth of paying traffic from distillers". https://www.anthropic.com/news/distillation-defenses |
| Q1 $4.7B, Q2 $11.6B, Q3 $16.8B (+45%) | What Anthropic told investors on Oct 14, 2026, as reported by Proactive on Yahoo Finance, Oct 16, 2026: "revenue rose 45% from the previous quarter to $16.8 billion in the third quarter"; Q2 "more than doubled to $11.6 billion from $4.7 billion". https://finance.yahoo.com/news/anthropic-ipo-valuation-expectations-cool-134900187.html |
| $2T → $1.5T | Same article: some investors value Anthropic "at about $1.5 trillion … below earlier expectations of $2 trillion, Reuters reported". Investor talk, not a price. |

**Correction:** in the video I say Anthropic's revenue "peaked". It didn't: Q3 revenue went up 45%. What slowed is the
growth rate (Q2 had more than doubled). The screen shows the real numbers.

## 2. Self-check: one point per "yes" (2 minutes)

1. You have written down, in one file, what your AI should know about a project (goal, where things live, rules).
2. You hand the AI a whole task ("build it, test it, tell me when it's done"), not one question at a time.
3. Every task has a written way to check it is done, and the AI runs that check before it reports back.
4. You have a list of things the AI must never do without asking you (spend money, publish, delete, send).
5. At least one job runs on a schedule without you starting it.
6. You know roughly what your AI costs per month and what one finished task costs.
7. When the AI makes the same mistake twice, you write the fix into its instructions so it doesn't happen a third time.

0-2: chat user. 3-5: getting there. 6-7: you're building a system.

## 3. The card I give my AI for every project

[`AGENTS-template.md`](AGENTS-template.md) is the shape of the card every one of my projects has (Claude Code and
Codex read it before they work). Copy it into a project folder as `AGENTS.md` (Claude Code: add a `CLAUDE.md` with the
line `@AGENTS.md`), fill in the brackets, and start your next task with "read AGENTS.md first".

The two sections that matter most: **"How to check it's done"** (the AI runs it and reports the result, failures
included) and **"Never without asking me"**.
