"""Tests for pb-random-number."""

import random

from conftest import load_script

mod = load_script("pb-random-number")
random_number = mod.random_number
DEFAULT_MAXIMUM = mod.DEFAULT_MAXIMUM


class TestRandomNumber:
    def test_default_maximum_is_999999(self) -> None:
        assert DEFAULT_MAXIMUM == 999999

    def test_within_range_default(self) -> None:
        for _ in range(200):
            n = random_number()
            assert 1 <= n <= DEFAULT_MAXIMUM

    def test_within_range_custom_maximum(self) -> None:
        for _ in range(200):
            n = random_number(10)
            assert 1 <= n <= 10

    def test_maximum_of_one_always_returns_one(self) -> None:
        assert random_number(1) == 1

    def test_deterministic_with_seeded_rng(self) -> None:
        rng1 = random.Random(42)
        rng2 = random.Random(42)
        assert random_number(1000, rng=rng1) == random_number(1000, rng=rng2)

    def test_result_is_int(self) -> None:
        assert isinstance(random_number(100), int)
