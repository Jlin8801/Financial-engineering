import QuantLib as ql
import matplotlib.pyplot as plt
import numpy as np
import math

#basic variables setup
S0 = float(input("Current price of the underlying assets: "))
#S0 = 100
K = float(input("Option strike price: "))
#K = 105
sigma = float(input("Volatility of the asset price: "))
#sigma = 0.1
a = float(input("Changing speed of interest rate: "))
#a = 0.1
length = float(input("Option life in years: "))
#length = 1 # in years
dt = 1/365
timestep = int(length/dt)

forward_rate = float(input("forward rate: "))
#forward_rate = 0.05
day_count = ql.Thirty360()
todays_date = ql.Date(11, 5, 2020)


#obtain forward and spot rate
ql.Settings.instance().evaluationDate = todays_date

spot_curve = ql.FlatForward(todays_date, ql.QuoteHandle(ql.SimpleQuote(forward_rate)), day_count)
spot_curve_handle = ql.YieldTermStructureHandle(spot_curve)

#simulation of hull white model using QuantLib
hw_process = ql.HullWhiteProcess(spot_curve_handle, a, sigma)
rng = ql.GaussianRandomSequenceGenerator(ql.UniformRandomSequenceGenerator(timestep, ql.UniformRandomGenerator()))
seq = ql.GaussianPathGenerator(hw_process, length, timestep, rng, False)

#define interest rate path generation function
def generate_paths(num_paths, timestep):
    arr = np.zeros((num_paths, timestep+1))
    for i in range(num_paths):
        sample_path = seq.next()
        path = sample_path.value()
        time = [path.time(j) for j in range(len(path))]
        value = [path[j] for j in range(len(path))]
        arr[i, :] = np.array(value)
    return np.array(time), arr

#generate Brownian path(under term structure mu has to become a list)
def genBrownPath (T, mu, sigma, S0, dt):
    
    n = round(T/dt)
    t = np.linspace(0, T, n)
    W = [0] + np.random.standard_normal(size = n)
    W = np.cumsum(W)*np.sqrt(dt) # == standard brownian motion
    X = (mu-0.5*sigma**2)*t + sigma*W
    S = S0*np.exp(X) # == geometric brownian motion
    plt.plot(t, S)
    return S

#apply Monte Carlo process
num_paths = 1000
time, rate_paths = generate_paths(num_paths, timestep)
#delete the last short rate at timestep n, due to data form calculation
time = np.delete(time,-1)
rate_paths = np.delete(rate_paths,-1,axis = 1)


#adjust the data form to put short rate into GBM
Asset_p_paths = []
for i in range(0,num_paths):
    np.random.seed(i)
    Asset_p_paths.append(genBrownPath(length, rate_paths[i], sigma, S0, dt))

plt.title("Geometric Brownian Motion Asset price")
plt.show()

#display the term structure form monte carlo simulation
for i in range(num_paths):
    plt.plot(time, rate_paths[i, :], lw=0.8, alpha=0.6)
plt.title("Hull-White Short Rate Simulation")
plt.show()

#calculate the option payoffs from different paths
#call option with strike price == K, max(p-k, 0)
Call_Payoff = []
for i in range(num_paths):
    if (Asset_p_paths[i][-1] - K) >= 0:
        Call_Payoff.append(Asset_p_paths[i][-1]-K)
    else:
        Call_Payoff.append(0)
#print(Call_Payoff)

#call option with strike price == K, max(k-p, 0)
Put_Payoff = []
for i in range(num_paths):
    if (K - Asset_p_paths[i][-1]) >= 0:
        Put_Payoff.append(K-Asset_p_paths[i][-1])
    else:
        Put_Payoff.append(0)
#print(Put_Payoff)

#calculate discount factors by multiplying short rates along with each scenario
Discount = []

tmp_r = rate_paths*dt+1
for i in range(num_paths):
    Term_structure = tmp_r[i]
    P = 1
    for j in range(len(Term_structure)):
        P = P*Term_structure[j]
    Discount.append(P)

#discounted the option payoff to t0
Call_value = []
Put_value = []
for i in range(num_paths):
    Call_value.append(Call_Payoff[i]/Discount[i])
    Put_value.append(Put_Payoff[i]/Discount[i])

Call = math.fsum(Call_value)/num_paths
Put = math.fsum(Put_value)/num_paths
print("Call = %.4f" % Call)
print("Put = %.4f" % Put)



