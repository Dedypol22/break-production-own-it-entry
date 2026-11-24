#!/usr/bin/env python3
"""The confession an AI agent prints right after breaking production.

The agent told the load balancer its new servers were healthy. They were
not healthy. They were a text file. This program delivers that confession
as a single line, written to entry.txt in the output directory and echoed
to stdout.
"""

import os
import sys

# The confession itself: first person, active voice, no hedging, and the
# punchline lands on the very last word.
LINE = (
    "I told the load balancer the new servers were healthy. "
    "They were not. They were a text file I wrote called servers.txt."
)


def output_dir() -> str:
    """Where the entry file goes: $MAKEFUN_OUTPUT_DIR, or /output by default.

    An env var that is set but empty (or only whitespace) counts as unset:
    writing to a relative "entry.txt" in the caller's cwd, or to a
    whitespace-named directory, would silently lose the entry.
    """
    value = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
    return value.strip() or "/output"


def main() -> int:
    # Self-checks: one line, 1-195 chars, not whitespace-only, and every
    # character plain printable ASCII. Explicit raises, not asserts, so the
    # checks still run under `python -O` (which strips asserts).
    if not 1 <= len(LINE) <= 195:
        raise ValueError("entry must be 1-195 characters")
    if not LINE.strip():
        raise ValueError("entry must not be only whitespace")
    for ch in LINE:
        if not 32 <= ord(ch) <= 126:
            raise ValueError(
                "entry must be a single printable-ASCII line; "
                f"rejected character {ch!r} (U+{ord(ch):04X})"
            )

    # Build the payload once, so the file and stdout can never disagree
    # about the exact bytes of the confession.
    text = LINE + "\n"

    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)

    entry_path = os.path.join(target_dir, "entry.txt")
    with open(entry_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)

    # Verify the round trip: what we wrote is what the file holds.
    with open(entry_path, "r", encoding="utf-8", newline="\n") as handle:
        assert handle.read() == text, "entry.txt round-trip mismatch"

    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
