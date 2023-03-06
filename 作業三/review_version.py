import numpy as np

def call_payout(curr_price, strike):
    return max(0, curr_price - strike)

def put_payout(curr_price, strike):
    return max(0, strike - curr_price)

def compute_price_array(s, u, d, n):
    arr = [[None]*2**i for i in range(n)]
    for i in range(len(arr)):
        if i==0: arr[i][0] = s
        elif i > 0:
            for j in range(len(arr[i])):
                arr[i][j] = arr[i-1][j//2]*u if np.mod(j,2)==0 else arr[i-1][j//2]*d
    return arr

def binomial_pricing_model(prob, interest, price, strike, option_kind):
    if option_kind=="C":
        intrinsic_value = [call_payout(p, strike) for p in price]
    elif option_kind=="P":
        intrinsic_value = [put_payout(p, strike) for p in price]
    
    induction = intrinsic_value.copy()
    while len(induction) > 1:
        temp = [None] * (len(induction)//2)
        for i in range(len(temp)):
            temp[i] = (prob * induction[2*i] + (1 - prob) * induction[2*i+1]) * np.exp(-1*interest)
        induction = temp.copy()
        del temp

    return induction[0]

def main():
    print(" - binomial option pricing model - ")
    spot_price = 160
    strike = 150
    interest = 18.232 * 10**(-2)
    period = 4  # 這裡實務上應該是用天數或是交易小時數 做切割 interval
    upward, downward = 1.5, 0.5  # 這裡 up / down 應該是用volatility去做最小單位的漲跌幅
    
    pseudo_prob = (np.exp(interest) - downward) / (upward - downward)
    print("p: %.4f" % pseudo_prob)

    spot_price_array = compute_price_array(spot_price, upward, downward, period)
    for sub_arr in spot_price_array:
        for x in sub_arr:
            print(f"{x:.2f}", end=" ")
        print()

    c_bopm_price = binomial_pricing_model(prob=pseudo_prob,
                                        interest=interest,
                                        price=spot_price_array[-1],
                                        strike=strike,
                                        option_kind="C")
    
    p_bopm_price = binomial_pricing_model(prob=pseudo_prob,
                                        interest=interest,
                                        price=spot_price_array[-1],
                                        strike=strike,
                                        option_kind="P")
    
    print("Call Option: %.4f" % c_bopm_price)
    print("Put  Option: %.4f" % p_bopm_price)

if __name__ ==  "__main__":
    main(0)
