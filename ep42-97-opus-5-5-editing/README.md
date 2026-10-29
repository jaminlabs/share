# $97 Opus 5.5 editing courses vs free open-source clones

From the jamin labs video of the same name. In October 2026 the same thing happened three times in a few weeks:
someone charged for an AI-built tool, and someone else gave a version away for free.

## The three cases (every date and number from the public post)

| What was paid | What came next | Source |
|---|---|---|
| An AI YouTuber's video-editing tool behind a $97-a-month paid community (Kim Doyal, Oct 12, 2026) | free247editor, a free MIT-licensed video editor for Claude (a separate project, no known link; repo created Oct 15 UTC) | [Kim Doyal's post](https://kimdoyal.substack.com/p/how-to-edit-video-with-claude-even), [free247editor](https://github.com/riecodes/free247editor) |
| beehiiv, the newsletter service Marc Lou said "keeps increasing its prices every year" (Oct 3) | Marc built his own with "a few prompts with Opus 5.5" (Oct 9), open-sourced it as MailCheap the next day, and launched it as "83% cheaper" by his own count (Oct 15) | [Oct 3](https://x.com/marclou/status/2106333942911758358), [Oct 9](https://x.com/marclou/status/2108509543810605218), [Oct 10](https://x.com/marclou/status/2108918232279400920), [Oct 15](https://x.com/marclou/status/2110743912885489960), [repo](https://github.com/marclou/mailcheap) |
| DataFast, Marc Lou's revenue analytics: Ahmed Gagan was paying $39 a month | Oct 24, 14:23 UTC: DataBull, "same idea", $29 lifetime. 4 h 31 min later: Minilytics was posted as "Datafast (But for free)", MIT, "$0 cost" to deploy (its repo was created 19 h before DataBull's post) | [DataBull post](https://x.com/ahmedgagan11/status/2113999817714319423), [Minilytics post](https://x.com/surendra_pandar/status/2114068131304050724), [repo](https://github.com/surendrapandar/minilytics) |

Prices change: DataBull's own page said $49 once on Oct 28.

## Take this: `free_clone_finder.py`

Before you pay for a tool or a course, look for the free version someone already posted.

```
python3 free_clone_finder.py "DataFast"
python3 free_clone_finder.py "beehiiv" --top 15
python3 free_clone_finder.py "claude video editor"
```

It searches public GitHub repositories that mention the tool next to "alternative", "open source", "self-hosted" or
"free", and prints stars, license, created and last-push dates and the link. Python 3.8+, standard library only, no
account or token.

Read the results like this:
1. License first. MIT or Apache-2.0: free to use, also at work. No license: you may not use it.
2. Last push. Untouched for months often means broken against today's APIs.
3. Created date. A copy made the same week as a paid launch is often a weekend project: try it on something small.
4. Stars are popularity, not quality. Open the README, then decide whether the paid one is worth it to you.

Free still costs something: the free video editors run on a paid AI plan (Claude's Opus models need a paid plan or
API credits), and self-hosted tools need your own server or a free-tier account you look after.
