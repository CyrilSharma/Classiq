import scipy.integrate as integrate
import math
import numpy as np
from scipy.optimize import minimize
import time

qubits = 3

space = 1/(2**qubits+1) #set up initial conditions
initial = []
for i in range (0, 2**qubits+1):
    initial.append(space)

data = [0.5 + sum(initial[:i]) for i in range (1, 2**qubits + 2)]
print(data)



def f(x, mu = 0, sigma = 0.1):
    return 1/(x*sigma*math.sqrt(2*math.pi))*math.exp(-1*(math.log(x)-mu)**2/(2*(sigma)**2)) #log normal

def p(x, rectPos): #should be 2**qubits + 1 things in rectPos
    if x < rectPos[0]:
        return 0
    elif x > rectPos[-1]:
        return 0
    else:
        for i in range(1, len(rectPos)):
            if x < rectPos[i]:
                return (f(rectPos[i]) + f(rectPos[i-1]))/2
        return 0

print(f(1))
print(p(1, data))

def l2norm(x, rectPos):
    # print(x)
    # print(rectPos)
    # print(p(x, rectPos))
    return math.sqrt((p(x, rectPos) - f(x))**2)

def inequality_constraint(dists):
    return 1.1 - sum(dists)

def error(dists):

    data = [0.5 + sum(dists[:i]) for i in range (1, 2**qubits + 2)]

    return integrate.quad(lambda x: l2norm(x, data), 0.5, 1.6)[0] #a, x1, x2, x3, b (using index 0 cause thats the actual value, 1 is the error)

b = (0, 0.4) #set bounds
bnds = []
for i in range (0, 2**qubits+1):
    bnds.append(b)
bnds = tuple(bnds)

cons = ({'type': 'ineq', 'fun': inequality_constraint}) #constraint
 
space = 1/(2**qubits+1) #set up initial conditions
initial = []
for i in range (0, 2**qubits+1):
    initial.append(space)

minerror = 100
for ax in range (0, 8):
    print("ax")
    for bx in range (0, 8):
        print("bx")
        for cx in range (0, 8):
            print("cx")
            for dx in range (0, 8):
                for ex in range (0, 8):
                    for fx in range (0, 8):
                        for gx in range (0, 8):
                            for hx in range (0, 8):
                                for ix in range (0, 8):
                                    data = [ax*1.1/64, bx*1.1/64, cx*1.1/64, dx*1.1/64, ex*1.1/64, fx*1.1/64, gx*1.1/64, hx*1.1/64, ix*1.1/64]
                                    currenterror = error(data)
                                    if currenterror < minerror:
                                        minerror = currenterror
                                
print(minerror)

#output = minimize(error, initial, options={"disp": True}, bounds = bnds, constraints=cons)
#print(output.fun)
#print(output.x)