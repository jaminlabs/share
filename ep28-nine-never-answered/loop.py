"""A one-message outreach loop as a small state machine. No dependencies, no network, no clock of its own.

    found -> video_fetched -> sample_made -> sample_passed -> dm_drafted -> sent
    sent  -> replied_yes | replied_no | replied_question | no_answer_24h
    closed: stopped before anything was sent

Rules it enforces:
- one message per person: `sent` has no way back, and a second send is refused;
- a failed sample is redone once, then the person is closed;
- 24 hours of silence after the message closes them as no_answer_24h; a late answer still moves them;
- stop when about 95 people have a message and nobody said yes.

Plug in your own finder, sample maker, judge and sender; call `step(lead, event, now)` after each one.
Run `python3 loop.py` for a walk-through.
"""
import datetime as dt

MOVES = {
    ("found", "fetched"): "video_fetched",
    ("video_fetched", "sample_made"): "sample_made",
    ("sample_made", "judge_pass"): "sample_passed",
    ("sample_made", "revise"): "video_fetched",
    ("sample_passed", "drafted"): "dm_drafted",
    ("dm_drafted", "sent"): "sent",
    ("sent", "reply_yes"): "replied_yes",
    ("sent", "reply_no"): "replied_no",
    ("sent", "reply_question"): "replied_question",
    ("sent", "no_answer"): "no_answer_24h",
    ("replied_question", "reply_yes"): "replied_yes",
    ("replied_question", "reply_no"): "replied_no",
    ("no_answer_24h", "reply_yes"): "replied_yes",
    ("no_answer_24h", "reply_no"): "replied_no",
    ("no_answer_24h", "reply_question"): "replied_question",
}
BEFORE_SEND = ("found", "video_fetched", "sample_made", "sample_passed", "dm_drafted")
CONTACTED = ("sent", "replied_yes", "replied_no", "replied_question", "no_answer_24h")
NO_ANSWER_HOURS = 24
STOP_AFTER = 95


def step(lead, event, now):
    """A copy of `lead` after `event`, or ValueError if the move is not allowed."""
    new = dict(lead)
    state = lead["state"]
    if event == "close":
        if state not in BEFORE_SEND:
            raise ValueError("only people who got nothing yet can be closed")
        new["state"] = "closed"
        return new
    if event == "sent" and lead.get("sends", 0):
        raise ValueError("already messaged once: no second message")
    if event == "revise" and lead.get("revisions", 0) >= 1:
        raise ValueError("sample failed twice: close this person")
    if (state, event) not in MOVES:
        raise ValueError(f"{event} is not a step from {state}")
    new["state"] = MOVES[(state, event)]
    if event == "revise":
        new["revisions"] = lead.get("revisions", 0) + 1
    if event == "sent":
        new["sends"] = 1
        new["sent_at"] = now.isoformat()
    return new


def no_answer_due(lead, now):
    """True when our one message is NO_ANSWER_HOURS old and still unanswered."""
    if lead["state"] != "sent" or not lead.get("sent_at"):
        return False
    return now - dt.datetime.fromisoformat(lead["sent_at"]) >= dt.timedelta(hours=NO_ANSWER_HOURS)


def should_stop(leads):
    """Stop sending when about STOP_AFTER people have a message and nobody said yes."""
    contacted = sum(1 for x in leads if x["state"] in CONTACTED)
    interested = sum(1 for x in leads if x["state"] == "replied_yes")
    return contacted >= STOP_AFTER and interested == 0


if __name__ == "__main__":
    t = dt.datetime(2026, 10, 26, 22, 0, tzinfo=dt.timezone.utc)
    lead = {"id": "creator-1", "state": "found"}
    for ev in ("fetched", "sample_made", "judge_pass", "drafted", "sent"):
        lead = step(lead, ev, t)
        print(f"{ev:<12} -> {lead['state']}")
    try:
        step(lead, "sent", t)
    except ValueError as e:
        print(f"second send  -> refused ({e})")
    later = t + dt.timedelta(hours=NO_ANSWER_HOURS)
    if no_answer_due(lead, later):
        lead = step(lead, "no_answer", later)
        print(f"24 h quiet   -> {lead['state']}")
    lead = step(lead, "reply_question", later + dt.timedelta(hours=3))
    print(f"late reply   -> {lead['state']}")
