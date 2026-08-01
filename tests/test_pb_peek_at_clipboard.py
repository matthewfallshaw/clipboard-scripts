"""Tests for pb-peek-at-clipboard and pb-peek-at-clipboard-sticky."""

from __future__ import annotations

from conftest import load_script

peek = load_script("pb-peek-at-clipboard")
peek_sticky = load_script("pb-peek-at-clipboard-sticky")

is_long = peek.is_long
LONG_MESSAGE_LENGTH = peek.LONG_MESSAGE_LENGTH


class TestLongMessageLength:
    def test_constant_value(self) -> None:
        assert LONG_MESSAGE_LENGTH == 100


class TestIsLong:
    def test_empty_string_not_long(self) -> None:
        assert not is_long("")

    def test_short_string_not_long(self) -> None:
        assert not is_long("hello")

    def test_exactly_at_limit_not_long(self) -> None:
        assert not is_long("x" * LONG_MESSAGE_LENGTH)

    def test_one_over_limit_is_long(self) -> None:
        assert is_long("x" * (LONG_MESSAGE_LENGTH + 1))

    def test_well_over_limit_is_long(self) -> None:
        assert is_long("x" * 500)


class TestPeekAtClipboardStickyLoads:
    def test_module_imports_cleanly(self) -> None:
        # pb-peek-at-clipboard-sticky always notifies sticky and has no
        # decision logic of its own; the meaningful assertion here is simply
        # that importing it (without running its __main__ block) succeeds.
        assert hasattr(peek_sticky, "notify")
        assert hasattr(peek_sticky, "paste")
