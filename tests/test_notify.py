"""Tests for lib/notify's argument marshalling.

`lib/notify` finds hammerspoon-config's `bin/notify` at a fixed path under
`$HOME`, so pointing `$HOME` at a tmpdir holding a stub that dumps its argv
exercises the real script against a fake backend. No test here may reach the
installed backend, which would fire a notification at whoever is running the
suite.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

NOTIFY = Path(__file__).resolve().parent.parent / "lib" / "notify"

STUB = """#!/bin/sh
printf '%s\\n' "$@" > "$ARGV_DUMP"
"""


@pytest.fixture
def run_notify(tmp_path: Path):
    """Run `lib/notify` against a stub backend; return the argv it received."""
    home = tmp_path / "home"
    backend = home / "code" / "hammerspoon-config" / "bin" / "notify"
    backend.parent.mkdir(parents=True)
    backend.write_text(STUB)
    backend.chmod(0o755)
    dump = tmp_path / "argv"

    def run(*args: str) -> "list[str]":
        result = subprocess.run(
            [str(NOTIFY), *args],
            env={"HOME": str(home), "ARGV_DUMP": str(dump), "PATH": "/usr/bin:/bin"},
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        return dump.read_text().split("\n")[:-1]

    return run


class TestBackendDispatch:
    def test_from_supplies_both_title_and_id(self, run_notify) -> None:
        assert run_notify("--from", "pb-upcase", "--", "SHOUTING") == [
            "--title", "pb-upcase",
            "--id", "pb-upcase",
            "--private",
            "--", "SHOUTING",
        ]

    def test_explicit_title_follows_the_default_so_it_wins(self, run_notify) -> None:
        # bin/notify keeps the last occurrence of a flag, so ordering is the
        # whole mechanism by which an explicit value overrides --from's default.
        argv = run_notify("--from", "pb-upcase", "--title", "Shout", "--", "hi")
        assert argv.index("Shout") > argv.index("pb-upcase")

    def test_explicit_id_follows_the_default_so_it_wins(self, run_notify) -> None:
        argv = run_notify("--from", "pb-upcase", "--id", "shout-1", "--", "hi")
        assert argv.index("shout-1") > argv.index("pb-upcase")

    def test_sticky_and_duration_pass_through(self, run_notify) -> None:
        argv = run_notify("--from", "pb-x", "--sticky", "--duration", "30", "--", "hi")
        assert "--sticky" in argv
        assert argv[argv.index("--duration") + 1] == "30"

    def test_flags_are_absent_unless_asked_for(self, run_notify) -> None:
        argv = run_notify("--from", "pb-x", "--", "hi")
        assert "--sticky" not in argv
        assert "--duration" not in argv


class TestPrivacy:
    """Nothing a pb-* script shows may reach disk unless it asks.

    Almost every script echoes the clipboard, which is as likely to hold a
    password as a phone number, so the safe setting has to be the default
    one — a script that forgets to ask must not be the leaky case.
    """

    def test_private_by_default(self, run_notify) -> None:
        assert "--private" in run_notify("--from", "pb-x", "--", "hi")

    def test_private_by_default_when_sticky(self, run_notify) -> None:
        # Sticky cards outlive a Hammerspoon restart, so they are the ones
        # that would linger on disk longest.
        assert "--private" in run_notify("--from", "pb-x", "--sticky", "--", "hi")

    def test_persist_opts_back_in(self, run_notify) -> None:
        argv = run_notify("--from", "pb-x", "--persist", "--", "hi")
        assert "--private" not in argv
        assert "--persist" not in argv  # consumed here, not a bin/notify flag

    def test_message_is_last_and_introduced_by_a_separator(self, run_notify) -> None:
        assert run_notify("--from", "pb-x", "--", "hi")[-2:] == ["--", "hi"]

    def test_a_message_that_looks_like_a_flag_survives(self, run_notify) -> None:
        # Clipboard content is arbitrary; `--` is what stops it being parsed.
        assert run_notify("--from", "pb-x", "--", "--sticky")[-2:] == ["--", "--sticky"]

    def test_message_words_are_joined(self, run_notify) -> None:
        assert run_notify("--from", "pb-x", "--", "one", "two")[-1] == "one two"

    def test_an_empty_message_is_still_delivered(self, run_notify) -> None:
        # pb-strip-nonnumbers and friends notify an empty result rather than
        # staying silent; bin/notify rejects a *missing* message with exit 2.
        assert run_notify("--from", "pb-x", "--", "")[-2:] == ["--", ""]

    def test_a_bare_message_needs_no_separator(self, run_notify) -> None:
        assert run_notify("hello")[-2:] == ["--", "hello"]

    def test_from_defaults_to_the_scripts_own_name(self, run_notify) -> None:
        # Useless as a label, which is why every caller passes --from; the
        # point is only that omitting it can't produce an empty title or id.
        assert run_notify("hello")[:4] == ["--title", "notify", "--id", "notify"]


REPO_DIR = Path(__file__).resolve().parent.parent


def bash_scripts() -> "list[Path]":
    return [
        p
        for p in sorted(REPO_DIR.glob("pb-*"))
        if p.is_file() and b"bash" in p.open("rb").readline()
    ]


@pytest.mark.parametrize("script", bash_scripts(), ids=lambda p: p.name)
def test_bash_scripts_name_themselves_when_notifying(script: Path) -> None:
    """Bash callers must pass --from; nothing else can work out who they are."""
    for line in script.read_text().splitlines():
        if "/notify" in line and not line.lstrip().startswith("#"):
            assert '--from "$(basename "$0")"' in line, line


def test_found_some_bash_scripts() -> None:
    """Guard against the glob silently matching nothing."""
    assert len(bash_scripts()) > 5
