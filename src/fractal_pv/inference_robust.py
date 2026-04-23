"""Robust inference for predictive regressions.

Addresses the referee concern that HC1 standard errors are insufficient given
overlapping rolling windows, generated regressors, and forward-looking targets.
This module provides:

    1. Firm-clustered SEs with t(G_firm − 1)
    2. Time-clustered SEs with t(G_month − 1)
    3. Two-way clustered SEs (firm + time) with t(min(G_firm, G_month) − 1),
       following Cameron, Gelbach & Miller (2011, JBES) and the
       reghdfe / fixest min-G convention
    4. Newey-West SEs on the pooled residual vector (flagged for replacement
       with Driscoll-Kraay in a later revision; see module NOTES below)
    5. Horse-race regression that accepts arbitrary regressor lists for
       comparison of CII against standard liquidity benchmarks

NOTES ON OUTSTANDING REFEREE-GRADE UPGRADES (Tier 3):

    - CGM (2011) §2.3 eigenvalue adjustment for non-PSD two-way sandwich;
      current implementation zero-floors negative diagonals, which breaks
      PSD for general Wald quadratic forms
    - Driscoll-Kraay SEs (Driscoll & Kraay 1998, REStat) for the daily
      panel, Bartlett bandwidth 21-42 per Hoechle (2007, Stata J.)
    - Bell-McCaffrey CR2 + Satterthwaite df (Imbens & Kolesár 2016, REStat);
      at G_firm ≈ 10 with unbalanced firms, Satterthwaite df typically
      falls in [3, 6], not 9
    - Wild cluster restricted (WCR) bootstrap p-values (Cameron-Gelbach-
      Miller 2008, REStat; MacKinnon-Webb 2017, JAE). Non-negotiable at
      G_firm ≈ 10 for publication; see `boottest` / `wildboottestpy`

The current implementation is adequate for internal horse-race evaluation
but the listed upgrades are required before journal submission of a
revision.
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from scipy import stats


# ---------------------------------------------------------------------------
# Core OLS and SE components
# ---------------------------------------------------------------------------

def _ols_core(X: np.ndarray, y: np.ndarray):
    """Core OLS estimation. Returns beta, residuals, (X'X)^{-1}, n, k."""
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    resid = y - X @ beta
    return beta, resid, XtX_inv, n, k


def _hc1_se(
    X: np.ndarray,
    resid: np.ndarray,
    XtX_inv: np.ndarray,
    k_effective: int,
) -> np.ndarray:
    """HC1 heteroskedasticity-consistent standard errors.

    Uses the weighted-X form X' diag(u²) X = (|u|·X)' (|u|·X) to avoid
    materializing the n×n diagonal matrix, per MacKinnon & White (1985).
    Small-sample factor n / (n − k_effective) where k_effective excludes
    absorbed fixed-effect rows.
    """
    n, _ = X.shape
    Xw = X * np.abs(resid)[:, None]
    meat = Xw.T @ Xw
    V = (n / (n - k_effective)) * XtX_inv @ meat @ XtX_inv
    return np.sqrt(np.diag(V))


def _clustered_se(
    X: np.ndarray,
    resid: np.ndarray,
    XtX_inv: np.ndarray,
    clusters: np.ndarray,
    k_effective: int,
) -> tuple[np.ndarray, int]:
    """Cluster-robust standard errors. Returns (se, G).

    Small-sample factor uses the min-G / reghdfe / fixest convention:
        c = [G / (G − 1)] · [(n − 1) / (n − k_effective)]

    Reference: Cameron & Miller (2015, JHR 50(2):317-372, eq. 12).
    Liang & Zeger (1986), Arellano (1987) for the core estimator.
    """
    n, _ = X.shape
    unique = np.unique(clusters)
    G = len(unique)

    meat = np.zeros_like(XtX_inv)
    for g in unique:
        mask = clusters == g
        score = X[mask].T @ resid[mask]
        meat += np.outer(score, score)

    if G <= 1:
        warnings.warn(
            "Cluster count G ≤ 1; small-sample correction is undefined. "
            "Returning unadjusted sandwich; inference is unreliable."
        )
        correction = 1.0
    else:
        correction = (G / (G - 1)) * ((n - 1) / (n - k_effective))

    V = correction * XtX_inv @ meat @ XtX_inv
    return np.sqrt(np.diag(V)), G


def _twoway_clustered_se(
    X: np.ndarray,
    resid: np.ndarray,
    XtX_inv: np.ndarray,
    clusters1: np.ndarray,
    clusters2: np.ndarray,
    k_effective: int,
) -> tuple[np.ndarray, int, int]:
    """Two-way cluster-robust SEs via V = V1 + V2 − V12.

    Reference: Cameron, Gelbach & Miller (2011, JBES 29(2):238-249);
    Thompson (2011, JFE 99:1-10).

    Uses the min-G convention (reghdfe / fixest) for the small-sample factor
    applied to each component.

    Non-PSD sandwich: if the resulting V has negative diagonal entries, the
    current implementation zero-floors them with a warning. This is a Tier-3
    upgrade target; CGM (2011) §2.3 eigenvalue adjustment is the correct
    fix but is deferred.
    """
    n, _ = X.shape

    def _component(cs):
        unique = np.unique(cs)
        G = len(unique)
        m = np.zeros_like(XtX_inv)
        for g in unique:
            mask = cs == g
            score = X[mask].T @ resid[mask]
            m += np.outer(score, score)
        c = (G / (G - 1)) * ((n - 1) / (n - k_effective)) if G > 1 else 1.0
        return c * XtX_inv @ m @ XtX_inv, G

    V1, G1 = _component(clusters1)
    V2, G2 = _component(clusters2)

    intersection = np.char.add(
        np.char.add(clusters1.astype(str), "_"),
        clusters2.astype(str),
    )
    V12, _ = _component(intersection)

    V = V1 + V2 - V12

    diag = np.diag(V).copy()
    if np.any(diag < 0):
        warnings.warn(
            f"Two-way CRVE has {(diag < 0).sum()} negative diagonal entry(ies); "
            f"min = {diag.min():.3g}. Zero-flooring; a CGM (2011) §2.3 "
            "eigenvalue adjustment is the proper fix and is planned as a "
            "Tier-3 upgrade. Interpret two-way SEs with caution until then."
        )
        diag = np.clip(diag, 0.0, None)

    return np.sqrt(diag), G1, G2


def _newey_west_se(
    X: np.ndarray,
    resid: np.ndarray,
    XtX_inv: np.ndarray,
    k_effective: int,
    n_lags: int | None = None,
) -> np.ndarray:
    """Newey-West HAC SEs on the pooled residual vector.

    Flagged for replacement with Driscoll-Kraay in Tier 3. Petersen (2009,
    RFS 22(1), §1.6) demonstrates that pooled NW with Bartlett weighting
    leaves ~40% of the firm-effect bias intact, versus 0% bias for
    firm-clustered SEs.
    """
    n, _ = X.shape
    if n_lags is None:
        n_lags = int(np.floor(4 * (n / 100) ** (2 / 9)))

    scores = X * resid[:, None]
    S = scores.T @ scores / n

    for j in range(1, n_lags + 1):
        w = 1 - j / (n_lags + 1)
        Gamma_j = scores[j:].T @ scores[:-j] / n
        S = S + w * (Gamma_j + Gamma_j.T)

    V = (n / (n - k_effective)) * XtX_inv @ (n * S) @ XtX_inv
    return np.sqrt(np.diag(V))


# ---------------------------------------------------------------------------
# Panel regression with the full five-method SE matrix
# ---------------------------------------------------------------------------

def robust_panel_regression(
    panel: pd.DataFrame,
    target: str,
    regressors: list[str],
    firm_col: str = "ticker",
    time_col: str = "date",
) -> dict:
    """Panel regression with firm fixed effects and five SE specifications.

    Specification
    -------------
    The within transformation demeans each variable by firm. The resulting
    design matrix drops the (now identically zero) intercept column, and
    k_effective counts only the non-absorbed regressors per the reghdfe /
    fixest / xtreg nested-FE convention. Cameron & Miller (2015, JHR) §IIIB
    discusses this convention.

    Degrees of freedom for p-values follow standard practice:
        HC1              t(n − k_effective)
        firm-clustered   t(G_firm − 1)
        time-clustered   t(G_month − 1)
        two-way          t(min(G_firm, G_month) − 1)
        Newey-West       t(n − k_effective)

    At G_firm ≈ 10 the G − 1 df is optimistic; Imbens & Kolesár (2016) CR2
    with Satterthwaite df is the Tier-3 correction.

    Parameters
    ----------
    panel : pd.DataFrame
        Long panel with at minimum columns: `target`, each `regressor`,
        `firm_col`, `time_col`.
    target : str
        Dependent variable column name.
    regressors : list[str]
        Column names to use as regressors. Order is preserved in output.
    firm_col, time_col : str
        Column names for the firm and time indices.

    Returns
    -------
    dict
        Keys: target, n, n_firms, n_months, r_squared, k_effective,
        coefficients (dict of regressor → SE-method → {se, t, p}).
    """
    df = panel.dropna(subset=regressors + [target]).copy()

    if len(df) < 50:
        return {"error": "Insufficient observations", "n": len(df)}

    # Within transformation: demean each column by firm.
    for col in regressors + [target]:
        df[f"{col}_dm"] = df[col] - df.groupby(firm_col)[col].transform("mean")

    y = df[f"{target}_dm"].values
    X_cols = [f"{r}_dm" for r in regressors]
    X = df[X_cols].values  # No constant column: demeaned ones are identically zero.

    beta, resid, XtX_inv, n, k_effective = _ols_core(X, y)

    # R² on the demeaned (within) scale.
    ss_res = float(np.sum(resid ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r_sq = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan

    # Cluster vectors.
    firms = df[firm_col].values
    time_clusters = (
        pd.to_datetime(df[time_col]).dt.to_period("M").astype(str).values
    )

    # SE estimates.
    se_hc1 = _hc1_se(X, resid, XtX_inv, k_effective)
    se_firm, G_firm = _clustered_se(X, resid, XtX_inv, firms, k_effective)
    se_time, G_month = _clustered_se(X, resid, XtX_inv, time_clusters, k_effective)
    se_twoway, G1, G2 = _twoway_clustered_se(
        X, resid, XtX_inv, firms, time_clusters, k_effective
    )
    se_nw = _newey_west_se(X, resid, XtX_inv, k_effective)

    # Degrees of freedom for each SE method.
    df_hc1 = n - k_effective
    df_firm = max(G_firm - 1, 1)
    df_time = max(G_month - 1, 1)
    df_twoway = max(min(G1, G2) - 1, 1)
    df_nw = n - k_effective

    results = {
        "target": target,
        "n": n,
        "n_firms": int(G_firm),
        "n_months": int(G_month),
        "k_effective": int(k_effective),
        "r_squared": float(r_sq),
        "coefficients": {},
    }

    method_specs = [
        ("HC1", se_hc1, df_hc1),
        ("firm_cluster", se_firm, df_firm),
        ("time_cluster", se_time, df_time),
        ("twoway_cluster", se_twoway, df_twoway),
        ("newey_west", se_nw, df_nw),
    ]

    for i, label in enumerate(regressors):
        b = float(beta[i])
        entry = {"beta": b}
        for method_name, se_arr, df_arr in method_specs:
            se = float(se_arr[i])
            if se > 0:
                t = b / se
                p = float(2 * stats.t.cdf(-abs(t), df=df_arr))
            else:
                t, p = 0.0, 1.0
            entry[method_name] = {
                "se": se, "t": float(t), "p": p, "df": int(df_arr),
            }
        results["coefficients"][label] = entry

    return results


# ---------------------------------------------------------------------------
# Horse race: CII vs standard liquidity benchmarks
# ---------------------------------------------------------------------------

def horse_race_regression(
    panel: pd.DataFrame,
    target: str,
    focal_regressor: str,
    benchmark_regressors: list[str],
    controls: list[str] | None = None,
    firm_col: str = "ticker",
    time_col: str = "date",
) -> dict:
    """Horse race of a focal regressor against standard benchmarks.

    Runs three classes of regressions:

        1. Focal-only: Y = α_i + β·FOCAL + controls
        2. Per-benchmark: Y = α_i + β₁·BENCHMARK_j + controls,
           one regression per benchmark in benchmark_regressors
        3. Combined: Y = α_i + β·FOCAL + Σ β_j·BENCHMARK_j + controls
           (the referee's question — does FOCAL add orthogonal information?)

    Follows the combined specification used by Goyenko, Holden & Trzcinka
    (2009, JFE 92) §5.2 for liquidity-proxy horse races.

    Parameters
    ----------
    panel : pd.DataFrame
        Long panel; see robust_panel_regression for required columns.
    target : str
        Dependent variable column.
    focal_regressor : str
        The regressor under test (typically "CII" in this project).
    benchmark_regressors : list[str]
        Column names of competing estimators (Roll, Corwin-Schultz, Amihud,
        turnover, vol-of-vol, lagged-RV, lagged-illiquidity, VIX).
    controls : list[str] | None
        Additional controls always included (e.g., ["H_price", "H_volume"]).
    firm_col, time_col : str
        Cluster indices for SEs.

    Returns
    -------
    dict
        Keys: focal_only, per_benchmark (list of dicts), combined.
        Each value is the full robust_panel_regression output.
    """
    controls = controls or []

    result = {
        "focal_only": robust_panel_regression(
            panel,
            target=target,
            regressors=[focal_regressor] + controls,
            firm_col=firm_col,
            time_col=time_col,
        ),
        "per_benchmark": [],
        "combined": None,
    }

    for bench in benchmark_regressors:
        per = robust_panel_regression(
            panel,
            target=target,
            regressors=[bench] + controls,
            firm_col=firm_col,
            time_col=time_col,
        )
        per["benchmark_name"] = bench
        result["per_benchmark"].append(per)

    result["combined"] = robust_panel_regression(
        panel,
        target=target,
        regressors=[focal_regressor] + benchmark_regressors + controls,
        firm_col=firm_col,
        time_col=time_col,
    )

    return result


def horse_race_summary_table(
    horse_race_result: dict,
    se_method: str = "twoway_cluster",
) -> pd.DataFrame:
    """Compact summary of a horse race result.

    Returns a DataFrame with rows for each specification (focal-only,
    each per-benchmark, combined) and columns for the focal regressor's
    coefficient, t-statistic, p-value under the chosen SE method, plus
    R².

    Parameters
    ----------
    horse_race_result : dict
        Output of horse_race_regression().
    se_method : str
        One of HC1, firm_cluster, time_cluster, twoway_cluster, newey_west.
    """
    rows = []

    def _row(tag: str, reg_result: dict, focal_name: str) -> dict | None:
        if "error" in reg_result:
            return None
        coef = reg_result["coefficients"].get(focal_name)
        if coef is None:
            return None
        se = coef[se_method]
        return {
            "specification": tag,
            "beta": coef["beta"],
            f"t_{se_method}": se["t"],
            f"p_{se_method}": se["p"],
            "R2": reg_result["r_squared"],
            "n": reg_result["n"],
            "n_firms": reg_result.get("n_firms"),
        }

    # The focal regressor name is inferable from the focal_only spec's
    # first regressor (which is always the focal by construction).
    focal_only = horse_race_result["focal_only"]
    if "error" not in focal_only:
        focal_name = next(iter(focal_only["coefficients"]))
        rows.append(_row(f"{focal_name} alone", focal_only, focal_name))

        for per in horse_race_result["per_benchmark"]:
            if "error" in per:
                continue
            bench = per["benchmark_name"]
            rows.append(_row(f"{bench} alone", per, bench))

        combined = horse_race_result["combined"]
        if "error" not in combined:
            rows.append(_row(f"{focal_name} + all benchmarks", combined, focal_name))

    rows = [r for r in rows if r is not None]
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Build an enriched panel: add baseline finance controls to the prediction panel
# ---------------------------------------------------------------------------

def build_enriched_panel(
    panel: pd.DataFrame,
    tickers_data: dict,
    horizon: int = 21,
) -> pd.DataFrame:
    """Augment the prediction panel with standard finance baseline controls.

    Adds: lagged_rv, lagged_illiq, vix, abn_turnover_t.

    All feature construction uses only information available at or before
    the feature date. Index lookups use `method="pad"` with a 7-day
    tolerance, the standard "as-of" semantics in finance. `method="nearest"`
    is explicitly avoided because it can resolve a Sunday target to the
    *following* Monday, producing silent look-ahead.

    The lagged Amihud illiquidity is computed with dollar volume
    (price × shares traded), matching Amihud (2002, eq. 1). Share-volume
    Amihud is a different measure without a price-impact interpretation.

    The volume feature is named `abn_turnover_t` to reflect its actual
    construction: (current-day volume) / (trailing 60-day mean volume).
    This is an abnormal-turnover spike indicator, not a strictly lagged
    turnover level. Welch-Goyal (2008) and Campbell-Thompson (2008)
    predictive-regression timing: an end-of-day-t feature is a valid
    t-indexed predictor of a target over [t+1, t+h].
    """
    import yfinance as yf

    # Fetch VIX with proxy-safe progress suppression.
    vix_df = yf.download("^VIX", start="2015-01-01", progress=False)
    if isinstance(vix_df.columns, pd.MultiIndex):
        vix_df.columns = vix_df.columns.get_level_values(0)
    vix_series = vix_df["Close"].squeeze()

    tolerance = pd.Timedelta("7D")
    enriched_rows = []

    for _, row in panel.iterrows():
        ticker = row["ticker"]
        date = pd.Timestamp(row["date"])

        if ticker not in tickers_data:
            enriched_rows.append(row.to_dict())
            continue

        df = tickers_data[ticker]["df"]
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        prices = df["Close"].squeeze()
        volume = df["Volume"].squeeze()

        # As-of lookup: "pad" returns the most recent index at or before the
        # target date. A date earlier than the first index returns -1.
        try:
            idx = prices.index.get_indexer(
                [date], method="pad", tolerance=tolerance
            )[0]
        except Exception:
            enriched_rows.append(row.to_dict())
            continue

        if idx < 0 or idx < horizon + 60:
            enriched_rows.append(row.to_dict())
            continue

        # Lagged realized volatility over [t − horizon, t − 1].
        past_returns = np.log(
            prices.iloc[idx - horizon:idx].values
            / prices.iloc[idx - horizon - 1:idx - 1].values
        )
        lagged_rv = float(np.sqrt(np.sum(past_returns ** 2)))

        # Lagged Amihud illiquidity with dollar volume.
        past_prices = prices.iloc[idx - horizon:idx].values.astype(float)
        past_vol_shares = volume.iloc[idx - horizon:idx].values.astype(float)
        past_dollar_vol = past_prices * past_vol_shares
        past_dollar_vol = np.where(past_dollar_vol > 0, past_dollar_vol, np.nan)
        past_abs_ret = np.abs(past_returns).astype(float)
        # Amihud (2002) 10⁶ scaling convention.
        lagged_illiq = float(np.nanmean(past_abs_ret / past_dollar_vol) * 1e6)

        # Abnormal-turnover spike at t: volume_t / trailing-60-day mean.
        vol_60 = volume.iloc[max(0, idx - 60):idx].mean()
        abn_turnover_t = (
            float(volume.iloc[idx] / vol_60) if vol_60 > 0 else np.nan
        )

        # VIX as-of at or before `date`.
        try:
            vix_idx = vix_series.index.get_indexer(
                [date], method="pad", tolerance=tolerance
            )[0]
            vix_val = float(vix_series.iloc[vix_idx]) if vix_idx >= 0 else np.nan
        except Exception:
            vix_val = np.nan

        row_dict = row.to_dict()
        row_dict["lagged_rv"] = lagged_rv
        row_dict["lagged_illiq"] = lagged_illiq
        row_dict["abn_turnover_t"] = abn_turnover_t
        row_dict["vix"] = vix_val
        enriched_rows.append(row_dict)

    return pd.DataFrame(enriched_rows)


# ---------------------------------------------------------------------------
# CII sensitivity sweep
# ---------------------------------------------------------------------------

def cii_sensitivity_sweep(
    tickers_data: dict,
    rolling_results: dict,
    L_values: list[int] | None = None,
    horizon: int = 21,
) -> pd.DataFrame:
    """Sweep CII trailing window L and report predictive results.

    Addresses the referee concern about L = 30 sensitivity.
    """
    from fractal_pv.predict import build_prediction_panel

    L_values = L_values or [15, 20, 30, 40, 60]
    results = []

    for L in L_values:
        panel = build_prediction_panel(
            tickers_data, rolling_results,
            horizon=horizon, correlation_window=L,
        )
        if panel.empty:
            continue

        for target in ["realized_vol", "amihud_illiq"]:
            if target not in panel.columns:
                continue
            res = robust_panel_regression(
                panel, target, ["CII", "H_price", "H_volume"],
            )
            if "error" in res:
                continue
            cii = res["coefficients"].get("CII", {})
            results.append({
                "L": L, "target": target,
                "beta": cii.get("beta", np.nan),
                "t_HC1": cii.get("HC1", {}).get("t", np.nan),
                "t_firm": cii.get("firm_cluster", {}).get("t", np.nan),
                "t_twoway": cii.get("twoway_cluster", {}).get("t", np.nan),
                "p_twoway": cii.get("twoway_cluster", {}).get("p", np.nan),
                "R2": res.get("r_squared", np.nan),
                "n": res.get("n", 0),
            })

    return pd.DataFrame(results)
