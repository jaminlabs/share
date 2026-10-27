# Four-hour edit audit

Video: ______________________  Date: __________  Total minutes: ______

Mark the agent column Y (an agent can do it from your files today), P (part of it) or N (no).

| # | Step | My minutes | Agent? Y / P / N | What to try first |
|---|---|---|---|---|
| 1 | Shoot it (mine took an hour or two) | | N | Before you film, record a 2-minute voice note and ask an agent for 5 lines to say. You still film it. |
| 2 | Open CapCut or Premiere, put the footage in | | Y if you edit from files | Trim without a project: command A below. |
| 3 | Background music | | Y | Use only tracks you have a license for. Duck the music under your voice: command B below. |
| 4 | Sound effects, video effects | | P | Pick the words that get a sound and let the agent place them. Which sound, and whether it fits, is your call. |
| 5 | Do the cuts, take the silence out | | Y | List every pause: command C below. Or get a timestamp for every word (command D) and cut on words, not on waveforms. |
| 6 | Retake what's missing | | P | Give an agent the transcript and ask: "What did I set up and never finish? Which number did I say wrong?" You film the retake. |
| 7 | Watch it once and approve | | N | Yours. Check every number on screen against what you said. |

Biggest Y step: ____________________  Minutes it took: ______

## Commands (free, open source: ffmpeg and WhisperX)

A. Cut one part out of a take (start and end in seconds, re-encoded so the cut is exact):

```
ffmpeg -ss 12.4 -to 31.0 -i take.mov -c:v libx264 -crf 18 -c:a aac part.mp4
```

B. Put music under your voice and duck it while you talk:

```
ffmpeg -i voice.wav -i music.mp3 -filter_complex "[0:a]asplit=2[v][sc];[1:a]volume=0.3[m];[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[duck];[v][duck]amix=inputs=2:duration=first:normalize=0[out]" -map "[out]" mixed.wav
```

C. Find every pause longer than 0.4 seconds (prints silence_start / silence_end in seconds):

```
ffmpeg -i take.mov -af silencedetect=noise=-35dB:d=0.4 -f null - 2>&1 | grep silence_
```

D. A start and end time for every word, as JSON (WhisperX; `whisperx --help` shows the options of your version):

```
whisperx take.mov --model large-v3 --output_format json --output_dir words
```

Commands A to C were run on test files on 2026-10-27 with ffmpeg 9. Raise `noise` (for example -30dB) if C finds no
pauses in a noisy room, lower it if it finds too many.
