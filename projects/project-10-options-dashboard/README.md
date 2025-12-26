# Project 10 — Options Payoff Dashboard (Streamlit)

Interactive Streamlit app to visualize single-option and multi-leg payoff diagrams and compute Black–Scholes Greeks.

Features

- Single-option payoff (call/put)
- Multi-leg presets: vertical, straddle, iron condor
- Sliders for underlying, days-to-expiry, vol, rate, strikes, premiums
- Optional live quote seed from `projects/project-8-options-ops/quotes_state.json`
- Greeks (delta, gamma, theta, vega) using Black–Scholes

Run

```powershell
cd projects/project-10-options-dashboard
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

Notes

- The app attempts to read a numeric value from `projects/project-8-options-ops/quotes_state.json` to seed the underlying price.
- This is a local demo for interview/demo purposes, not production-grade.
