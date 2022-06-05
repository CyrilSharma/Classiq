import scipy.integrate as integrate
import math
import numpy as np
from scipy.optimize import minimize

def f(x, mu = 0, sigma = 0.1):
    return 1/(x*sigma*math.sqrt(2*math.pi))*math.exp(-1*(math.log(x)-mu)**2/(2*(sigma)**2)) #log normal

def p(x, a, x1, x2, x3, b):
    if x < a:
        return 0
    elif x < x1:
        return (f(x1)-f(a))/2
    elif x < x2:
        return (f(x2)-f(x1))/2
    elif x < x3:
        return (f(x3)-f(x2))/2
    elif x < b:
        return (f(b)-f(x3))/2
    else:
        return 0

def l2norm(x, a, x1, x2, x3, b):
    return math.sqrt((p(x, a, x1, x2, x3, b) - f(x))**2)

def inequality_constraint(dists):
    return 1.1 - sum(dists)

def error(dists):
    return integrate.quad(lambda x: l2norm(x, 0.5 + dists[0], 0.5 + dists[0] + dists[1], 0.5 + dists[0] + dists[1] + dists[2], 0.5 + dists[0] + dists[1] + dists[2] + dists[3],  0.5 + dists[0] + dists[1] + dists[2] + dists[3] + dists[4]), 0.5, 1.6)[0] #a, x1, x2, x3, b (using index 0 cause thats the actual value, 1 is the error)

b = (0.1, 0.4)
bnds = (b, b, b, b, b)

cons = ({'type': 'ineq', 'fun': inequality_constraint})
initial = [0.2, 0.2, 0.2, 0.2, 0.2]

output = minimize(error, initial, options={"disp": True}, bounds = bnds, constraints=cons)
print(output.fun)
print(output.x)