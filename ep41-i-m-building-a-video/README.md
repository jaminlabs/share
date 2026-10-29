# I'm building a video editor that tells me my content is boring (EP41)

Cutting a video is the easy part now. The hard part is knowing what to say. So the editor I'm building (my app
CueRoom plus my PC) does more than cut. Before I edit, it reads the transcript of my take and tells me which lines to
say again, and why.

The "why" comes from my own YouTube retention data. From about 30 of my videos, these patterns came up again and again:
- Openings that named something people know and gave a surprise in the same sentence kept 53-63% of viewers.
  Openings that pointed at something I hadn't named yet ("the app", "they") kept 16-45%.
- Side talk about myself (excuses, hopes, "I haven't gone viral yet") lost viewers 1.4-3.9x faster than usual.
- Lines with a concrete fact or a number kept viewers. Loss dropped to 0.3-0.7x of the usual rate.

My best video so far has 2,610 views, so treat these as one small channel's numbers, not laws.

## Take this

`content-coach-prompt.md` is a prompt you can paste into any AI chat with the transcript of your own take. It flags
the weak lines with the same rules my coach uses and gives you one line to say again for each, before you start
editing. Run it on your next take, re-record only the lines it flags, then edit.
