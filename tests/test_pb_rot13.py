"""Tests for pb-rot13."""

from conftest import load_script

mod = load_script("pb-rot13")
rot13 = mod.rot13


class TestRot13:
    def test_lowercase(self) -> None:
        assert rot13("hello") == "uryyb"

    def test_uppercase(self) -> None:
        assert rot13("HELLO") == "URYYB"

    def test_mixed_case(self) -> None:
        assert rot13("Hello, World!") == "Uryyb, Jbeyq!"

    def test_non_letters_untouched(self) -> None:
        assert rot13("123 !@# .,-") == "123 !@# .,-"

    def test_unicode_untouched(self) -> None:
        assert rot13("café") == "pnsé"

    def test_empty_string(self) -> None:
        assert rot13("") == ""

    def test_multiline(self) -> None:
        assert rot13("line one\nline two") == "yvar bar\nyvar gjb"

    def test_is_involution(self) -> None:
        # ROT13 applied twice returns the original text.
        text = "The Quick Brown Fox, 123!"
        assert rot13(rot13(text)) == text


class TestScriptWiring:
    def test_uses_sticky_notification(self) -> None:
        # The old Ruby used clipboard(true) { ... } for a sticky notification;
        # the __main__ block must pass sticky=True to transform().
        import ast
        from pathlib import Path

        source = Path(mod.__file__).read_text()
        tree = ast.parse(source)
        calls = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "transform"
        ]
        assert calls, "expected a call to transform() in pb-rot13"
        sticky_kwargs = [
            kw for call in calls for kw in call.keywords if kw.arg == "sticky"
        ]
        assert sticky_kwargs, "expected transform(..., sticky=True)"
        assert all(
            isinstance(kw.value, ast.Constant) and kw.value.value is True
            for kw in sticky_kwargs
        )
