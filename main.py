#!/usr/bin/env python3
"""Commit-message entry for make.fun bounty
u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722.

Writes a single commit message (at most 100 characters) to
/output/entry.txt: the message for a bug fix that made
everything worse. Standard library only, no network, no input
files: everything the program writes is in this file.
"""

import os
import sys

# The commit message: a tired engineer's one-liner for a fix
# that backfired. The fix did not kill the bug, it bred: one
# bug became two, smaller and faster, so the repair broke more
# than it mended. It reads like a real subject line, needs no
# explanation, and avoids the obvious angles (revert, testing
# in production, breaking everything).
MESSAGE = "fix: replaced the bug with two smaller, faster bugs"

MAX_CHARS = 100


def validate(text):
    """The gate accepts UTF-8 text of 1 to 100 characters."""
    stripped = text.strip()
    if not stripped:
        raise ValueError("commit message must not be only whitespace")
    if len(stripped) > MAX_CHARS:
        raise ValueError(
            "commit message is %d characters, over the %d limit"
            % (len(stripped), MAX_CHARS)
        )
    # One line: a newline would make it a second line, not a
    # one-line commit subject.
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("commit message must be a single line")
    return stripped


def output_path():
    """The grader sets MAKEFUN_OUTPUT_DIR; default is /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def main():
    text = validate(MESSAGE)
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote %d characters to %s" % (len(text), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
