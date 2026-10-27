# Blind judge prompt

Paste this into a DIFFERENT model than the one you're testing (I use Codex to judge Claude). Shuffle the answers first
and give them neutral labels (A, B, C…), with your saved "good day" answer mixed in. Keep a private note of which label
is which; don't put dates, model names or run numbers in the prompt.

```text
You are judging several answers to the same task. Judge them blind and independently; do not assume any answer is
better because of its position or label. Do not use tools; answer from the text below.

THE TASK (exactly what the model was asked):
<paste the prompt>

WHAT A GOOD ANSWER MUST DO (my checklist):
1. <the result must ...>
2. <it must not ...>
3. <length / format ...>

ANSWERS:
--- A ---
<answer>
--- B ---
<answer>
--- C ---
<answer>

For every answer give integer scores 1-10:
- correct: does it do what the task asks, with no wrong facts or broken code?
- complete: does it cover everything in my checklist?
- clean: is it free of filler, repeats and made-up details?
- overall: how happy would I be to use it as-is?
Add a note of at most 25 words naming its main strength or flaw. Then rank ALL answers best to worst by overall,
listing every label exactly once.
```

Run it twice with a different shuffle. If the two rankings disagree a lot, the answers are closer than they feel.
