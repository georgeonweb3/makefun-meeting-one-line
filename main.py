#!/usr/bin/env python3
"""The Meeting That Should Have Been One Line — make.fun entry.

Writes one line to /output/entry.txt:

    Somebody booked Conference Room B for a meeting about meetings,
    and Brenda brought a cake that said "See you at the next one".

The joke: a meeting whose only subject is meetings — booked in a named
room, with a named colleague, and a cake that celebrates the cycle
continuing. Three beats (booked / brought cake / quote), ends on the
quoted punch. A meeting about meetings has no subject, so nothing
could justify holding it: that is how the line kills the meeting.

Winner of a blind pairwise tournament (6 candidates, 15 pairs, fresh
Gemini judge): 5/5 wins. Extra-mile pass compared it against the house
baseline ("This meeting could have been an email.") and the past
leaderboard tops; it ships exactly as judged.

Python 3.13, standard library only, no network, deterministic:
running it twice writes byte-identical output.
"""

import os

ENTRY = (
    'Somebody booked Conference Room B for a meeting about meetings, '
    'and Brenda brought a cake that said "See you at the next one".'
)

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")

# Gate from the competition's own kit (competition.yaml): entry.txt
# must be UTF-8 text of 1 to 200 characters, not only whitespace.
MAX_CHARS = 200


def main() -> None:
    # Gate self-check: /output/entry.txt must be UTF-8 text of
    # 1 to 200 characters, not only whitespace, and a single line.
    # Verified live: 126 characters, one line, no trailing newline.
    assert 1 <= len(ENTRY) <= MAX_CHARS, (
        f"entry is {len(ENTRY)} chars, gate wants 1-{MAX_CHARS}"
    )
    assert "\n" not in ENTRY and "\r" not in ENTRY, "entry must be a single line"
    assert ENTRY.strip(), "entry must not be only whitespace"
    assert ENTRY == ENTRY.strip(), "entry must not start or end with whitespace"
    assert ENTRY.encode("utf-8").decode("utf-8") == ENTRY
    directory = os.path.dirname(OUTPUT_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as handle:
        handle.write(ENTRY.encode("utf-8"))
    # Read-back verification: the graded artifact is the file on
    # disk, not the string in memory — confirm the bytes landed.
    # No randomness, no clock, no I/O beyond the one write, so a
    # second run reproduces the same 126 bytes exactly.
    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    assert written == ENTRY.encode("utf-8"), (
        f"entry.txt on disk differs from ENTRY: {written!r}"
    )


if __name__ == "__main__":
    main()
