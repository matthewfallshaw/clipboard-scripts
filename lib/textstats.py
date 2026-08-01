"""Word- and character-counting helpers shared by pb-wc and pb-wcc.

Word counting uses Python's Unicode-aware ``\\w`` (unlike the Ruby original,
which was ASCII-only under Ruby's default regex semantics). See
``tests/test_pb_wc.py::TestCountWords::test_unicode_word_chars`` for the
behaviour this preserves: multi-byte letters such as accented characters
count as word characters, matching how a modern user actually expects
"café résumé" to count as two words rather than four fragments.
"""

from __future__ import annotations

import re

_WORD_RE = re.compile(r"[\w-]+")


def count_words(text: str) -> int:
    """Count words, where a word is a run of ``[\\w-]`` characters.

    Hyphenated words count as one word; underscores are word characters.
    """
    return len(_WORD_RE.findall(text))


def count_chars(text: str) -> int:
    """Count characters in text."""
    return len(text)
