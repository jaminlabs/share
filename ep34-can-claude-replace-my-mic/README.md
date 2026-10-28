# Mic Twin recipe, from "Can Claude Replace My Mic?"

I film a lot of takes on my phone without my handheld mic. So I asked Claude Code to build a small model that makes
my phone-mic recordings sound like my own mic. It took one day. The take in this Short was recorded on the phone's
mic only (the mic in my hand wasn't feeding it), and the voice you hear in it is that model's output.

`mic-twin-brief.md` is the brief to hand your coding agent (Claude Code, Codex or similar) so it can build the same
thing for your voice. It's the approach that worked for me, in the order it worked.

## What you need

- Your own recordings, two sets: takes recorded with your mic, and takes recorded with only your phone. I used what I
  already had: about two hours with the mic and about 40 minutes on the phone, all my own voice. You don't need the
  same sentences on both, and you don't need to record anything new if you already film a lot.
- A computer with an NVIDIA GPU. The main model trained in about two minutes on mine; the slow part is preparing the
  data.
- Open models only (WavLM for speech features, a HiFi-GAN vocoder). No account or paid API is needed for the audio
  itself; the coding agent just writes and runs the code on your machine.

## What to expect

- It's close to my mic, not identical. On test clips it never saw, a mic-vs-phone classifier trained on my own takes
  rated the output 84-95 % "mic" (a real mic scored 100 %). A few words get a slight warble.
- It works for one voice (yours) and one target sound (your mic). It is not a general "studio voice" filter, and that's
  why it still sounds like you.
- It can change a word now and then, so check captions against what you actually said.
- Judge it by ear. I made a side-by-side listening video (phone, cleanup, model, real mic) and picked the version that
  sounded most natural, not the one with the best score.

Nothing in here needs a password, an account or a paid tool.
