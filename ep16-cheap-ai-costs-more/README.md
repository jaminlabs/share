# The real-price check: is the cheap model actually cheaper?

Before you swap a $200/month plan for a cheaper model, price your own time, not just the tokens. Takes about 5 minutes.

## 1. Write down three numbers

| | Your number |
|---|---|
| Your hourly rate (what an hour of your time is worth; at least what you need to live on) | $ ___ / h |
| Hours to get the cheap model working on this job (prompts, retries, guardrails, checking its output) | ___ h |
| Hours to redo that setup each time a new model comes out | ___ h per new model |

## 2. Do the math

```
setup cost  = setup hours × hourly rate
redo cost   = redo hours  × hourly rate × new models per year / 12      (per month)
real price  = cheap model's bill + setup cost (once) + redo cost (every month)
```

Compare the real price with the plan you'd cancel. If the setup alone costs more than a few months of the plan, the cheap model isn't cheaper for that job.

## My numbers (2026-10-21, my own rough math)

- My hourly floor: $10–20/h. Setup for a creative workflow: 2–3 weeks. Redo after a new model: 3–4 days.
- Low end: 2 weeks × 40 h × $10/h = **$800** of my time, plus about **$240** (3 days × 8 h × $10) every new model.
- The plan it would replace: Claude Max 20x, **$200/month** ([Anthropic help center](https://support.claude.com)).
- The test that day: DeepSeek V4 Flash (through the `pi` agent) editing one of my raw takes into a Short took ~2.5 hours and 4 revision rounds and cost $1.50 in API fees, and I had to ask several times for what Claude (on the plan I already pay for) did at once. One take, one day, my own rules: not a benchmark.

## Where cheap models are worth it

Jobs with a clear right answer and little judgement: searching the web, searching social media, routine manual steps, sorting and tagging. Point the cheap model there and keep the expensive one for creative work.

## Sources

- DeepSeek API prices: https://api-docs.deepseek.com/quick_start/pricing (deepseek-flash: $0.15–0.30 per 1M input tokens on a cache miss, $0.6–1.2 per 1M output tokens, off-peak vs peak; read 2026-10-21).
- DeepSeek's own margin math ("cost profit margin of 545%", one day in Feb 2025, theoretical): https://github.com/deepseek-ai/open-infra-index (202502OpenSourceWeek, day 6). 545% cost-profit ≈ 84% margin.
- ChatGPT Pro tiers ($100 / $200 / $500): https://help.openai.com
- My monthly AI bill: https://jaminlabs.com/stack/

The 80–90% margin figure for Anthropic in the video is my guess; Anthropic doesn't publish one.
