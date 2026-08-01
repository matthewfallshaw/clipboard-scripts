"""Tests for pb-pwgen-pin PIN generation."""

from conftest import load_script

mod = load_script("pb-pwgen-pin")
generate_pin = mod.generate_pin


class TestGeneratePin:
    def test_length_is_four(self) -> None:
        assert len(generate_pin()) == 4

    def test_is_all_digits(self) -> None:
        assert generate_pin().isdigit()

    def test_is_zero_padded(self, monkeypatch) -> None:
        monkeypatch.setattr(mod.secrets, "randbelow", lambda n: 7)
        assert generate_pin() == "0007"

    def test_max_value(self, monkeypatch) -> None:
        monkeypatch.setattr(mod.secrets, "randbelow", lambda n: 9999)
        assert generate_pin() == "9999"

    def test_range_across_many_runs(self) -> None:
        for _ in range(200):
            pin = generate_pin()
            assert 0 <= int(pin) <= 9999
            assert len(pin) == 4
