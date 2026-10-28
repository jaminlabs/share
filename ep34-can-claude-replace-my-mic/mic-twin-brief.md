# Brief for your coding agent: make my phone-mic takes sound like my mic

Paste this into Claude Code (or another coding agent) from an empty project folder. Fill in the two folder paths first.

---

I record videos of myself talking. Some takes use my mic, some only the phone's built-in mic. I want a tool that takes a
phone-mic video and returns the same video with the audio rebuilt to sound like my mic: same words, same timing, same
length, lip sync untouched.

My recordings:
- Mic takes (my voice, my mic): `<folder>`
- Phone-mic takes (my voice, phone only): `<folder>`

Work in this order and show me results at each step:

1. **Collect.** Extract the audio of every take as 48 kHz mono WAV. Leave the original files untouched. List each take
   with its length and which set it's in. If a take isn't clearly mic or phone, check a few video frames and ask me.
2. **Measure the gap.** Compare the average spectrum, noise floor and room tail of the two sets so we know what the
   phone loses (for me: most of 5-16 kHz, more room noise, a longer room tail).
3. **Build a judge.** Train a small mic-vs-phone classifier on my own takes only (spectrum features plus speech-model
   features such as WavLM). Hold out whole takes to test it. We use it to score every version.
4. **Make training pairs.** My sets don't contain the same sentences, so simulate them: degrade my mic takes until the
   judge calls them phone (measured phone EQ, room reverb, real noise from the quiet parts of my phone takes).
5. **Train the mapper.** A small model that maps phone speech features to mic speech features, trained on those
   simulated pairs, then voiced with an open vocoder (for example kNN-VC's HiFi-GAN). Keep the timing frame for frame
   so the words can't change.
6. **Test on phone takes the model never saw.** Report the judge score, a naturalness score (UTMOS) and how many words a
   transcriber reads differently, next to the original phone audio and a real mic take from the same room.
7. **Make a listening video.** The same 15 seconds as: phone original, simple cleanup (denoise + EQ), your model, real
   mic, all at the same loudness, labelled on screen. I'll pick by ear.
8. **Wrap it** as one command: `fix input.mov output.mov`. It should copy the video stream, replace only the audio,
   keep the length, and skip takes the judge already hears as mic.

Rules: keep everything local, never overwrite my original recordings, keep big temporary files out of /tmp, and ask
before any training run longer than an hour.
