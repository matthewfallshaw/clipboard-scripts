"""Word/case transforms shared by the pb-* scripts.

``titlecase`` follows John Gruber's TitleCase rules: capitalise every word except
small words, unless first or last; leave anything with an internal capital
(acronyms, camelCase) alone.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# humanize
# ---------------------------------------------------------------------------

_SMALL_HUMANIZE_WORDS = re.compile(r"^(?:and|the|of|is)$", re.IGNORECASE)


def _all_caps(text: str) -> bool:
    """Report whether `text` has no ASCII lowercase letter anywhere."""
    return re.search(r"[a-z]", text) is None


def _dotty(text: str) -> bool:
    """Report whether `text` contains a "word.word" boundary (e.g. "Pirates.S01")."""
    return re.search(r"\w+\.\w+", text, flags=re.ASCII) is not None


def _as_humanize(text: str) -> str:
    """Approximate ActiveSupport::Inflector.humanize.

    Downcases the string (letter/digit runs only, so punctuation and
    spacing are untouched), strips a leading run of underscores and a
    trailing "_id", turns remaining underscores into spaces, and
    capitalises the first character.
    """
    result = re.sub(r"^_+", "", text)
    result = re.sub(r"_id$", "", result)
    result = result.replace("_", " ")
    result = re.sub(r"[A-Za-z0-9]+", lambda m: m.group(0).lower(), result)
    return re.sub(r"^\w", lambda m: m.group(0).upper(), result, count=1, flags=re.ASCII)


def _humanize_word(word: str) -> str:
    """Downcase a small joining word ("and", "the", "of", "is")."""
    return word.lower() if _SMALL_HUMANIZE_WORDS.match(word) else word


def humanize(text: str) -> str:
    """Turn a shouty/underscored/dotted label into a readable phrase.

    Ported from the Ruby ``HumanizingString#humanize``:

    - "LOREM IPSUM DOLOR SIT AMET." -> "Lorem Ipsum Dolor Sit Amet."
    - "JAKE AND THE NEVER LAND PIRATES" -> "Jake and the Never Land Pirates"
    - "Jake.and.the.Never.Land.Pirates" -> "Jake and the Never Land Pirates"
    - "Pirates.S01E05" -> "Pirates S01E05"

    Rules, applied in order: "@", "_" and "-" become spaces; an all-caps
    string (no lowercase letters at all) is downcased then each word is
    capitalised; a "dotted" string (a run of dots between word characters,
    as in filenames or episode codes) has those dots turned into spaces;
    anything else is passed through ActiveSupport-style humanize. Finally,
    the small joining words "and", "the", "of", "is" are lowercased unless
    that lowercasing already happened above.
    """
    text = re.sub(r"[@_-]", " ", text)
    if _all_caps(text):
        base = _as_humanize(text)
        base = " ".join(word.capitalize() for word in base.split())
    elif _dotty(text):
        base = re.sub(r"(\w)\.(\w)", r"\1 \2", text, flags=re.ASCII)
    else:
        base = _as_humanize(text)
    return " ".join(_humanize_word(word) for word in base.split())


# ---------------------------------------------------------------------------
# titlecase
# ---------------------------------------------------------------------------

SMALL_WORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "as",
        "at",
        "but",
        "by",
        "en",
        "for",
        "if",
        "in",
        "of",
        "on",
        "or",
        "the",
        "to",
        "v",
        "v.",
        "via",
        "vs",
        "vs.",
    }
)

_SPLIT_RE = re.compile(r"(\s+)")
_STRIP_PUNCT = ".,;:!?\"'()[]{}"


def _has_internal_capital(word: str) -> bool:
    """Report whether `word` is an "iPhone"/"NASA"/"McDonald" -- leave those alone."""
    letters = [c for c in word if c.isalpha()]
    return any(c.isupper() for c in letters[1:])


def _titlecase_word(word: str) -> str:
    """Capitalise the first letter of `word`, downcase the rest."""
    if _has_internal_capital(word):
        return word
    match = re.search(r"[A-Za-z]", word)
    if not match:
        return word
    i = match.start()
    return word[:i] + word[i].upper() + word[i + 1 :].lower()


def _lowercase_word(word: str) -> str:
    """Downcase `word`, unless it already carries an internal capital."""
    return word if _has_internal_capital(word) else word.lower()


def titlecase(text: str) -> str:
    """Title-case `text` in standard English style-guide fashion.

    Capitalises each word except small words -- articles and short
    conjunctions/prepositions, see `SMALL_WORDS` -- which stay lowercase
    unless they are the first or last word. Words that already carry an
    internal capital (acronyms like "NASA", camel-case like "iPhone") are
    left untouched. Hyphenated compounds are title-cased part by part.
    """
    tokens = _SPLIT_RE.split(text)
    word_indices = [i for i, tok in enumerate(tokens) if i % 2 == 0 and tok]
    if not word_indices:
        return text
    first_i, last_i = word_indices[0], word_indices[-1]

    for i in word_indices:
        word = tokens[i]
        core = word.strip(_STRIP_PUNCT)
        is_small = core.lower() in SMALL_WORDS
        if is_small and i not in (first_i, last_i):
            tokens[i] = "-".join(_lowercase_word(p) for p in word.split("-"))
        else:
            tokens[i] = "-".join(_titlecase_word(p) for p in word.split("-"))
    return "".join(tokens)


# ---------------------------------------------------------------------------
# separator normalisation
#
# Shared by pb-* scripts that were byte-for-byte identical in Ruby.
# Neither function collapses runs of separators -- that matches the
# observed Ruby behaviour (each separator character becomes exactly one
# underscore/space; only the ends are trimmed).
# ---------------------------------------------------------------------------


def underscorize(text: str) -> str:
    """Collapse runs of non-alphanumeric characters into single underscores.

    Trims them from the ends too. Shared by pb-underscore and pb-underscorize.
    """
    result = re.sub(r"[\W_]+", "_", text, flags=re.ASCII)
    return re.sub(r"^_+|_+$", "", result)


def undasherize(text: str) -> str:
    """Collapse runs of dashes/underscores into single spaces, and trim them.

    Shared by pb-undasherize, pb-ununderscore, and pb-ununderscorize.
    """
    result = re.sub(r"[-_]+", " ", text)
    return re.sub(r"^ +| +$", "", result)
