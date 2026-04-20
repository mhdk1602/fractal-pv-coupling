# Temporal Fractal Coupling Between Price Volatility and Trading Volume

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19611544.svg)](https://doi.org/10.5281/zenodo.19611544)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fractal-pv.streamlit.app)

**Paper**: *Static and Temporal Fractal Coupling Between Volatility and Trading Volume: Evidence from S&P 500 Stocks, 2015–2026*

**Author**: [Dinesh Hari](https://orcid.org/0009-0003-1036-9477)

## Data Provenance

All data are daily OHLCV prices from Yahoo Finance via the `yfinance` Python package. No proprietary, restricted, or purchased data are used. The 50-ticker sample (Appendix A of the paper) covers all 11 GICS sectors from the S&P 500 index, with continuous listing from January 2015 through April 2026. VIX data are sourced from the CBOE via Yahoo Finance. Data are downloaded on first run and cached as parquet files under `data/raw/`.

## Replication

### Requirements

- Python 3.10+
- Dependencies listed in `pyproject.toml`

### Quick Start

```bash
git clone https://github.com/mhdk1602/fractal-pv-coupling.git
cd fractal-pv-coupling
pip install -e .
python replicate.py
```

### Execution Order

`replicate.py` is the master script. It runs all steps in sequence:

1. **Data fetch** — downloads and caches OHLCV for 50 tickers (~2 min)
2. **Hurst estimation** — full-sample DFA for returns, |returns|, volume
3. **Rolling analysis** — dual rolling Hurst with W=500, step=20 (~10 min)
4. **Regime conditioning** — VIX classification, crisis windows
5. **Predictive regressions** — panel with 5 SE methods
6. **Figure generation** — pre-generated PDFs in `research/paper/figures/`
7. **Summary** — prints all headline numbers to stdout

### Expected Outputs

| Output | Location |
|--------|----------|
| Hurst estimates (50 tickers) | `research/paper/tables/table1_hurst_estimates.csv` |
| Robustness summary | `research/paper/tables/table2_robustness_summary.csv` |
| Sector summary | `research/paper/tables/table3_sector_summary.csv` |
| 9 publication figures | `research/paper/figures/fig1_*.pdf` through `fig9_*.pdf` |
| LaTeX manuscript | `research/paper/main.tex` → compile with `tectonic main.tex` |
| Compiled PDF | `research/paper/main.pdf` |

### Package Structure

```
replicate.py                    # Master replication script
src/fractal_pv/
  data.py                       # Yahoo Finance download + parquet caching
  hurst.py                      # DFA, R/S, MFDFA Hurst estimation
  stationarity.py               # ADF/KPSS tests, series transforms
  bootstrap.py                  # Block bootstrap CIs (Politis & Romano 1994)
  rolling.py                    # Rolling dual-Hurst, temporal correlation
  predict.py                    # CII, forward metrics, panel regressions
  inference_robust.py           # 5 SE methods, sensitivity sweeps
  regimes.py                    # VIX regime conditioning, crisis windows
  validate.py                   # Theory-backed validation checks
  inference.py                  # Finding extraction
research/
  paper/main.tex                # Manuscript source
  paper/references.bib          # 46 BibTeX entries
  paper/figures/                # 9 publication figures (PDF + PNG)
  paper/tables/                 # 3 CSV data tables
  lineage/                      # Original MSc report (Hari, 2013, KCL)
  robustness/RESULTS.md         # 11 robustness check results
app.py                          # Streamlit dashboard
legacy/                         # Original MATLAB code (2014)
```

## Interactive Dashboard

The [Streamlit dashboard](https://fractal-pv.streamlit.app) provides interactive exploration of per-ticker fractal dynamics. Source code for the enhanced dashboard is at [fractal-pv-dashboard](https://github.com/mhdk1602/fractal-pv-dashboard).

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
