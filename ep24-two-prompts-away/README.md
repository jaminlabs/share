# The two-prompt test: how much of your app can a model copy?

From the jamin labs Short "Your app is two prompts away" (2026-10-24). In the Short I say that most of what we
build is a few prompts away from the big AI labs. That is my opinion, not a measurement. This is the test you can run
on your own product today to see what is copyable and what isn't.

**Time:** 10 minutes of your time (the model may take longer to answer). **Needs:** any chat model you already
use, and your product's public landing page.

## How to run it

1. Open your landing page logged out (a private window). Select all the text on it and copy it. Don't paste
   anything that is not public.
2. Start a new chat. No files, no tools, no web search: just the chat. Paste **prompt 1** below with your page text.
3. When it answers, send **prompt 2**. Stop there: two prompts, no hints, no fixing its code.
4. Save the file it gave you as `index.html` and open it in a browser.
5. Fill in the checklist below. Everything on the "it could not copy" side is your moat. Everything on the other side
   is a weekend for anyone with the same page.

**Prompt 1**

```text
Below is the full public text of a product's landing page. Rebuild the product it describes as a working app in ONE
self-contained index.html (HTML, CSS, JS; no external files or CDNs). Copy what the product does, not the website.
Reply with the complete file in one html code block.

--- LANDING PAGE TEXT ---
<paste your page text here>
```

**Prompt 2**

```text
Second and last prompt: make your rebuild as close to the real product as you can in one more pass. Reply with the
complete updated index.html in one html code block, then a short list titled CANNOT REBUILD: what you could not
rebuild from the landing page alone, and why.
```

## The checklist

Mark each line: did the copy get it (C), or not (N)?

| | What | C / N |
|---|---|---|
| 1 | The main screen and the main button | |
| 2 | The core flow, start to finish, with fake data | |
| 3 | Your wording, your steps, your pricing page | |
| 4 | The part that needs **your** data (history, a model you tuned, a dataset you collected) | |
| 5 | The part that runs somewhere it can't see (your server, your PC, your agents, your integrations) | |
| 6 | Your users: who already uses it, and why they came | |
| 7 | Your daily loop: what you change every day from what users hit | |
| 8 | Trust: your face, your name, your track record, your receipts | |

Lines 1-3 are usually "C". If lines 4-8 are also "C", the product is the page. Move the value into the parts a
page can't describe.

## My run (2026-10-24)

- Page: https://jaminlabs.com/ (where I build CueRoom, an iPhone camera that asks me the next question while I
  talk), read logged out on 2026-10-24.
- Model: Claude Opus 5.5 in the Claude Code CLI, chat only (tools turned off), in an empty folder.
- Prompt 1 took 23 minutes to answer (a very long reply). Prompt 2 took 5 minutes and gave one 80 KB `index.html`.
- What it built: a dark camera screen with "1 Talk. 2 Pause. 3 Get a question.", a record button, a takes list,
  a "good bits" picker, captions and a draft step. On my PC it said "No camera found" (no camera here), so I did not
  test the recording.
- Its own CANNOT REBUILD list, shortened: the question engine that runs on my PC; a native iPhone app; the agents
  that add custom animation per video; the fact checks; how the best parts are really chosen; exact word timing;
  posting to the platforms; version history and the waitlist.
- My checklist: 1 C, 2 C (with fake data), 3 C. 4 N, 5 N, 6 N, 7 N, 8 N.

So: the screens were two prompts away. My users, my daily loop and my face were not. That's the part I keep
working on.

## Sources

- Prompts: the exact text I sent is above (my run started the first prompt with "(https://jaminlabs.com, read
  logged out on 2026-10-24)" after "landing page").
- The model's limits are its own words from that run; I did not change its list, only shortened it.
