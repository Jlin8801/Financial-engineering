import numpy as np
from scipy.stats import norm

def compute_div_pv(interest, dividends):
    div_pv = 0.
    for div in dividends:
        div_pv += div[0] * np.exp(-1*interest*div[1]/12)
    return div_pv

def black_scholes(S, K, r, sigma, tao):
    d1 = (np.log(S / K) + (r + sigma**2 / 2) * tao) / (sigma * np.sqrt(tao))
    d2 = d1 - sigma * np.sqrt(tao)
    call = S * norm.cdf(d1) - K * np.exp(-1*r*tao) * norm.cdf(d2)
    put = K * np.exp(-1*r*tao) * norm.cdf(-1*d2) - S * norm.cdf(-1*d1)
    return call, put

def main():
    spot_price = 75
    strike = 65
    interest = 6 * 10**(-2)
    tao = 6 / 12
    sigma = 0.35

    dividends = [[1,1], [1,6]]  # (cash div, paied in months)

    div_pv = compute_div_pv(interest, dividends)

    net_spot = spot_price - div_pv
    c, p = black_scholes(S=net_spot,
                         K=strike,
                         r=interest,
                         sigma=sigma,
                         tao=tao)

    print(" - Black-Scholes Option pricing Model - ")
    print("call - %.4f" % c)
    print("put  - %.4f" % p)

    
"""
 - Black-Scholes Option pricing Model - 
call - 12.8136
put  - 2.8580
"""

if __name__ == "__main__":
    main()
