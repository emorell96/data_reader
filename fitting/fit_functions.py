import numpy as np
import sys

#Je definis ici toutes les fonctions que je vais utiliser pour fiter les données
def expone(x,a,b,c,d):
    
    res=a*(1-d*np.exp(-(x-b)/c))
    
    return res



def multi_peak(x,*p):
    res=p[10]*np.exp(-((x-p[0])**2/(p[1]**2)))*(p[2] / (((x-p[3])/p[4])**2 + 1) +p[5]+p[6] / (((x-p[7])/p[8])**2 + 1) +p[9])
    return res




def double_lorentz(x,*p):
    #p0 = p[0]
    #sum = 0
    #for i in range(0,5, 3):
    #    sum += p[i] / (((x-p[i+1])/p[i+2])**2 + 1)
    return p[0] / (((x-p[1])/p[2])**2 + 1) + p[3] / (((x-p[4])/p[5])**2 + 1) 
    #return sum
def lorentz(x,*p):
    
    return p[0] / (((x-p[1])/p[2])**2 + 1) +p[3]
