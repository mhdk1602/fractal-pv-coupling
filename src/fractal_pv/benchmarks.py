"""Standard liquidity and microstructure benchmarks for comparison against CII.

This module implements established liquidity-state estimators from the market
microstructure literature. They are used as controls in the horse race that
extends Section H4 of the main manuscript, testing whether the Coupling
Intensity Index contributes orthogonal predictive information or is subsumed
by simpler measures.

Citation conventions follow the published literature rather than working-paper
drafts. Equation numbers reference the Journal of Finance versions of Roll
(1984) and Corwin-Schultz (2012), and the Journal of Financial Markets
version of Amihud (2002).

Primary references:
    Amihud, Y. (2002). "Illiquidity and stock returns: cross-section and
        time-series effects." Journal of Financial Markets 5(1), 31-56.
    Corwin, S. A., & Schultz, P. (2012). "A Simple Way to Estimate Bid-Ask
        Spreads from Daily High and Low Prices." Journal of Finance 67(2),
        719-760.
    Roll, R. (1984). "A Simple Implicit Measure of the Effective Bid-Ask
        Spread in an Efficient Market." Journal of Finance 39(4), 1127-1139.

Convention references:
    Abdi, F., & Ranaldo, A. (2017). "A Simple Estimation of Bid-Ask Spreads
        from Daily Close, High, and Low Prices." Review of Financial
        Studies 30(12), 4437-4480.
    Goyenko, R. Y., Holden, C. W., & Trzcinka, C. A. (2009). "Do liquidity
        measures measure liquidity?" Journal of Financial Economics 92(2),
        153-181.
    Hasbrouck, J. (2009). "Trading Costs and Returns for U.S. Equities:
        Estimating Effective Costs from Daily Data." Journal of Finance
        64(3), 1445-1477.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Roll (1984) implicit bid-ask spread
# ---------------------------------------------------------------------------

def roll_spread(prices: pd.Series, window: int = 21) -> pd.Series:
    """Roll's effective spread from the serial covariance of returns.

    Roll's theoretical derivation on p. 1129 is in first differences of price,
    Δp_t, yielding a dollar spread. His empirical implementation (p. 1130 and
    footnote 5) uses arithmetic percentage returns R_t = Δp_t / p_{t-1},
    yielding a proportional spread with O(s²) bias that Roll himself
    characterizes as negligible for typical values. Equation (3) on p. 1134
    summarizes the empirical estimator as s = 2·sqrt(-Cov).

    This implementation uses log returns, which are numerically equivalent to
    arithmetic returns at daily frequency up to third order and are the
    modern convention popularized by Hasbrouck (2009, eq. 1, p. 1447) and
    adopted in Abdi-Ranaldo (2017, footnote 6). The output is therefore a
    proportional effective spread, directly comparable in units to the
    Corwin-Schultz estimator and the Amihud ratio.

    When the empirical serial covariance is non-negative, four conventions
    coexist in the literature:
        (i)   Roll (1984) himself reports signed negative spreads in Table I
        (ii)  Zero-flooring, modal in modern work: Goyenko-Holden-Trzcinka
              (2009), Corwin-Schultz (2012), and analogous to Hasbrouck's
              (2009) truncated-normal Gibbs prior
        (iii) Absolute-value 2·sqrt(|Cov|), attributed in the later
              literature to Harris (1990) (see Lesmond 2005; Abdi-Ranaldo
              2017, footnote 6), though Harris himself documents the
              sampling-noise problem and proposes the French-Roll variance
              estimator rather than the |·| trick
        (iv)  The Hasbrouck (2009) Gibbs sampler with a truncated-normal
              prior N⁺(0, 0.05²)

    This implementation adopts convention (ii), zero-flooring, citing
    Goyenko-Holden-Trzcinka (2009) and Corwin-Schultz (2012) as precedent.
    Hasbrouck (2009, p. 1456) reports this affects roughly one-third of
    firm-years in typical samples.

    Parameters
    ----------
    prices : pd.Series
        Close prices, indexed by date.
    window : int
        Rolling window length in trading days.

    Returns
    -------
    pd.Series
        Rolling Roll proportional effective spread. Zero where the window's
        empirical serial covariance of log returns is non-negative. NaN
        where the window has fewer than three valid observations.
    """
    log_returns = np.log(prices).diff()

    def _estimate(window_returns: np.ndarray) -> float:
        if len(window_returns) < 3 or np.any(np.isnan(window_returns)):
            return np.nan
        r_t = window_returns[1:]
        r_tm1 = window_returns[:-1]
        cov = np.cov(r_tm1, r_t, ddof=1)[0, 1]
        if cov >= 0:
            # Zero-floor per Goyenko-Holden-Trzcinka (2009) and
            # Corwin-Schultz (2012). See module docstring for the four
            # alternative conventions.
            return 0.0
        return 2.0 * np.sqrt(-cov)

    return log_returns.rolling(window).apply(_estimate, raw=True)


# ---------------------------------------------------------------------------
# Corwin & Schultz (2012) high-low spread
# ---------------------------------------------------------------------------

def _apply_overnight_adjustment(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
) -> tuple[pd.Series, pd.Series]:
    """Corwin-Schultz Section II.A overnight-return adjustment.

    When the prior close C_{t-1} falls below the current day's low L_t, the
    day's (H_t, L_t) are both reduced by (L_t - C_{t-1}). When the prior
    close exceeds the current day's high H_t, both are raised by
    (C_{t-1} - H_t). This is the "close-to-low" / "close-to-high" method in
    the Internet Appendix Table IA.II; the open price is explicitly rejected
    in the paper for reasons enumerated in Section II.A.

    Note the asymmetric use in the β formula: current day's H/L take the
    overnight-adjusted values; the lagged H/L use the raw previous day.
    This is a deliberate rolling-window convention in the authors' SAS code,
    not an oversight.
    """
    prev_close = close.shift(1)

    # Case 1: prior close below current low — shift range down.
    below = prev_close < low
    shift_down = (low - prev_close).where(below, 0.0)

    # Case 2: prior close above current high — shift range up.
    above = prev_close > high
    shift_up = (prev_close - high).where(above, 0.0)

    h_adj = high - shift_down + shift_up
    l_adj = low - shift_down + shift_up

    return h_adj, l_adj


def corwin_schultz_mspread0(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    window: int = 21,
    min_obs: int = 12,
) -> pd.Series:
    """Corwin-Schultz spread, primary variant (SAS: MSPREAD_0).

    This is the authors' primary published estimator: overnight-adjusted
    high and low, negative two-day spreads zeroed at the daily level before
    averaging, and a minimum-observations filter on the window. Abdi-Ranaldo
    (2017) formalize the SAS variable taxonomy and treat MSPREAD_0 as the
    canonical Corwin-Schultz spread.

    Formulation follows the published Journal of Finance paper:
        β = [ln(H_t/L_t)]² + [ln(H_{t-1}/L_{t-1})]²               (eq. 9)
        γ = [ln(H_{t,t-1} / L_{t,t-1})]²                          (eq. 11)
            where H_{t,t-1} = max(H_t, H_{t-1}), L_{t,t-1} = min
        k = 3 - 2·sqrt(2)
        α = (sqrt(2β) - sqrt(β)) / k  -  sqrt(γ / k)              (eq. 14)
        S = 2·(exp(α) - 1) / (1 + exp(α))                         (eq. 18)

    The constant k enters both α terms but in different algebraic positions:
    external divisor in the first term, internal divisor under the radical
    in the second. The implementation below preserves this.

    Section II.C: "we set all negative two-day spreads to zero before
    calculating monthly averages." The primary SAS variable is
    SPREAD_0 = max(SPREAD, 0), not NaN and not kept negative. Corwin's 2019
    note ("Dealing with Negative Values in the High-Low Spread Estimator")
    explicitly warns that skipping this step produces negative average
    spreads as in Kim & Lee (2014).

    The paper works on calendar-month boundaries with a minimum-12-observation
    filter (SAS: IF N1>=12). This implementation uses a rolling trading-day
    window instead, because the horse-race regression needs daily values.
    The min_obs argument applies the analogous filter to each rolling window.

    The SAS code additionally drops any day with H/L > 8 as a final screen
    (not in the published paper). This is an implementation-level detail
    flagged here for completeness; the implementation below does not apply
    this screen, on the grounds that the 50 S&P 500 tickers in the study
    sample are unlikely to hit this threshold.

    Output is a proportional (percentage) effective spread, comparable in
    units to the Roll proportional spread and the Amihud ratio.

    Parameters
    ----------
    high, low : pd.Series
        Daily high and low prices, strictly positive.
    close : pd.Series
        Daily close prices, used for the overnight adjustment.
    window : int
        Rolling window length in trading days (default 21).
    min_obs : int
        Minimum valid two-day estimates within the window (default 12).

    Returns
    -------
    pd.Series
        Rolling MSPREAD_0 proportional effective spread.
    """
    h_adj, l_adj = _apply_overnight_adjustment(high, low, close)
    log_h = np.log(h_adj)
    log_l = np.log(l_adj)

    # β uses overnight-adjusted current day, raw (unshifted) lagged day,
    # per the authors' SAS convention.
    log_h_raw = np.log(high)
    log_l_raw = np.log(low)

    beta_current = (log_h - log_l) ** 2
    beta_lagged = (log_h_raw.shift(1) - log_l_raw.shift(1)) ** 2
    beta = beta_current + beta_lagged

    # γ uses max/min across the two days, overnight-adjusted.
    h_two = np.maximum(log_h, log_h.shift(1))
    l_two = np.minimum(log_l, log_l.shift(1))
    gamma = (h_two - l_two) ** 2

    k = 3.0 - 2.0 * np.sqrt(2.0)
    alpha = (np.sqrt(2.0 * beta) - np.sqrt(beta)) / k - np.sqrt(gamma / k)

    spread = 2.0 * (np.exp(alpha) - 1.0) / (1.0 + np.exp(alpha))

    # MSPREAD_0: daily zero-flooring before averaging (Section II.C).
    spread = spread.where(spread > 0, 0.0)
    spread = spread.replace([np.inf, -np.inf], np.nan)

    return spread.rolling(window, min_periods=min_obs).mean()


def corwin_schultz_xspread0(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    window: int = 21,
    min_obs: int = 12,
) -> pd.Series:
    """Corwin-Schultz spread, alternative variant (SAS: XSPREAD_0).

    The "monthly corrected" alternative from the same paper. Negative daily
    spreads are retained through the averaging step; the zero-floor is
    applied only to the resulting monthly (here: rolling-window) mean.
    Lower bias in simulation, though Corwin-Schultz and Abdi-Ranaldo (2017)
    report weaker TAQ correlation than MSPREAD_0.

    Included as a robustness check. MSPREAD_0 should be the primary
    specification in the horse race regression.
    """
    h_adj, l_adj = _apply_overnight_adjustment(high, low, close)
    log_h = np.log(h_adj)
    log_l = np.log(l_adj)
    log_h_raw = np.log(high)
    log_l_raw = np.log(low)

    beta = (log_h - log_l) ** 2 + (log_h_raw.shift(1) - log_l_raw.shift(1)) ** 2

    h_two = np.maximum(log_h, log_h.shift(1))
    l_two = np.minimum(log_l, log_l.shift(1))
    gamma = (h_two - l_two) ** 2

    k = 3.0 - 2.0 * np.sqrt(2.0)
    alpha = (np.sqrt(2.0 * beta) - np.sqrt(beta)) / k - np.sqrt(gamma / k)
    spread = 2.0 * (np.exp(alpha) - 1.0) / (1.0 + np.exp(alpha))
    spread = spread.replace([np.inf, -np.inf], np.nan)

    # XSPREAD_0: keep negatives through the average, zero-floor at the end.
    averaged = spread.rolling(window, min_periods=min_obs).mean()
    return averaged.where(averaged > 0, 0.0)


# Back-compat alias for callers that reference the old name.
corwin_schultz_spread = corwin_schultz_mspread0


# ---------------------------------------------------------------------------
# Amihud (2002) illiquidity ratio
# ---------------------------------------------------------------------------

def amihud_illiquidity(
    returns: pd.Series,
    dollar_volume: pd.Series,
    window: int = 21,
    scale: float = 1e6,
) -> pd.Series:
    """Amihud illiquidity ratio, rolling window with dollar-volume scaling.

    Amihud (2002, eq. 1, p. 34) defines the measure as:

        ILLIQ_{iy} = (1/D_{iy}) · Σ_{d=1}^{D} |R_{iyd}| / VOLD_{iyd}

    where VOLD is "the respective daily volume in dollars" (text preceding
    eq. 1). On p. 37 Amihud reports the measure "multiplied by 10⁶"; the
    Table 1 NYSE 1963-1996 mean of 0.337 is consistent with this convention.

    The measure captures average absolute return per unit of dollar volume,
    a proxy for Kyle's lambda price-impact parameter. Large values indicate
    illiquid assets where a given trade moves prices substantially.

    Dollar-volume scaling is used rather than share-volume because:
        1. Goyenko-Holden-Trzcinka (2009, Section 5.2) treat dollar volume
           as the standard in the "Extended Amihud class" of measures
        2. Fong-Holden-Trzcinka (2017) confirm dollar-volume Amihud as the
           best monthly cost-per-dollar-volume proxy globally (p. 1355)
        3. Hasbrouck (2009) uses dollar volume in his Amihud analog (I₂),
           though he applies a √ transform to control skewness
        4. Horse-race comparability requires a dollar-denominated target;
           share-volume Amihud is not comparable to TAQ Kyle's λ

    Users running a cross-sectional regression with ILLIQ as a regressor
    should add a control for ln(size). Amihud's own Table 1 reports a
    correlation of -0.614 between ILLIQ and ln(market cap) in his NYSE
    sample; Cochrane (2005) and Florakis-Gregoriou-Kostakis (2011) discuss
    this mechanical size-loading issue.

    NASDAQ volume is inflated by interdealer trades. For NASDAQ samples,
    standard practice is to deflate reported volume by 0.5 before computing
    Amihud. Not implemented here because the 50 S&P 500 tickers in the
    study sample mix NYSE and NASDAQ, and the mechanical scaling difference
    is small relative to the effect size we are looking for in the horse
    race. Flagged as a future refinement.

    Parameters
    ----------
    returns : pd.Series
        Daily arithmetic or log returns; convention should be consistent
        with the broader pipeline (log returns in our case).
    dollar_volume : pd.Series
        Daily dollar volume (close × shares traded).
    window : int
        Rolling window in trading days.
    scale : float
        Multiplicative scaling factor (default 1e6, matching Amihud 2002
        p. 37 and GHT 2009 convention). Output units are therefore
        10⁻⁶ × |return| / dollar.

    Returns
    -------
    pd.Series
        Rolling scaled Amihud illiquidity. Zero-volume days produce
        infinities which are replaced with NaN before averaging.
    """
    daily = returns.abs() / dollar_volume
    daily = daily.replace([np.inf, -np.inf], np.nan)
    averaged = daily.rolling(window, min_periods=max(5, window // 4)).mean()
    return averaged * scale


# ---------------------------------------------------------------------------
# Turnover (normalized)
# ---------------------------------------------------------------------------

def normalized_turnover(
    volume: pd.Series,
    window: int = 20,
) -> pd.Series:
    """Abnormal turnover: current volume relative to trailing mean.

    True turnover (volume ÷ shares outstanding) requires a fundamentals
    source that yfinance does not provide consistently across the sample
    period. This normalized proxy captures the same signal in a scale-free
    way: values above one indicate heavier-than-usual trading.

    The trailing mean is shifted by one day to avoid contemporaneous leakage
    into the numerator.
    """
    trailing = volume.rolling(window).mean().shift(1)
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
    and has been documented as a priced risk factor (Cboe VVIX index
    captures the analogous quantity at the market-index level).

    Included as a horse-race control because intensifying information flow
    could reasonably raise both CII and vol-of-vol simultaneously. Omitting
    it risks misattribution of the CII coefficient.
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

    Primary variants are used throughout: MSPREAD_0 for Corwin-Schultz,
    zero-flooring for Roll, dollar-volume Amihud at 10⁶ scaling. The
    XSPREAD_0 robustness variant is available via corwin_schultz_xspread0().

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
    result["corwin_schultz"] = corwin_schultz_mspread0(
        df[high_col], df[low_col], prices, window=window
    )
    result["amihud"] = amihud_illiquidity(returns, dollar_volume, window=window)
    result["turnover"] = normalized_turnover(df[volume_col], window=window)
    result["vol_of_vol"] = volatility_of_volatility(returns)

    return result
