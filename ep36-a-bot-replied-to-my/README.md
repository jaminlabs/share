# A bot replied to my $99 offer (EP36)

I sent a creator a free Short I'd made from one of their videos, plus an offer: 30 Shorts a month for $99.
The answer came back within half an hour. It said "Hi! Thanks for your Message!", pitched me a coaching session, gave me a
community link and a bookings email, and was signed "~Support Team". Nothing in it mentioned the Short or the offer.

So a sales DM got a sales DM back. My guess is that more of these conversations will be bots talking to bots.

## Take this: check a reply before you answer it

`canned_reply_check.py` compares your message with their reply and tells you whether anything in the reply shows
that someone read what you sent. Plain Python 3, no packages, and nothing gets sent anywhere.

```
python3 canned_reply_check.py my_message.txt their_reply.txt
```

```
CANNED: nothing here shows they read your message
  canned: template phrase: 'thanks for your message'
  canned: template phrase: 'support team'
  canned: 3 link(s) or email(s) of their own
  canned: asks you nothing
  canned: not one word of your message comes back
```

What it looks for:
- **Canned:** template phrases ("thanks for your message", "~Support Team", "book a call", "join our community"),
  their own links and emails, no question back to you, and none of your words coming back.
- **Read:** your words, and especially your numbers ($99, 30), showing up in their reply.

It's a hint, not proof. A person can paste a saved reply too.
If it says CANNED, I'd send one more message that's short and asks one question only a person who read it can
answer, instead of replying to the template.

Made by jamin labs: automation, with receipts.
