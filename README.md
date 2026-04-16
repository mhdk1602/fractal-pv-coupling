# Temporal Fractal Coupling Between Price Volatility and Trading Volume

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19611544.svg)](https://doi.org/10.5281/zenodo.19611544)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fractal-pv.streamlit.app)

**Paper**: *Static and Temporal Fractal Coupling Between Volatility and Trading Volume: Evidence from S&P 500 Stocks, 2015–2026*

**Author**: [Dinesh Hari](https://orcid.org/0009-0003-1036-9477) — University of the Cumberlands

## Key Finding

The fractal scaling properties of price volatility and trading volume are temporally coupled in 49 of 50 S&P 500 equities studied (mean *r* = 0.665). The Coupling Intensity Index (CII), introduced here, predicts future Amihud illiquidity at the one-month horizon (two-way clustered *t* = 2.90, *p* = 0.004) under five standard-error specifications. CII does not predict realised volatility once cross-sectional and temporal dependence are properly accounted for (*t* = 0.84, *p* = 0.40).

When price-volume fractal coupling tightens, liquidity conditions deteriorate.

## Methods

- **Hurst estimation**: Detrended Fluctuation Analysis (DFA), with R/S and MFDFA(*q*=2) as cross-checks
- **Rolling analysis**: Aligned rolling Hurst exponents for |returns| and log-volume (*W* = 500, Δ = 20)
- **CII**: Time-varying trailing Pearson correlation of rolling Hurst exponents
- **Inference**: Panel regressions with firm fixed effects and five SE methods (HC1, firm-clustered, time-clustered, two-way clustered, Newey-West)
- **Robustness**: 11 checks including shuffled surrogates, non-overlapping windows, first-differenced series, subperiod analysis, and market-factor controls
- **Data**: Daily OHLCV from Yahoo Finance for 50 S&P 500 constituents (2015–2026)

## Setup

```bash
pip install -e ".[dev,test]"
python -c "from fractal_pv.data import fetch_universe, SP500_SAMPLE; fetch_universe(SP500_SAMPLE)"
```

## Interactive Dashboard

The [Streamlit app](https://fractal-pv.streamlit.app) provides interactive exploration of fractal dynamics for any ticker. No installation required.

## Project Structure

```
app.py                          # Streamlit dashboard
src/fractal_pv/
  data.py                       # Data fetching + parquet caching
  hurst.py                      # Hurst estimation (DFA, R/S, MFDFA)
  stationarity.py               # ADF, KPSS, preprocessing
  bootstrap.py                  # Block bootstrap CIs for Hurst exponents
  rolling.py                    # Rolling window dual-Hurst analysis
  predict.py                    # CII computation + predictive regressions
  inference_robust.py           # Clustered SEs, Newey-West, sensitivity sweeps
  regimes.py                    # VIX regime conditioning
  validate.py                   # Theory-backed validation harness
  inference.py                  # Inference engine
research/
  paper/main.tex                # Submission-ready manuscript
  paper/figures/                # 9 publication figures (PDF + PNG)
  lineage/                      # Original MSc report (Hari, 2013, KCL)
legacy/                         # Original MATLAB code (2014)
```

## Research Lineage

This project builds on an [MSc project](research/lineage/hari_2013_msc_fractal_modelling_kcl.pdf) at King's College London (2013) that examined static cross-sectional association between fractal characteristics and average trading volume. The present work shifts from static association to temporal co-evolution, introducing a dynamic coupling measure and testing its predictive content for future market illiquidity.

## Citation

```bibtex
@misc{hari2026fractal,
  author={Hari, Dinesh},
  title={Static and Temporal Fractal Coupling Between Volatility and
         Trading Volume: Evidence from {S\&P}~500 Stocks, 2015--2026},
  year={2026},
  doi={10.5281/zenodo.19611544},
  url={https://doi.org/10.5281/zenodo.19611544}
}
```

## License

MIT
