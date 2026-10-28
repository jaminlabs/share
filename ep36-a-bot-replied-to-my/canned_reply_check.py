#!/usr/bin/env python3
"""Did a person read my DM, or did I get a canned auto-reply?

Usage:
    python3 canned_reply_check.py my_message.txt their_reply.txt

Prints a verdict and the reasons. Plain Python 3, no packages, nothing is sent anywhere.
It only looks at the two texts, so it is a hint, not proof: a person can paste a saved reply too.
"""
import re
import sys

STOP = set("""a an and are as at be but by can do for from get got have hey hi how i i'm if in is it its it's just like
me my of on or our so that the their them then there they this to try us want was we what when where which who will
with would you your you're yours""".split())

TEMPLATE_PHRASES = [
    r"thanks? (you )?for (your|the) (message|dm|reaching out|note)",
    r"we('ll| will) get back to you",
    r"(support|customer|care|social) team",
    r"(book|schedule|invest in) (a|an|your) .{0,40}(call|session|consultation)",
    r"(bookings?|inquiries|enquiries|business email)\s*:",
    r"join (our|my) .{0,30}(community|group|newsletter|list)",
    r"can'?t wait to work with you",
    r"this is an automated",
    r"(away|out of office)",
]
LINK = re.compile(r"https?://\S+|www\.\S+|\b[\w.-]+@[\w-]+\.\w+")


def words(text):
    found = re.findall(r"\$?\d+(?:[.,]\d+)?|[a-z][a-z']+", text.lower())
    return [w for w in found if w not in STOP and (len(w) > 2 or w[0].isdigit() or w[0] == "$")]


def check(mine, theirs):
    signs, human = [], []
    low = theirs.lower()
    for pat in TEMPLATE_PHRASES:
        m = re.search(pat, low, re.M)
        if m:
            signs.append(f"template phrase: '{m.group(0).strip()}'")
    links = LINK.findall(theirs)
    if links:
        signs.append(f"{len(links)} link(s) or email(s) of their own")
    if not re.search(r"\?", theirs):
        signs.append("asks you nothing")
    # what of your message shows up in their reply: numbers, prices, rare words
    my_words = set(words(LINK.sub(" ", mine)))
    shared = sorted(set(words(LINK.sub(" ", theirs))) & my_words)
    numbers = [w for w in shared if re.search(r"\d", w)]
    if shared:
        human.append("uses your words: " + ", ".join(shared[:8]))
    else:
        signs.append("not one word of your message comes back")
    if numbers:
        human.append("repeats your numbers: " + ", ".join(numbers))
    score = len(signs) - 2 * len(human)
    if score >= 3:
        verdict = "CANNED: nothing here shows they read your message"
    elif score >= 1:
        verdict = "PROBABLY CANNED: write once more, short, with one question only a reader can answer"
    else:
        verdict = "LOOKS READ: answer it like a conversation"
    return verdict, signs, human


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip())
        return 2
    mine = open(argv[1], encoding="utf-8").read()
    theirs = open(argv[2], encoding="utf-8").read()
    verdict, signs, human = check(mine, theirs)
    print(verdict)
    for s in signs:
        print("  canned:", s)
    for h in human:
        print("  read:  ", h)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
