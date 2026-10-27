# What did one video cost in AI? (jamin labs EP29)

In the video I say editing one video costs me about $1 to $1.50 right now, with a goal of $0.10. That number
is my share of flat monthly AI plans, not a bill per token. This folder has the meter I use, so you can count
your own.

`video_cost_meter.py` reads the logs Claude Code already keeps on your computer and adds up every model call
that worked on one video. It prints:

- how many model calls and tokens the video took,
- what that would cost at API list prices,
- and, if you are on a flat plan, your share of that plan for this video.

It only reads files on your machine. Nothing is uploaded. No install: Python 3.8+ standard library.

## Run it

1. Put `video_cost_meter.py` anywhere.
2. Count every session that touched your video's folder (use the folder or file name you work in):

   ```
   python3 video_cost_meter.py --match my-video-folder
   ```

   Or point it at session logs directly (files or folders under `~/.claude/projects/`):

   ```
   python3 video_cost_meter.py ~/.claude/projects/<project>/<session>.jsonl
   ```

3. On a flat plan, add your plan price and how much of this week's limit you have used (type `/usage` in
   Claude Code):

   ```
   python3 video_cost_meter.py --match my-video-folder --plan-monthly 200 --week-used 44
   ```

   Add `--until 2026-10-27T18:00:00+09:00` to stop counting at the moment you finished the video.

## What my numbers look like

- One editing session for a Short (October 26): 170 model calls, about 38M tokens, almost all of them cache
  reads. At API list prices that is $11.93.
- The same kind of work, counted as a share of my monthly plans (one long video plus three Shorts measured on
  October 21): about $1.50 in all.
- So the same video is "about $12 to $21" or "about $1" depending on how you count. Say which one you mean.

## How to read it

- Cost is mostly calls x context size. Each call re-reads the whole conversation, so a session that grows long
  costs more per call. Starting each editing step in a fresh session is the cheapest fix I found.
- The plan share is an estimate: it splits your week's `/usage` percentage by API price. Runs that keep no
  log (`claude -p --no-session-persistence`, scripts) still use your limit but are not in the logs.
- Prices change. The `PRICES` table at the top of the script was checked in October 2026; check
  https://www.anthropic.com/pricing and edit it if needed. Models not in the table are listed as "not priced".
