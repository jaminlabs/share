# How I check my content stats every day

From the jamin labs Short "How I check my content stats every day". It shows the one page I open every day to see how my posts are doing, step by step. This folder has what you need to build your own.

## The five checks on my page

1. **Platforms.** One card per platform (YouTube, Instagram, TikTok, X): followers, total views of the posts it tracks, and when it last collected.
2. **Click rate.** Long-form click-through rate and, for Shorts, how many people stayed to watch instead of swiping away, each with a target next to it. These are two different numbers: the Shorts one is "stayed to watch", not clicks.
3. **What to change.** A short list, biggest effect first: titles and thumbnails, the first second of a Short, its last line, topics.
4. **Growth, day by day.** One line per platform, so I can see if I'm doing better than before.
5. **Content performance.** Every post sorted by views, with the change since yesterday, so the ones doing well and the ones doing badly sit on one list.

## How mine gets its numbers

- A small script runs once a day. It reads YouTube through the YouTube Data API and the public pages of Instagram, TikTok and X, and saves one row per post per day in a SQLite file. The page reads that file. No AI runs in the daily collection, and nothing gets posted.
- The "why views are low / what to change" panel is different: it came from one AI read of my YouTube Studio numbers on Oct 20. The page says so ("this page doesn't re-measure them daily"), and I update it by hand when I read Studio again.

## Build your own

Open `build-prompt.md`, fill in the three lines at the top (your platforms, your accounts, where it should run) and paste the whole thing into a coding agent (Claude Code, Codex or similar). It builds the same five checks on a page that only runs on your own computer.

Things to know before you start:
- Start with one platform. YouTube is the easiest: the YouTube Data API gives public views of your own videos with a free API key. Click-through rate and "stayed to watch" are only in YouTube Studio (or the YouTube Analytics API with your login), so the prompt has you type those in by hand at first.
- Instagram, TikTok and X change their pages often. Expect to fix the collector now and then, and keep a "last collected" time on every card so you can see when it broke.
- Keep your API keys in an environment file outside the project, never in the page or in a repo.

Numbers in the video are from my channel on Oct 20 (click rate) and Oct 28 (views and followers). Yours will be different, and that's the point of checking them every day.
