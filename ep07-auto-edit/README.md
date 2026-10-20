# Talk to your phone, let your agent edit (jamin labs EP07)

Video, transcript and numbers: [jaminlabs.com/v/phone-to-edited-video](https://jaminlabs.com/v/phone-to-edited-video/?src=github)

What this is: the recipe my agent follows to turn phone clips into a finished cut with captions, cards and a review, plus the prompt I give it. You can run it with your own coding agent (Claude Code, Codex, or anything that can run commands) on your own computer.

How long: setting it up with an agent takes an afternoon. After that, one edit is "send the clips, type one message, watch the result".

What it does not do: it doesn't publish. I watch the cut and say yes before anything goes up. It also doesn't start by itself yet: I type the message that starts it.

## My numbers (Oct 17, 2026, this episode)
- Filmed: 8 clips, 18 min 31 s of me talking, outdoors and indoors, between 13:38 and 14:04.
- Phone to computer: the 8 clips (1.2 GB) reached my Linux PC at 14:26, two minutes after they landed on my Mac.
- Transcribed all 8 clips 14:30 to 14:36. Gemini watched 19 one-minute pieces 14:43 to 14:45. 14 claims fact-checked by 14:46 (1 false, cut).
- One thing broke: the Gemini strategy call answered in 65 seconds and then hung for 37 minutes on exit. Fix below (step 8).
- Before agents, a 5-6 minute video took me about 4 hours to edit by hand.

## The recipe

### 1. Get the clips onto the computer without touching them
- Send the files from the phone to any folder the computer can see: AirDrop to a Mac, Taildrop (Tailscale), Syncthing, a synced cloud folder.
- A small job runs every minute (cron, a systemd timer, or launchd) and moves new videos into an inbox folder.
- Only move a file when its size is the same on two checks in a row. Otherwise you grab a half-copied video.
- Make an edit copy right away. iPhone video is often HDR (HLG); tone-map it to normal SDR so colors don't wash out later:

```bash
# the chain my inbox job runs for iPhone HLG video (drop the zscale/tonemap part for SDR files)
ffmpeg -i IMG_1234.MOV -map 0:v:0 -map 0:a:0? \
  -vf "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,scale='if(gt(iw,ih),min(1920,iw),-2)':'if(gt(iw,ih),-2,min(1920,ih))',format=yuv420p" \
  -c:v libx264 -crf 18 -preset medium -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -c:a aac -b:a 192k -movflags +faststart IMG_1234.edit.mp4
```

### 2. Transcribe, but only to know what was said
Any speech-to-text works (I use parakeet through `npx hyperframes transcribe`, or Whisper). Read the transcript to pick lines. Don't cut on its word times: in my test of 120 takes, the transcriber put the first word 0.2 to 0.5 s too early in 94 of them.

### 3. Pick the lines
Give the transcript to your agent with rules like these:
- One story: a question in the first 30 seconds that the end answers, one or two surprises, why the viewer should care, one thing they can try.
- Cut false starts, repeats ("I'm probably, I'm probably"), and "um" between sentences.
- Cut anything you can't back with a file or a link.
- Cut anything that says the system does something it doesn't. (I said "it uploads everything". It doesn't: uploads wait for me. That line is gone.)

### 4. Force-align the words you kept
You already know the exact words, so match them to the audio instead of trusting the transcriber's timings. I use WhisperX alignment (wav2vec2, runs on a CPU, about 2 s per 10 s clip). Write numbers as words ("four hours") so the aligner can place them.

### 5. Cut with these numbers
- Start 0.10 s before the first word, end 0.18 s after the last word. Never cut into the neighbouring word.
- Inside a sentence, cut any pause longer than 0.4 s. Keep 0.10 s after the word before it and 0.08 s before the word after it.
- Zoom every other segment in by 1.12x, so the jump cuts look intentional.

```python
PRE, POST = 0.10, 0.18
GAP, KEEP_AFTER, KEEP_BEFORE = 0.40, 0.10, 0.08

def segments(words, prev_end, next_start):
    """words: [{"start", "end"}] in source seconds, from the aligner. Returns [(in, out)] to keep."""
    cin = max(words[0]["start"] - PRE, prev_end + 0.02)
    cout = min(words[-1]["end"] + POST, next_start - 0.02)
    segs, s0 = [], cin
    for w, nxt in zip(words, words[1:]):
        if nxt["start"] - w["end"] > GAP:
            segs.append((s0, w["end"] + KEEP_AFTER))
            s0 = nxt["start"] - KEEP_BEFORE
    segs.append((s0, cout))
    return segs
```

### 6. Captions from the aligned words
Show 1 to 3 words at a time, timed to the word, with your keywords in one highlight color.

### 7. Have a model that can watch video review it
- Cut the render into pieces of 70 s or less. Longer pieces make the model invent scenes and misread on-screen text.
- Tell it: "Answer only from watching and listening to the video yourself. Do not run any tools." Ask for timestamps, and "can't tell" instead of guesses.
- Check every claim against the frames before you fix anything. Reviewers are often wrong about cut words and about model names newer than their training.

### 8. Put a hard timeout on every model call
My Gemini call printed its full answer in 65 s and then never exited. It sat there for 37 minutes. The command-line tool's own timeout flag didn't fire, so the wrapper has to do it:

```python
import subprocess

def ask(cmd, timeout=360):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        return out  # keep whatever it printed before it hung
```

### 9. Loudness
Master to -14 LUFS with a true peak of -1.5 dB (ffmpeg `loudnorm`, two passes). Keep the music around 7% of full volume under talking.

## The prompt (copy, paste, change the folder)

```text
You are my video editor. New phone clips are in ./inbox/<date>/.
1. Transcribe each clip. Use the transcript to read what I said, not for cut times.
2. Pick lines for one video: a question in the first 30 s that the end answers on screen,
   one or two surprises, why a viewer should care, one thing they can try.
3. Cut false starts, repeats, "um" between sentences, anything I can't back with a file,
   and anything that claims the system does something it doesn't.
4. Write an edit list: clip, rough in/out, the exact words I said, the caption.
5. Force-align those exact words to the audio (WhisperX). Cut 0.10 s before the first word
   and 0.18 s after the last, never into the next word. Cut pauses over 0.4 s.
6. Captions: 1-3 words at a time from the aligned words. Every number on screen
   gets a source line in facts.md.
7. Render. Have a model that can watch video review it in pieces of 70 s or less:
   no tools, timestamps, "can't tell" instead of guessing. Check its claims against frames.
8. Put a hard timeout on every model call and keep whatever it printed.
9. Don't publish anything. Send me the file and one line on what you cut and why.
```

## Tools I used (all free or open source, except the AI plans I already pay for)
- HyperFrames (HTML to video): https://github.com/heygen-com/hyperframes
- WhisperX (forced alignment): https://github.com/m-bain/whisperX
- RobustVideoMatting (cuts me out of the background, GPU): https://github.com/PeterL1n/RobustVideoMatting
- ffmpeg: https://ffmpeg.org
- Gemini through the Antigravity CLI for the video reviews; Claude Code as the agent that runs all of the above.
