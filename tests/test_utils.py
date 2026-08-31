"""Tests for the formatting helpers."""

from __future__ import annotations

import pytest

from pchealth.utils import human_duration, human_size


@pytest.mark.parametrize(
    "num,expected",
    [
        (0, "0 B"),
        (512, "512 B"),
        (1024, "1.0 KB"),
        (1536, "1.5 KB"),
        (1024 ** 2, "1.0 MB"),
        (int(1.5 * 1024 ** 3), "1.5 GB"),
        (1024 ** 4, "1.0 TB"),
    ],
)
def test_human_size(num, expected):
    assert human_size(num) == expected


def test_human_size_negative():
    assert human_size(-2048) == "-2.0 KB"


@pytest.mark.parametrize(
    "seconds,expected",
    [
        (None, "unknown"),
        (-1, "unknown"),
        (0, "0m"),
        (90, "1m"),
        (3600, "1h 00m"),
        (5400, "1h 30m"),
    ],
)
def test_human_duration(seconds, expected):
    assert human_duration(seconds) == expected
