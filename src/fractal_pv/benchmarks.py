"""Standard liquidity and microstructure benchmarks for comparison against CII.

This module implements established liquidity-state estimators from the market
microstructure literature. They are used as controls in the horse race that
extends Section H4 of the main manuscript, testing whether the Coupling
Intensity Index contributes orthogonal predictive information or is subsumed
by simpler measures.

Citations are attached to each estimator. Edge cases that appear routinely
in daily OHLCV panels (non-negative Roll covariance, degenerate alpha in
Corwin-Schultz, zero-volume days) are handled explicitly rather than silenced.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Roll (1984) implicit bid-ask spread
# ---------------------------------------------------------------------------

def roll_spread(prices: pd.Series, window: int = 21) -> pd.Series:
    """Roll's effective spread estimator from the serial covariance of returns.

    Citation:
        Roll, R. (1984). "A Simple Implicit Measure of the Effective Bid-Ask
        Spread in an Efficient Market." Journal of Finance 39(4), 1127-1139.

    Formula:
        S = 2 * sqrt(-Cov(Δp_t, Δp_{t-1}))

    The estimator exploits the negative serial covariance induced by bounces
    between bid and ask. When the empirical covariance is non-negative (common
    in liquid samples or short windows), the spread is undefined; this
    implementation returns NaN for such periods rather than fabricating a zero.

    Parameters
    ----------
    prices : pd.Series
        Close prices, indexed by date.
    window : int
        Rolling window length in trading days.

    Returns
    -------
    pd.Series
        Rolling Roll spread estimates. NaN where covariance is non-negative.
    """
    log_returns = np.log(prices).diff()

    def _estimate(window_returns: np.ndarray) -> float:
        if len(window_returns) < 3 or np.any(np.isnan(window_returns)):
            return np.nan
        r_t = window_returns[1:]
        r_tm1 = window_returns[:-1]
        cov = np.cov(r_tm1, r_t, ddof=1)[0, 1]
        if cov >= 0:
            return np.nan
        return 2.0 * np.sqrt(-cov)

    return log_returns.rolling(window).apply(_estimate, raw=True)


# ---------------------------------------------------------------------------
# Corwin & Schultz (2012) high-low spread
# ---------------------------------------------------------------------------

def corwin_schultz_spread(
    high: pd.Series,
    low: pd.Series,
    window: int = 21,
) -> pd.Series:
    """Corwin-Schultz bid-ask spread from daily high and low prices.

    Citation:
        Corwin, S. A., & Schultz, P. (2012). "A Simple Way to Estimate Bid-Ask
        Spreads from Daily High and Low Prices." Journal of Finance 67(2),
        719-760.

    The estimator rests on two observations. First, the daily high-low ratio
    reflects both volatility and the spread; second, volatility scales with
    the time interval while spread does not. Comparing the single-day high-low
    to the two-day high-low isolates the spread.

    Let H_i, L_i denote daily high and low. The estimator computes:

        β  = [log(H_t / L_t)]² + [log(H_{t+1} / L_{t+1})]²
        γ  = [log(H_{t,t+1} / L_{t,t+1})]²
        k  = 3 - 2·sqrt(2)
        α  = (sqrt(2β) - sqrt(β)) / k  -  sqrt(γ / k)
        S  = 2·(exp(α) - 1) / (1 + exp(α))

    Negative α values produce negative spread estimates; following the authors'
    recommendation, these are floored at zero rather than discarded, because a
    zero spread is a legitimate interpretation of a highly efficient market.

    Parameters
    ----------
    high, low : pd.Series
        Daily high and low prices, indexed by date, strictly positive.
    window : int
        Rolling window over which to average the two-day pairwise estimates.

    Returns
    -------
    pd.Series
        Rolling average Corwin-Schultz spread.
    """
    log_h = np.log(high)
    log_l = np.log(low)

    beta_single = (log_h - log_l) ** 2
    beta = beta_single + beta_single.shift(1)

    h_two = np.maximum(log_h, log_h.shift(1))
    l_two = np.minimum(log_l, log_l.shift(1))
    gamma = (h_two - l_two) ** 2

    k = 3.0 - 2.0 * np.sqrt(2.0)

    alpha = (np.sqrt(2.0 * beta) - np.sqrt(beta)) / k - np.sqrt(gamma / k)

    spread = 2.0 * (np.exp(alpha) - 1.0) / (1.0 + np.exp(alpha))

    # Floor negative values per Corwin & Schultz recommendation.
    spread = spread.where(spread > 0, 0.0)

    # Replace infinities from division blowups.
    spread = spread.replace([np.inf, -np.inf], np.nan)

    return spread.rolling(window).mean()


# ---------------------------------------------------------------------------
# Amihud (2002) illiquidity ratio
# ---------------------------------------------------------------------------

def amihud_illiquidity(
    returns: pd.Series,
    dollar_volume: pd.Series,
    window: int = 21,
) -> pd.Series:
    """Amihud illiquidity ratio, rolling window.

    Citation:
        Amihud, Y. (2002). "Illiquidity and stock returns: cross-section and
        time-series effects." Journal of Financial Markets 5(1), 31-56.

    Formula (rolling D-day version):
        ILLIQ_t = (1/D) · Σ_{τ=t-D+1}^{t} |r_τ| / DVol_τ

    Measures the average absolute return per unit of dollar volume, a proxy
    for price impact. Large values indicate illiquid assets where a given
    trade moves prices substantially.

    Parameters
    ----------
    returns : pd.Series
        Daily log-returns or arithmetic returns. Convention should be
        consistent with the broader pipeline.
    dollar_volume : pd.Series
        Daily dollar volume (price × shares traded). If only share volume is
        available, pass that instead and interpret the output accordingly.
    window : int
        Rolling window in trading days.

    Returns
    -------
    pd.Series
        Rolling Amihud illiquidity. Zero-volume days produce infinities which
        are replaced with NaN before averaging.
    """
    daily = returns.abs() / dollar_volume
    daily = daily.replace([np.inf, -np.inf], np.nan)
    return daily.rolling(window, min_periods=max(5, window // 4)).mean()


# ---------------------------------------------------------------------------
# Turnover (normalized)
# ---------------------------------------------------------------------------

def normalized_turnover(
    volume: pd.Series,
    window: int = 20,
) -> pd.Series:
    """Abnormal turnover: current volume relative to trailing mean.

    Computing true turnover (volume ÷ shares outstanding) requires a
    fundamentals source that yfinance does not provide consistently across
    the sample period. This normalized proxy captures the same signal in a
    scale-free way: values above one indicate heavier-than-usual trading.

    Parameters
    ----------
    volume : pd.Series
        Daily share volume.
    window : int
        Trailing window length (default 20 trading days, roughly one month).

    Returns
    -------
    pd.Series
        Ratio of current volume to trailing-window mean. The trailing mean
        is shifted by one day to avoid contemporaneous leakage.
    """
    trailing = volume.rolling(window).mean().shift(1)
    # Guard against division by zero.
    trailing = trailing.replace(0, np.nan)
    return volume / trailing


# ---------------------------------------------------------------------------
# Volatility of volatility
# ---------------------------------------------------------------------------

def volatility_of_volatility(
    returns: pd.Series,
    rv_window: int = 21,
    vov_window: int = 63,
) -> pd.Series:
    """Realized volatility of realized volatility.

    A second-moment measure of uncertainty: how much does the volatility
    regime itself vary? High vol-of-vol tends to precede regime transitions
    and has been documented as a risk factor in its own right (Cboe VVIX
    index captures the analogous quantity at the market level).

    This is included as a control because intensifying information flow
    could reasonably increase both CII and vol-of-vol simultaneously, so a
    horse race that does not partial-out vol-of-vol risks misattribution.

    Parameters
    ----------
    returns : pd.Series
        Daily log-returns.
    rv_window : int
        Window for realized volatility (default 21 trading days ≈ 1 month).
    vov_window : int
        Window for standard deviation of the RV series (default 63 ≈ 3 months).

    Returns
    -------
    pd.Series
        Rolling vol-of-vol, annualized at the RV stage.
    """
    rv = returns.rolling(rv_window).std() * np.sqrt(252.0)
    return rv.rolling(vov_window).std()


# ---------------------------------------------------------------------------
# Convenience: all benchmarks for a single ticker
# ---------------------------------------------------------------------------

def compute_all_benchmarks(
    df: pd.DataFrame,
    window: int = 21,
    price_col: str = "Close",
    high_col: str = "High",
    low_col: str = "Low",
    volume_col: str = "Volume",
) -> pd.DataFrame:
    """Run every benchmark estimator on a single ticker's OHLCV frame.

    Expects a DataFrame indexed by date with the standard yfinance columns
    (Close, High, Low, Volume). Returns a DataFrame with one column per
    benchmark, aligned on the original index.

    The horse race regression in `inference_robust.py` will merge this output
    with the CII and rolling-Hurst panel before estimating coefficients.

    Parameters
    ----------
    df : pd.DataFrame
        OHLCV data.
    window : int
        Common rolling window for spread-based measures.
    price_col, high_col, low_col, volume_col : str
        Column names in the input DataFrame.

    Returns
    -------
    pd.DataFrame
        Columns: roll_spread, corwin_schultz, amihud, turnover, vol_of_vol.
    """
    prices = df[price_col]
    returns = np.log(prices).diff()
    dollar_volume = prices * df[volume_col]

    result = pd.DataFrame(index=df.index)
    result["roll_spread"] = roll_spread(prices, window=window)
    result["corwin_schultz"] = corwin_schultz_spread(
        df[high_col], df[low_col], window=window
    )
    result["amihud"] = amihud_illiquidity(returns, dollar_volume, window=window)
    result["turnover"] = normalized_turnover(df[volume_col], window=window)
    result["vol_of_vol"] = volatility_of_volatility(returns)

    return result
