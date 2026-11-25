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
    # Must be a real string and valid UTF-8: a surrogate or a
    # non-encodable character would fail the gate's UTF-8 check.
    if not isinstance(text, str):
        raise ValueError("commit message must be a string")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("commit message is not valid UTF-8: %s" % exc)
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
    # No control characters: the gate reads the file as text,
    # and a stray control byte would make the entry unreadable.
    for ch in stripped:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            raise ValueError(
                "commit message contains control character U+%04X" % ord(ch)
            )
    return stripped


def verify_output(path, expected):
    """Read the file back and fail loudly unless it is exactly
    the validated message: UTF-8, one line, 1 to 100 chars."""
    with open(path, "rb") as f:
        raw = f.read()
    try:
        actual = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("output is not valid UTF-8: %s" % exc)
    if actual != expected:
        raise ValueError(
            "output mismatch: wrote %r, read back %r" % (expected, actual)
        )
    if not 1 <= len(actual) <= MAX_CHARS:
        raise ValueError(
            "output is %d characters, outside the 1-%d range"
            % (len(actual), MAX_CHARS)
        )
    if "\n" in actual or "\r" in actual:
        raise ValueError("output must be a single line")
    return actual


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
    verify_output(path, text)
    print("wrote %d characters to %s" % (len(text), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
