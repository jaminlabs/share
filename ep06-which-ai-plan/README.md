# Which AI plan fits your work? A 2-minute self-check

From the jamin labs video *Everyone Says a Different AI Plan Is Best. I Pay for All Three.* I pay for the top plan at Claude, ChatGPT and Google, and I check what I actually use. You can do the same check on your own account in about two minutes.

## 1. Find your own usage (official places)

| Plan | Where to look | What you see |
|---|---|---|
| **Claude** (Pro / Max) | claude.ai → **Settings → Usage** ([claude.ai/settings/usage](https://claude.ai/settings/usage)). In Claude Code: `/usage` | Bars for the 5-hour session and the weekly limits, with reset times |
| **ChatGPT / Codex** (Plus / Pro) | The Codex usage dashboard ([chatgpt.com/codex/settings/usage](https://chatgpt.com/codex/settings/usage)). In the Codex CLI: `/status` | % used and reset times for the 5-hour and weekly windows, plus credits. Regular chat has no remaining-usage meter; it only shows a reset time once you hit a limit |
| **Google** (AI Pro / Ultra) | Gemini app → **Settings → Usage limits**. Antigravity CLI: `/usage`. Antigravity app: Settings. Flow: your remaining credits are under your profile, history at [one.google.com/ai/activity](https://one.google.com/ai/activity) | Gemini: limit "refreshes every 5 hours until you reach your weekly limit". Flow: monthly credits |

Sources (checked October 17, 2026): [Claude usage limits](https://support.claude.com/en/articles/9797557), [Claude Code commands](https://code.claude.com/docs/en/commands), [Codex pricing and limits](https://learn.chatgpt.com/docs/pricing), [Gemini usage limits](https://support.google.com/gemini/answer/16275805), [Antigravity `/usage`](https://antigravity.google/docs/cli/commands/usage), [Flow credits](https://support.google.com/flow/answer/16526234).

## 2. Read it as "by the end of the week", not "right now"

A number on Tuesday means nothing without knowing how much of the week has passed. Divide:

**end of week ≈ % used ÷ % of the week gone**

Example from my Google plan: on October 16, 8% used when 48% of the week had gone → about **17%** by the end of the week.

## 3. The rule

**Keep the plan you run out of. Downgrade the plan that ends the week far under its limit.**

- **Claude Max and Google AI Ultra:** the $100 tier has **1/4** of the $200 tier's quota (5x vs 20x the Pro plan, per both companies' plan pages). So if you finish the week under about 20% on the $200 tier, the $100 tier still fits.
- **ChatGPT Pro:** OpenAI doesn't publish the ratio between Pro $100 and Pro $200. Also, new Pro $200 subscriptions that aren't grandfathered already get "a lower usage allowance than previously offered with Pro 200", and eligible older subscribers keep the previous allowance only "through October 29, 2026". Same $200 price. Check your number again after that date.

## 4. Which kind of user are you? (my take)

- **You build with coding agents all day → Claude.** Start at $100. Go up only when you hit the weekly wall two weeks in a row.
- **You make video → Google.** Of these three, it's the only plan with video credits. The $100 tier gives 10,000 Flow credits a month. A full episode cost me about 2,000.
- **Your day is writing, research and planning → ChatGPT.** Chat has its own limit, separate from Codex. $20 may be all you need.
- **You run bots around the clock → put the bulk reading on the plan that sits idle,** and save your best plan for the work that needs it.
- **Just starting → one $20 plan.** Upgrade when you hit the limit, not when a video tells you to.

## 5. My receipts

Measured on my own accounts. Dates fixed so the numbers don't drift.

| Plan | What I pay | Weekly limit used | When |
|---|---:|---|---|
| Claude Max 20x | $200 | **78%**, with 66% of the week gone | Oct 17, 11:28 KST |
| ChatGPT Pro | $200 | **9%**, with 20% of the week gone (42% the week before) | Oct 17, 01:29 KST |
| Google AI Ultra (billed in Korea) | ≈ $224 | **1%** (new week); **8%** with 48% of the week gone on Oct 16 | Oct 17, 11:33 KST |

Claude is the only plan I run out of. Google is the one people call "best value", and it's the one I use least.

## 6. Do the check with one command (optional)

`usage_snapshot.py` reads what Claude Code, Codex and the Antigravity CLI already saved on your computer and prints the end-of-week pace for each. It sends nothing anywhere. It reads undocumented local files, so it may stop working when the tools update. If it does, use the official pages in step 1.

```
python3 usage_snapshot.py          # Claude Code + Codex
python3 usage_snapshot.py --agy    # also asks the Antigravity CLI
```

My output on October 17, 2026:

```
Claude                    79% used ·  68% of the week gone · ~117% by reset · resets Mon 20:59
                       on Max $100 this week would be ~468%: you'd run out
ChatGPT (Codex)            9% used ·  28% of the week gone · ~32% by reset · resets Thu 15:23
Google (Antigravity)       2% used ·   4% of the week gone · too early in the week to tell · resets Sat 07:00
```

Claude and Codex only update these files when you use them. If a number looks old, the script says when it was saved.

## 7. Prices (official, checked October 17, 2026)

| Plan | Price | Source |
|---|---|---|
| Claude Max | $100 (5x Pro) / $200 (20x Pro). Since Oct 7 it includes monthly API credit ($100 / $200). That credit doesn't work in interactive Claude Code and doesn't roll over | [support.claude.com 11049741](https://support.claude.com/en/articles/11049741), [17154008](https://support.claude.com/en/articles/17154008) |
| ChatGPT Pro | $100 / $200 / $500 | [help.openai.com 9793128](https://help.openai.com/en/articles/9793128) |
| Google AI Ultra | $99.99 (5x Pro) / $199.99 (20x Pro). Flow credits 10,000 / 25,000 a month, which don't roll over | [gemini.google/subscriptions](https://gemini.google/us/subscriptions/), [Flow credits](https://support.google.com/flow/answer/16526234) |

Prices and limits change often. Check the source pages before you switch.

---
jamin labs · [youtube.com/@jaminlabs](https://www.youtube.com/@jaminlabs) · I pay for all three plans myself. No sponsor.
