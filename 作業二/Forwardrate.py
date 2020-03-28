#input multiple bonds' factors

#bonds' cashflow function
def CashFlow(coup_r, n_period):
	CF = list()
	for i in range(n_period):
		if i != (n_period-1):
			CF.append(coup_r*100)
		else:
			CF.append(coup_r*100+100)
	return(CF)

#bonds forward rate calculation function
def Forward(i, j, Spot_rate):
	starting_t = Spot_rate[i]
	ending_t = Spot_rate[j]
	Fi_j = (((1+ending_t)**(j+1))/((1+starting_t)**(i+1)))**(1/(j-i))-1
	return(Fi_j)

#basic number of bonds
N = int(input("how many bonds info we have?"))

bondSet = list()

for i in range(N):
	bondSet.append([0,0,0])
	bondSet[i][0] = int(input())        #bond's period
	bondSet[i][1] = float(input())/100  #bond's coupon rate
	bondSet[i][2] = float(input())      #bond's market price

bondSet.sort() #sort the bonds in the order of period
#print(bondSet)

#calculate YTM for bonds
#set up an original Spot rate list as later discounting factors
Spot_rate = list()
for i in range(N):
	Spot_rate.append(0)
#calculate Spot rate from bonds' cashflow
for i in range(N):
	n_period = bondSet[i][0]
	coup_r = bondSet[i][1]
	mkt_p = bondSet[i][2]
	cashflow = CashFlow(coup_r, n_period)
	#print(cashflow)
	PV = 0.0
	for j in range(i+1):
		if j != i:
			PV += cashflow[j]/(1+Spot_rate[j])**(j+1)
		else:#calculate the last period's discount rate, which is the spot rate i
			Spot_rate[j] = float((cashflow[j]/(mkt_p-PV))**(1/(j+1)) - 1)

Spot_rate.insert(0,0)#adjust the list for layout purpose

#layout the spot rate of each period
Forward_r = list()
for i in range(N):
	Forward_r.append(list())
	Forward_r[i].append("N/A")
	for j in range(N):
		if i < j:
			Forward_r[i].append(Forward(i, j, Spot_rate))
		elif i == j:
			Forward_r[i].append(1)
		else:
			Forward_r[i].append("N/A")

Forward_r.insert(0,0)#adjust the list for layout purpose

#Headers line
for i in range(N+1):
  if i == 0:
    print(8*" ",end = "")
  print("%8d" % i,end ="")
#change line
print("")
#layout forward rate information
for i in range(N+1):
  print("%8d" % i, end = "")#row name
  for j in range(N+1):
  	if i == 0:
  		print("%7.2f%%" % (Spot_rate[j]*100), end = "")
  	else:
  		if type(Forward_r[i][j]) != str:
  			print("%7.2f%%" % (Forward_r[i][j]*100), end = "")
  		else:
  			print("%8s" % Forward_r[i][j], end = "")
  print("")
