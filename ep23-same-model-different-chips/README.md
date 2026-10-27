# Is my AI having a bad day? A 20-minute re-run test (Oct 24, 2026)

In the Short I say the same Claude model felt worse at times, back when Anthropic was serving it on different chips:
"sometimes very bad, sometimes okay". That's my experience, not proof. This folder gives you what Anthropic actually
wrote about it, and the test I now run before I believe "it got dumber": the same task, re-run, scored blind.

## 1. What Anthropic wrote (Sep 17, 2025)

"A postmortem of three recent issues", https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues

- "Between August and early September, three infrastructure bugs intermittently degraded Claude's response quality."
- "We deploy Claude across multiple hardware platforms, namely AWS Trainium, NVIDIA GPUs, and Google TPUs."
- Two of the three bugs were on the TPU side: "On August 25, we deployed a misconfiguration to the Claude API TPU
  servers that caused an error during token generation", and a sampling change that "triggered a latent bug in the
  XLA:TPU compiler". The third, a context-window routing error, was not TPU-specific.
- "The same prompt might work perfectly on one request and fail on the next."
- "These initial reports were difficult to distinguish from normal variation in user feedback."
- "To state it plainly: We never reduce model quality due to demand, time of day, or server load."

**Correction:** in the video I say the difference was because the model "was not optimized for TPUs". Anthropic's
postmortem says the cause was bugs (a TPU server misconfiguration and a TPU compiler bug, plus a routing error), not a
missing optimization. I also wasn't sure which model or year it was; the postmortem's dated bugs hit Sonnet 4, Opus 4
and 4.1, Haiku 3.5 and possibly Opus 3, in August and September 2025.

## 2. My own test: did Opus 5.5 get worse overnight? (Oct 21, 2026)

People on X were asking if Opus 5.5 got worse, so I re-ran one of my real jobs: the step where Claude picks a Short out
of my raw talking take. Same saved input, same prompt, same model and effort as the day before, 10 runs. A second
model (Codex) scored all 11 drafts blind: shuffled, no labels, no dates.

| | Take 1 | Take 2 |
|---|---|---|
| Yesterday's draft, blind rank | 3.5 of 11 | 5 of 11 |
| Today's 10 re-runs, scores out of 10 | 3 to 4.5 | 4 to 8 |

Yesterday's draft landed in the middle of today's runs. The same input, run 10 times on the same day, varied more
(4 to 8 out of 10) than yesterday differed from today. One bad answer feels like a nerf; ten answers tell you the
spread. Limits: one task type, a short structured job, one judge model.

## 3. Run it on your own work (about 20 minutes)

1. **Save a real task the day it works well**: the exact prompt and input in one file, the model name, and the answer
   you liked. Without yesterday's input you can't compare anything.
2. **Re-run it 5 times when it "feels worse"**: [`rerun.sh`](rerun.sh) runs one saved prompt N times with the
   Claude Code CLI and keeps every answer (works the same with any CLI that reads a prompt from stdin; swap the line).
3. **Check what you can with code first**: does it compile, do the tests pass, is the JSON valid, is it the length you
   asked for. Count passes per run.
4. **Score blind with a second model**: paste your saved good answer and the new ones, shuffled and unlabeled, into
   [`blind-judge-prompt.md`](blind-judge-prompt.md). Use a different model than the one you're testing.
5. **Compare against the spread, not one run**: if your old answer ranks in the middle of the new ones, it's normal
   variation. If it beats all 5, write it in [`bad-day-log.md`](bad-day-log.md) with the date and time, and report it.

## 4. If it really is worse, tell them

From the same postmortem: "You can use the /bug command in Claude Code or you can use the 'thumbs down' button in the
Claude apps". Anthropic says user reports with specific examples helped them find these bugs. A saved prompt, its old
answer and five new ones is exactly that kind of example.

Files: `rerun.sh` (the re-run loop), `blind-judge-prompt.md` (the scoring prompt), `bad-day-log.md` (a log to copy).
