"""Regression tests for the rolling-window stamping convention.

The midpoint stamp is a documented look-ahead (see the `rolling_hurst` Notes
section and `research/lookahead/RESULT.md`). These tests pin the behaviour so a
future change to the convention is deliberate rather than accidental, and so the
documented offsets stay true.

Run: pytest tests/
"""

import numpy as np
import pandas as pd
import pytest

from fractal_pv.rolling import rolling_dual_hurst, rolling_hurst

W, STEP = 500, 20


@pytest.fixture(scope="module")
def series_and_dates():
    """Synthetic series long enough for several windows. No network, no cache."""
    rng = np.random.default_rng(7)
    n = 1200
    x = np.abs(np.cumsum(rng.standard_normal(n)) * 0.01 + rng.standard_normal(n) * 0.01)
    v = np.log(np.abs(rng.standard_normal(n)) * 1e6 + 1e5)
    dates = pd.bdate_range("2015-01-02", periods=n).values
    return x, v, dates


def test_default_stamp_is_midpoint(series_and_dates):
    x, _, dates = series_and_dates
    df = rolling_hurst(x, dates, window=W, step=STEP)
    expected = df["window_start"] + W // 2
    idx = pd.Index(dates).get_indexer(pd.to_datetime(df["date"]).values)
    assert (idx == expected).all()


def test_midpoint_stamp_precedes_window_end_by_249(series_and_dates):
    """The documented look-ahead. Changing this invalidates the manuscript note."""
    x, _, dates = series_and_dates
    df = rolling_hurst(x, dates, window=W, step=STEP)
    idx = pd.Index(dates).get_indexer(pd.to_datetime(df["date"]).values)
    trading_days_ahead = (df["window_end"] - 1) - idx
    assert (trading_days_ahead == W // 2 - 1).all()
    assert (trading_days_ahead == 249).all()


def test_right_stamp_lands_on_last_window_observation(series_and_dates):
    x, _, dates = series_and_dates
    df = rolling_hurst(x, dates, window=W, step=STEP, stamp="right")
    idx = pd.Index(dates).get_indexer(pd.to_datetime(df["date"]).values)
    assert (idx == df["window_end"] - 1).all()


def test_stamp_changes_labels_only_not_estimates(series_and_dates):
    """Re-stamping must be a pure relabel; research/lookahead relies on this."""
    x, _, dates = series_and_dates
    mid = rolling_hurst(x, dates, window=W, step=STEP)
    right = rolling_hurst(x, dates, window=W, step=STEP, stamp="right")
    assert np.allclose(mid["H"], right["H"], equal_nan=True)
    assert np.allclose(mid["r_squared"], right["r_squared"], equal_nan=True)
    assert (right["idx"] - mid["idx"] == W // 2 - 1).all()


def test_dual_hurst_threads_stamp_through(series_and_dates):
    x, v, dates = series_and_dates
    mid = rolling_dual_hurst(x, v, dates, window=W, step=STEP)
    right = rolling_dual_hurst(x, v, dates, window=W, step=STEP, stamp="right")
    assert len(mid) == len(right)
    assert np.allclose(mid["H_price"], right["H_price"], equal_nan=True)
    assert np.allclose(mid["H_volume"], right["H_volume"], equal_nan=True)
    shift = pd.to_datetime(right["date"]) - pd.to_datetime(mid["date"])
    assert (shift > pd.Timedelta(0)).all()


def test_unknown_stamp_rejected(series_and_dates):
    x, _, dates = series_and_dates
    with pytest.raises(ValueError, match="stamp must be"):
        rolling_hurst(x, dates, window=W, step=STEP, stamp="centre")


def test_short_series_returns_empty_frame():
    df = rolling_hurst(np.arange(100.0), window=W, step=STEP)
    assert df.empty
    assert list(df.columns) == ["date", "H", "r_squared", "window_start", "window_end"]
