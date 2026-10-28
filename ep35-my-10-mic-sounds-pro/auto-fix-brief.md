# Brief for your coding agent: fix only the takes filmed without my mic

Paste this to Claude Code, Codex or a similar agent, in the folder where your Mic Twin (or other phone-to-mic fix)
already lives. Replace the parts in brackets.

---

I have a model that makes my phone-mic recordings sound like my own mic: [command or function that turns in.wav into
out.wav]. I film many takes, some with my mic and some on the phone only, and I want a step that runs before editing
and fixes only the phone takes.

Build `fixtake <movie> <out-movie>` that:

1. Extracts the audio of the take (mono, 16 kHz for the checks; keep the original sample rate for the output).
2. Decides "phone mic" or "my mic" with a small classifier you train on my own labelled takes:
   - Phone takes: [folder or list]. Mic takes: [folder or list]. Hold out a few of each for testing.
   - Use a pretrained speech model's embeddings (for example WavLM base plus) averaged over short windows, then a
     simple classifier (logistic regression is fine). Report the held-out scores per take before anything else.
   - Score = probability the take was recorded on my mic. Pick the cut-off from the held-out scores (mine was 0.5,
     with mic takes at 0.95+ and phone takes at 0.07 or less). Tell me if the two groups overlap.
3. Checks that the speaker is me: speaker-verification embedding (for example `microsoft/wavlm-base-plus-sv`) compared
   with my mic takes; if the similarity is under the cut-off you measure on my takes, skip the take.
4. Only for a phone take that is my voice: runs my model, matches the output's speech loudness to the original's,
   keeps the exact start and length (lip sync must not move), and writes `<out-movie>` with the video stream copied
   unchanged and the new audio.
5. Never modifies the original file. Prints one JSON line per take, for example
   `{"action": "fixed" | "skip", "reason": "phone mic" | "mic" | "not my voice", "room_p_mic": 0.03, "voice_cos": 0.93}`,
   and keeps that line next to the output so I can see later why each take was or wasn't changed.
6. Exits 0 for both "fixed" and "skip"; any other exit means "keep the original sound".

Then run it on three takes I name, one mic, one phone, one with another person talking, and show me the three JSON
lines. Do not wire it into anything else until I've listened to the fixed take.

---

Notes from doing this myself:

- My own mic/phone labels came from watching a few frames of each take (is the mic at my mouth?), then the classifier.
  Spot-check its labels the same way before you trust it.
- The scores are a sorting tool, not a quality score. Judge the fixed audio by ear.
