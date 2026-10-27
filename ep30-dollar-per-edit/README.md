# What does one edited video cost you in AI? (jamin labs EP30)

In the Short I say editing one video costs me somewhere between $1 and $1.50 right now, and I hope to get it to
$0.10. That number is my estimate: a share of my flat monthly AI subscriptions, not a bill per video. This folder
has the counter, so you can work out your own number the same way.

`cost_per_edit.py` turns your plan meters into dollars. You write down how much of your weekly limit you had used
before you started editing a video and again when it was done, and it prints what that slice of the plan cost.

It only reads what you type (and, if you ask, Claude Code's logs on your own computer). Nothing is sent anywhere.
No install: Python 3.8 or newer, standard library only.

## Run it

1. Before you start editing, check your weekly limit: type `/usage` in Claude Code (Codex: `/status`). Note the
   percent used, for example 31.
2. Edit the video. Check again when it is done, for example 33.
3. Run, with your plan's monthly price:

   ```
   python3 cost_per_edit.py --plan Claude 200 31 33
   ```

   ```
   Claude: 2 points of the weekly limit x $46.15 a week = $0.92
   plan share for this work: $0.92
   ```

4. More than one plan worked on it? Add one `--plan` each. Made several videos in that stretch? Add
   `--videos 3` and it splits the total.

   ```
   python3 cost_per_edit.py --plan Claude 200 31 34 --plan ChatGPT 200 24 25 --videos 3
   ```

5. Optional: add `--logs my-video-folder` to also price the same Claude Code calls at API list prices (it reads
   the session logs under `~/.claude/projects` that mention that text).

## How to read it

- The plan share is the honest number if you pay a flat price. The API-list price of the same calls is usually
  10 to 20 times higher (for one of my Shorts it came to about $12 to $21), and you only pay it if you are on the
  API. Say which one you mean when you quote a cost.
- Your meter also moves for other work you do at the same time. Edit in one stretch, or subtract what else ran.
- If the weekly limit resets while you work, the meter goes down; split the job at the reset and add both parts.
- Prices change. The `PRICES` table in the script was checked in October 2026; see
  https://www.anthropic.com/pricing and edit it if needed.
