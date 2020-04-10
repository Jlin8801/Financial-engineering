#Binomial option pricing model
import math

#basic factors input
spot_p = int(input("Enter the asset spot price -> "))
u = float(input("upward momentum -> "))
d = float(input("downward momentum -> "))
Strike_X = float(input("Option strike price -> "))
interest_r = float(input("assumed continous compounding interest rate -> "))/100
n = int(input("option period -> "))

#transform compounding factor and pseudo probability
R = math.e**interest_r
p = (R-d)/(u-d)

#calculate callvalue = max(0, S - X)
def call_option(price, X):
	callvalue = list()
	for i in range(n+1):
		if (price[n][i] > X):
			v = price[n][i] - X
			callvalue.append(v)
		else:
			callvalue.append(0)
	return(callvalue)

#calculate putvalue = max(0, X - S)
def put_option(price, X):
	putvalue = list()
	for i in range(n+1):
		if (price[n][i] < X):
			v = X - price[n][i]
			putvalue.append(v)
		else:
			putvalue.append(0)
	return(putvalue)

#conduct backward induction
def BOPM(BIvalue, prob, discount_factor):
	for i in range(n):
		BIvalue.append(list())
		for j in range(n-i):
			v = (prob*BIvalue[i][j]+(1-prob)*BIvalue[i][j+1])/R
			BIvalue[i+1].append(v)

	return BIvalue

#European option
#compute the asset price at each situation
S_price = list()
S_price.append([spot_p])

for i in range(n):#0,1,2
	S_price.append(list())
	for j in range(i+2):#2,3,4
		if (j == 0):
			up = S_price[i][j]*u
			S_price[i+1].append(up)
		else:
			down = S_price[i][j-1]*d
			S_price[i+1].append(down)

#determine call or put?

opt = str(input("call or put?"))
option_v = list()

if (opt == "call"):
	value = call_option(S_price, Strike_X)
elif (opt == "put"):
	value = put_option(S_price, Strike_X)

#compute the option's value at each situation
option_v.append(value)
option_v = BOPM(option_v, p, R)

#layout results by for loops
for i in range(len(option_v)):
	for j in range(len(option_v[i])):
		print("%.3f" % option_v[i][j], end = " ")
	print()

