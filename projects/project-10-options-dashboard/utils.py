import math
from math import erf, sqrt, exp, log

def norm_cdf(x):
    return 0.5 * (1.0 + erf(x / math.sqrt(2.0)))

def norm_pdf(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)

def black_scholes_price(S, K, T, sigma, r, kind="call"):
    if T <= 0 or sigma <= 0:
        if kind == "call":
            return max(S - K, 0.0)
        return max(K - S, 0.0)
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if kind == "call":
        return S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
    else:
        return K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)

def greeks(S, K, T, sigma, r, kind="call"):
    if T <= 0 or sigma <= 0:
        delta = 1.0 if (S > K and kind == "call") else ( -1.0 if (S < K and kind == "put") else 0.0)
        return {"delta": delta, "gamma": 0.0, "theta": 0.0, "vega": 0.0}
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    pdf = norm_pdf(d1)
    gamma = pdf / (S * sigma * math.sqrt(T))
    if kind == "call":
        delta = norm_cdf(d1)
        theta = - (S * pdf * sigma) / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * norm_cdf(d2)
    else:
        delta = norm_cdf(d1) - 1
        theta = - (S * pdf * sigma) / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * norm_cdf(-d2)
    vega = S * pdf * math.sqrt(T)
    return {"delta": delta, "gamma": gamma, "theta": theta, "vega": vega}

def payoff_single_option_grid(S_range, K, premium, qty, kind="call"):
    import numpy as np
    ST = S_range
    if kind == "call":
        payoff = np.maximum(ST - K, 0.0) - premium
    else:
        payoff = np.maximum(K - ST, 0.0) - premium
    return payoff * qty

def combine_payoffs(payoffs):
    import numpy as np
    total = None
    for p in payoffs:
        if total is None:
            total = p
        else:
            total = total + p
    return total
