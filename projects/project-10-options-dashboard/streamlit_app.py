import json
from pathlib import Path
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from utils import black_scholes_price, greeks, payoff_single_option_grid, combine_payoffs

ROOT = Path(__file__).parent.parent
QUOTE_PATH = ROOT / 'project-8-options-ops' / 'quotes_state.json'

st.title('Options Payoff & Greeks Explorer')

def load_quote_price():
    if QUOTE_PATH.exists():
        try:
            with open(QUOTE_PATH, 'r') as f:
                data = json.load(f)
            # try common keys
            def find_number(d):
                if isinstance(d, dict):
                    for v in d.values():
                        r = find_number(v)
                        if r is not None:
                            return r
                elif isinstance(d, (int, float)):
                    return float(d)
                return None
            v = find_number(data)
            if v:
                return float(v)
        except Exception:
            pass
    return None

live_price = load_quote_price()

st.sidebar.header('Market / Option Inputs')
underlying = st.sidebar.number_input('Underlying price', value=float(live_price) if live_price else 100.0)
days = st.sidebar.slider('Days to expiry', 1, 365, 30)
vol = st.sidebar.slider('Implied vol (sigma)', 1.0, 200.0, 20.0) / 100.0
rate = st.sidebar.number_input('Risk-free rate (annual)', value=0.01)

st.sidebar.header('Legs')
leg_type = st.sidebar.selectbox('Preset', ['Single Call','Vertical (Call)','Straddle','Iron Condor'])

S_min = max(1, underlying * 0.5)
S_max = underlying * 1.5
S = np.linspace(S_min, S_max, 201)
T = days / 365.0

payoffs = []
greek_list = []

if leg_type == 'Single Call':
    K = st.sidebar.number_input('Strike', value=round(underlying))
    premium = st.sidebar.number_input('Premium (paid)', value=1.0)
    qty = st.sidebar.number_input('Quantity', value=1)
    kind = st.sidebar.selectbox('Kind', ['call','put'])
    pay = payoff_single_option_grid(S, K, premium, qty, kind=kind)
    payoffs.append(pay)
    g = greeks(underlying, K, T, vol, rate, kind=kind)
    greek_list.append(('leg1', g))

elif leg_type == 'Vertical (Call)':
    K1 = st.sidebar.number_input('Long strike', value=round(underlying))
    K2 = st.sidebar.number_input('Short strike', value=round(underlying+5))
    p1 = st.sidebar.number_input('Long premium', value=2.0)
    p2 = st.sidebar.number_input('Short premium', value=0.5)
    q = st.sidebar.number_input('Quantity', value=1)
    pay_long = payoff_single_option_grid(S, K1, p1, q, kind='call')
    pay_short = payoff_single_option_grid(S, K2, p2, -q, kind='call')
    payoffs.extend([pay_long, pay_short])
    greek_list.append(('long', greeks(underlying, K1, T, vol, rate, 'call')))
    greek_list.append(('short', greeks(underlying, K2, T, vol, rate, 'call')))

elif leg_type == 'Straddle':
    K = st.sidebar.number_input('Strike', value=round(underlying))
    p_call = st.sidebar.number_input('Call premium', value=2.0)
    p_put = st.sidebar.number_input('Put premium', value=2.0)
    q = st.sidebar.number_input('Quantity', value=1)
    pay_call = payoff_single_option_grid(S, K, p_call, q, kind='call')
    pay_put = payoff_single_option_grid(S, K, p_put, q, kind='put')
    payoffs.extend([pay_call, pay_put])
    greek_list.append(('call', greeks(underlying, K, T, vol, rate, 'call')))
    greek_list.append(('put', greeks(underlying, K, T, vol, rate, 'put')))

elif leg_type == 'Iron Condor':
    k1 = st.sidebar.number_input('Short put strike', value=round(underlying-10))
    k2 = st.sidebar.number_input('Long put strike', value=round(underlying-15))
    k3 = st.sidebar.number_input('Short call strike', value=round(underlying+10))
    k4 = st.sidebar.number_input('Long call strike', value=round(underlying+15))
    p1 = st.sidebar.number_input('Short put premium', value=1.0)
    p2 = st.sidebar.number_input('Long put premium', value=0.2)
    p3 = st.sidebar.number_input('Short call premium', value=1.0)
    p4 = st.sidebar.number_input('Long call premium', value=0.2)
    q = st.sidebar.number_input('Quantity', value=1)
    pay_short_put = payoff_single_option_grid(S, k1, p1, q, kind='put')
    pay_long_put = payoff_single_option_grid(S, k2, p2, -q, kind='put')
    pay_short_call = payoff_single_option_grid(S, k3, p3, q, kind='call')
    pay_long_call = payoff_single_option_grid(S, k4, p4, -q, kind='call')
    payoffs.extend([pay_short_put, pay_long_put, pay_short_call, pay_long_call])
    greek_list.append(('sp', greeks(underlying, k1, T, vol, rate, 'put')))
    greek_list.append(('lp', greeks(underlying, k2, T, vol, rate, 'put')))
    greek_list.append(('sc', greeks(underlying, k3, T, vol, rate, 'call')))
    greek_list.append(('lc', greeks(underlying, k4, T, vol, rate, 'call')))

total = combine_payoffs(payoffs)

fig, ax = plt.subplots(figsize=(8,4))
ax.plot(S, total, label='Net payoff (incl. prem)')
ax.axhline(0, color='k', linewidth=0.6)
ax.set_xlabel('Underlying Price at Expiry')
ax.set_ylabel('Profit / Loss')
ax.legend()
st.pyplot(fig)

st.header('Greeks (per-leg)')
for name, g in greek_list:
    st.write(name, {k: round(v,6) for k,v in g.items()})

st.markdown('---')
st.write('Tips: use sliders and presets to demonstrate payoff shapes and how Greeks change with underlying and vol.')
