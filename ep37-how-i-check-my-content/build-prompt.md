# Prompt: build my own daily content dashboard

Fill in the three lines, then paste everything below the line into a coding agent (Claude Code, Codex or similar).

- My platforms: <for example: YouTube, Instagram, TikTok, X>
- My accounts: <for example: YouTube channel ID, @handles>
- Where it runs: <for example: my Mac, my Linux PC>

---

Build me a small personal dashboard that shows how my content is doing. It runs only on my own computer.

**Collector (runs once a day):**
- A script that runs once a day at a time I choose (cron, launchd or a systemd timer, whichever fits my computer).
- YouTube: use the YouTube Data API v3 with an API key read from an environment file outside the project. For my channel, list my public videos and save each video's title, publish date, views, likes and comments.
- Other platforms in my list: read only public numbers I can see without logging in. If a platform can't be read, save "not collected" with the reason. Never save a zero for something you couldn't read.
- Save one row per post per day in a SQLite file (date, platform, post id, title, views, likes, comments, collected time), plus one row per platform per day for followers/subscribers.
- Never post, comment or change anything on any account.

**Page (a single local web page reading that SQLite file):**
1. **Platforms:** one card per platform with followers, total views of tracked posts, the change since yesterday, how many posts were measured, and the time it was last collected.
2. **Numbers to watch:** two boxes I fill in by hand from YouTube Studio, each with the date I read it and a target: "Long-form click rate" (target over 2%) and "Shorts: stayed to watch" (target over 50%). Label them exactly like that so I never mix them up.
3. **What to change:** a short list I write myself, biggest effect first (titles and thumbnails, the first second of a Short, the last line, topics), with the date I wrote it.
4. **Growth, day by day:** a line chart with one line per platform, 30 days by default, and a switch between followers and views. Missing days stay as gaps.
5. **Content performance:** every post in one table, sorted by total views, with the change since yesterday, a platform filter and a search box.

**Rules:**
- Show "not collected" instead of zero when a number is missing, and show the collected time next to every number.
- A daily change is only computed when the same post has a value for the day before.
- No tracking scripts, no outside fonts or CDNs; it should work offline.
- Put a short README in the project: how to set the API key, how to run the collector by hand, how to see the page, and how to turn the daily run off.

When it's built, run the collector once, open the page, and show me what got collected and what didn't.
