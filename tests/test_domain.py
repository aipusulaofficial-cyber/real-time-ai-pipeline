import math

import pytest

from pipeline_domain import Sample, Window


def test_window_evicts_expired_samples() -> None:
    window = Window(10)
    window.add(Sample("a", 2, 0))
    window.add(Sample("a", 4, 5))
    window.add(Sample("a", 8, 12))
    assert len(window) == 2
    assert window.aggregate("a") == 6


def test_sample_rejects_invalid_values() -> None:
    with pytest.raises(ValueError):
        Sample("", 1, 0)
    with pytest.raises(ValueError):
        Sample("a", float("nan"), 0)
    with pytest.raises(ValueError):
        Sample("a", 1, float("inf"))


def test_window_rejects_invalid_configuration() -> None:
    with pytest.raises(ValueError, match="positive and finite"):
        Window(0)
    with pytest.raises(ValueError, match="positive and finite"):
        Window(math.inf)
    with pytest.raises(ValueError, match="positive"):
        Window(10, max_samples=0)


def test_window_rejects_out_of_order_samples() -> None:
    window = Window(10)
    window.add(Sample("a", 1, 2))
    with pytest.raises(ValueError, match="out-of-order"):
        window.add(Sample("a", 2, 1))


def test_window_enforces_capacity_after_expiry() -> None:
    window = Window(10, max_samples=1)
    window.add(Sample("a", 1, 0))
    window.add(Sample("a", 2, 11))
    assert len(window) == 1
    assert window.aggregate("a") == 2


def test_window_enforces_capacity_for_live_samples() -> None:
    window = Window(10, max_samples=1)
    window.add(Sample("a", 1, 0))
    with pytest.raises(OverflowError, match="capacity"):
        window.add(Sample("a", 2, 1))


def test_aggregate_returns_zero_for_unknown_key() -> None:
    window = Window(10)
    window.add(Sample("a", 2, 0))
    assert window.aggregate("missing") == 0.0


def test_aggregate_rejects_blank_key() -> None:
    with pytest.raises(ValueError, match="aggregation key"):
        Window(10).aggregate(" ")
