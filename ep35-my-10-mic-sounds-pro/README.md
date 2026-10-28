# Auto-fix only the takes you filmed without your mic, from "I Recorded This Without My Mic"

The Short was recorded on my phone's own mic. The cheap handheld mic I hold up in it was not feeding the recording.
What you hear is my "Mic Twin": a small model Claude Code wrote for me that makes my phone-mic voice sound close to my
handheld mic. Close, not identical.

The model itself is in the earlier package: [`../ep34-can-claude-replace-my-mic/mic-twin-brief.md`](../ep34-can-claude-replace-my-mic/mic-twin-brief.md).

This package is the step after it. I film a lot, sometimes with the mic and sometimes without, and I don't want to
sort the files by hand. So before a take goes into editing, a check listens to it, decides "phone mic" or "my mic",
and runs the Mic Twin only on the phone takes. The log line you see in the Short is that check's output for this
take: `"reason": "phone mic"`, `"room_p_mic": 0.027` (a score near 0 means phone, near 1 means mic).

`auto-fix-brief.md` is the brief to hand your coding agent (Claude Code, Codex or similar) to build that check for
your own recordings.

## What you need

- A Mic Twin (or any phone-to-mic fix) that already works for your voice.
- Labelled examples you already have: some takes you know were recorded with your mic, some you know were phone only.
- A computer with an NVIDIA GPU helps; the check itself is light.

## What to expect

- On my own held-out takes the mic takes scored 0.95 or more and the phone takes 0.07 or less, so one cut-off at 0.5
  separates them. Yours will differ: measure it on your takes before you trust it.
- The check also asks "is this my voice?". If someone else is talking, it leaves the take alone, because a Mic Twin
  trained on you would make them sound like you.
- It never edits the original file. It writes a fixed copy with the same video, the same length and the same timing,
  plus one log line per take, so you can always see what it did and why.

Nothing in here needs a password, an account or a paid tool.
