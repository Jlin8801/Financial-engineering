#Black-Scholes option pricing model
import math
from scipy.stats import norm

#data info input
Spot_price = float(input("Market price of the underlying: "))
Strike_price = float(input("Strike price till maturity: "))
R = float(input("Risk free interest rate: "))/100
tao = float(input("Time span of the contract(in month): "))/12
sigma = float(input("Return volatility: "))

#riskless dividends input
Dividends = list()
D_num = int(input("Number of annouced dividends: "))

for i in range(D_num):
	dividends_payment = float(input("%dth dividends: " % (i+1)))
	dividends_pay_date = float(input("after how many months: "))/12
	D_info = [dividends_payment,dividends_pay_date]
	Dividends.append(D_info)

#present value of dividends that are riskless
D_pv = 0
for i in range(D_num):
	D_pv += Dividends[i][0]*math.e**(-R*Dividends[i][1])

#get the part of Spot price that are risky
Spot_price -= D_pv

#derive the calculation component under Black-Scholes assumptions
d1_nomi = math.log(Spot_price/Strike_price)+(R+(0.5)*sigma**2)*tao
d1_deno = sigma*(tao**(0.5))
d1 = d1_nomi/d1_deno
d2 = d1 - d1_deno

put_price = -Spot_price*norm.cdf(-d1) + Strike_price*math.e**(-R*tao)*norm.cdf(-d2)
call_price = Spot_price*norm.cdf(d1) - Strike_price*math.e**(-R*tao)*norm.cdf(d2)

print("Put price = %.2f" % put_price)
print("Call price = %.2f" % call_price)







