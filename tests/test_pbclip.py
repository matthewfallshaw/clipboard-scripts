"""Tests for lib/pbclip.py -- clipboard access and user notification.

subprocess.run is mocked throughout: these tests must never actually invoke
lib/notify, which could fire a real notification.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import MagicMock

from conftest import always

if TYPE_CHECKING:
    import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

import pbclip


class TestNotify:
    def test_command_starts_with_notify_script(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(sys, "argv", ["/repo/pb-example"])
        mock_run = MagicMock()
        monkeypatch.setattr(pbclip.subprocess, "run", mock_run)

        pbclip.notify("hello")

        command = mock_run.call_args[0][0]
        assert command[0] == str(pbclip.NOTIFY_SCRIPT)

    def test_from_is_the_calling_scripts_basename(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(sys, "argv", ["/repo/bin/pb-example", "some", "args"])
        mock_run = MagicMock()
        monkeypatch.setattr(pbclip.subprocess, "run", mock_run)

        pbclip.notify("hello")

        command = mock_run.call_args[0][0]
        assert command[1:3] == ["--from", "pb-example"]

    def test_sticky_false_by_default(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(sys, "argv", ["pb-example"])
        mock_run = MagicMock()
        monkeypatch.setattr(pbclip.subprocess, "run", mock_run)

        pbclip.notify("hello")

        assert "--sticky" not in mock_run.call_args[0][0]

    def test_sticky_true_adds_sticky_flag(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(sys, "argv", ["pb-example"])
        mock_run = MagicMock()
        monkeypatch.setattr(pbclip.subprocess, "run", mock_run)

        pbclip.notify("hello", sticky=True)

        assert "--sticky" in mock_run.call_args[0][0]

    def test_nothing_is_persisted_by_default(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # lib/notify is private unless asked otherwise, so the default is to
        # send no flag at all rather than to opt out of one.
        monkeypatch.setattr(sys, "argv", ["pb-example"])
        mock_run = MagicMock()
        monkeypatch.setattr(pbclip.subprocess, "run", mock_run)

        pbclip.notify("hello")

        assert "--persist" not in mock_run.call_args[0][0]

    def test_persist_true_adds_persist_flag(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(sys, "argv", ["pb-example"])
        mock_run = MagicMock()
        monkeypatch.setattr(pbclip.subprocess, "run", mock_run)

        pbclip.notify("hello", persist=True)

        assert "--persist" in mock_run.call_args[0][0]

    def test_message_follows_a_separator(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # `--` guards a message that happens to start with '-' (or match one
        # of lib/notify's own flag names) from being parsed as an option.
        monkeypatch.setattr(sys, "argv", ["pb-example"])
        mock_run = MagicMock()
        monkeypatch.setattr(pbclip.subprocess, "run", mock_run)

        pbclip.notify("--persist")

        assert mock_run.call_args[0][0][-2:] == ["--", "--persist"]

    def test_never_raises_on_a_nonzero_exit(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(sys, "argv", ["pb-example"])
        mock_run = MagicMock()
        monkeypatch.setattr(pbclip.subprocess, "run", mock_run)

        pbclip.notify("hello")

        assert mock_run.call_args.kwargs["check"] is False


class TestTransform:
    def test_passes_sticky_and_persist_through_to_notify(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(pbclip, "paste", lambda: "clipboard text")
        monkeypatch.setattr(pbclip, "copy", always(None))
        mock_notify = MagicMock()
        monkeypatch.setattr(pbclip, "notify", mock_notify)

        pbclip.transform(lambda text: text.upper(), sticky=True, persist=True)

        mock_notify.assert_called_once_with("CLIPBOARD TEXT", sticky=True, persist=True)

    def test_sticky_and_persist_default_to_false(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(pbclip, "paste", lambda: "clipboard text")
        monkeypatch.setattr(pbclip, "copy", always(None))
        mock_notify = MagicMock()
        monkeypatch.setattr(pbclip, "notify", mock_notify)

        pbclip.transform(lambda text: text)

        mock_notify.assert_called_once_with(
            "clipboard text", sticky=False, persist=False
        )

    def test_notify_result_false_skips_notify_entirely(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(pbclip, "paste", lambda: "clipboard text")
        monkeypatch.setattr(pbclip, "copy", always(None))
        mock_notify = MagicMock()
        monkeypatch.setattr(pbclip, "notify", mock_notify)

        pbclip.transform(lambda text: text, notify_result=False)

        mock_notify.assert_not_called()
