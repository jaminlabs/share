# The outreach loop from "Nine never answered"

This is the loop I used to send free sample edits to creators. It's one message per person, with a free sample
first and no follow-ups, and it has a hard stop. Copy the states and rules and plug in your own offer.

## What happened

I sent ten creators a short that my editing system cut from one of their own recent videos, each with one
message. Nine never answered. One did, and the first thing they asked was "Is this made with AI?". By the time I
filmed, 19 people had a message and that was still the only reply. Ten is too few to judge, so the loop keeps
going until about a hundred.

## States

```
found -> video fetched -> sample made -> sample passed -> message drafted -> sent
sent  -> replied yes | replied no | replied question | no answer after 24 h
closed = stopped before anything was sent (no public contact, no usable video, sample failed twice)
```

`loop.py` has the same states as a small Python state machine with no dependencies and no network. Run
`python3 loop.py` to see one person go through it.

## Rules

1. **One message per person.** No follow-ups and no reminders. Once someone is `sent`, the only way out is an
   answer or 24 hours of silence. If they answer late, they still move to replied.
2. **Free sample first.** Make it from their own recent video. If you wouldn't post it yourself, don't send it.
3. **Check before you send.** The sample has to pass a quality check, and every name, title or number on screen has
   to come from their own words or their own video. If a sample fails, fix it once. If it fails again, close that
   person and move on. Don't lower the bar to keep the numbers up.
4. **Contact them only through what they made public.** Try email first (it keeps your DM accounts safe), then their
   own DMs. If the bio says "do not DM", use email only. Never guess an address.
5. **Pace it to protect your accounts.** At most 10 DMs a day per account, 20 minutes apart. At most 60 emails a day,
   3 minutes apart. At most 50 messages a day overall. A deadline doesn't raise the caps.
6. **Stop rule.** If about 95 to 100 people have a message and nobody is interested, stop and change the offer (who,
   what, price) before you send more.
7. **After the first reply, talk like a person.** Automation finds people and sends the first message. You do the
   conversation yourself.

## The message

See `message-template.md`. Short, one link, one question, and the price once.

My message never said "AI", and the one reply asked about it right away. Decide how you'll answer that before you
send anything. Mine was "Yes, it's AI, but the content is yours, I just did the editing."
