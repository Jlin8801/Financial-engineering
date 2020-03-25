import math

m = 12 #annual compound basis

principle = int(input())*10000
period = int(input())*m
interest_rate = float(input())/100/m

month_P_payment = math.ceil(principle/period)
TTA = 0
Cinterest = 0

#Basic information
print("本金          %15d元" % principle)
print("期數          %15d年" % (period//m))
print("年利率        %15d％" % (interest_rate*100*m))
print("平均每月攤還本金%15d元" % month_P_payment)
print("")

#showcase the columes' names
print("%10s%10s%10s%10s" % ("期數","支付本金","支付利息","累積支付"))

for i in range(period):
	if i < period-1:
		interest = round(principle * interest_rate)
		principle -= month_P_payment

	else:
		month_P_payment = principle
		interest = round(principle * interest_rate)
		#due to the ceiling effect, the left amount will be all we need to pay for the principle, which will be less than previous months.		
	
	TTA = TTA + month_P_payment + interest
	print("%11d%13d%13d%12d" % (i+1, month_P_payment, interest, TTA))
	Cinterest += interest

print("")
print("全部利息  %d元" % Cinterest)

#THE END