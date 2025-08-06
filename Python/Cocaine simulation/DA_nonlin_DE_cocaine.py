# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import cocaine_in_rat_brain as coc
import kernel_smooth as ks

#final model incoorperates all of the previous scripting with the addition of the
#effect of cocaine of striatal dopamine release dynamics, specifically uptake
#inhibition, increasing the MM constant Kapp meaning lower uptake = more dopamine
#stays in the synaptic cleft
def DA_modeling3():
    N0 = 3000 ## molecules released pr release
    P = 0.08 #release prob
    alfa = 0.2 #DA can be release into 20# of availble volume, thus only in free extracellular space. 
    #ie it cannot be released into the cell.
    Na = 6.022E23#advogrados number
    n = 100
    p1 = 0.0006#density of terminals for single DA axon. 0.0006 in NA, 0.001 in Dorsal Striatum. 
    gamma0=((N0*P)/(alfa*Na))*p1*1E24 # 

    Vmax = n*15 
    
    G=gamma0*n #DA in nM if all DA neurons fire one AP simultaniously 
    gamma_soma = 20  #(in nano molar)
    Vmax_soma = 200  #(i nanomolar)
    A = 0.008  #somatodendritic inhibition constant units: Hz/nM
    
    Km=160 #MM.nM. 
    
    Tmax = 200 #s
    dt=0.01 #in s
    t = np.linspace(0,Tmax, Tmax/dt+1)
    Nmax=len(t) 
    cDAsoma = np.zeros(Nmax) 
    cDAstriatum = np.zeros(Nmax) 
    D2pre = np.zeros(Nmax) 
    Pr = np.zeros(Nmax)  
    
    k_on = 1e-2 # Presyn AR: On rate in nanomolar! nM^-1 * s^-1
    k_off = 0.4 #Presyn AR off rate! s^-1
    Pmin = 0.03 
    Pmax = 0.15 
    Pr[0] = Pmax  
    
    nu_in= 5*np.ones(Nmax) #Hz
    nu_eff = np.copy(nu_in)
    
    Ki = 0.35 #inhibition constant for competive uptake inhibitor
    D = 3  #(mg pr kg, iv) cocaine dose
    tinfusion = 10 #time of cocaine infusion
    #construct a cocaine concentration time evolution given the simulation time vector,
    #time of infusion and cocaine dose
    C_coc = coc.cocaine_in_rat_brain(t, tinfusion, D)
    #new MM K value from cocaine effect
    Kapp = Km*(1 + C_coc/Ki)
    
    #data from FSCV to compare with simulation
    temp = "C:\Users\Claus\Dropbox\Kursus\Python\Cocaine simulation\core_coc.csv"
    #time points from data
    Tcoc = np.genfromtxt(temp, dtype=float, delimiter=',',usecols=(0))
    
    NAcore_coc = np.genfromtxt(temp, dtype=float, delimiter=',',usecols=(1,2,3,4,5))
    NAcore_coc = 1000*NAcore_coc

    
    #soma loop, modifying nu from autoinhib
    for k in range(1,Nmax):
        deltaC = ( gamma_soma*nu_eff[k-1] - Vmax_soma*cDAsoma[k-1]/(Kapp[k-1]+cDAsoma[k-1]) ) * dt
        cDAsoma[k] = cDAsoma[k-1] + deltaC
        nu_eff[k] = max([nu_in[k] - A*cDAsoma[k], 0])

    #create spiking functions
    RAS = np.zeros((n,Nmax))
    for k in range(0,n):
        RAS[k] = np.random.poisson(nu_eff*dt)
    F = sum(RAS,0)/dt

    #nu_in vs nu_eff
    plt.figure(1)
    plt.plot(t, nu_in, t, nu_eff)
    plt.xlabel('time, s')
    plt.ylabel('Frequency (Hz)')
    plt.title('DA neuron firing freq over time')
#    plt.xticks(np.arange(0,16,1))
#    plt.yticks(np.arange(0,21,2))
    plt.draw()
    plt.waitforbuttonpress()

    #F and smoothed F
    plt.figure(2)
    plt.plot(t, F, t, ks.kernel_smooth(F,10))
    plt.xlabel('time, s')
    plt.ylabel('summed firing freq of n neurons')
    plt.title('summed firing freq of n neurons over time')
#    plt.xticks(np.arange(0,16,1))
#    plt.yticks(np.arange(0,21,2))
    plt.draw()
    plt.waitforbuttonpress()

    
    # Calculation of real firing rates based on somatodendritic autoinhibition
    # Trick: We can calculate s.d. DA before everything else because there is
    # no reverse interaction
    for k in range(1,Nmax):
        dD2pre = ( k_on*cDAstriatum[k-1]*(1-D2pre[k-1]) - k_off*D2pre[k-1] ) * dt
        D2pre[k] = D2pre[k-1] + dD2pre
        
        Pr[k] = (Pmin - Pmax)*D2pre[k] + Pmax
        #note how the effect of cocaine is on the MM model of reuptake giving slower rate
        deltaC = (gamma0/P*Pr[k-1]*F[k-1] - Vmax*cDAstriatum[k-1]/(Kapp[k-1] + cDAstriatum[k-1]) ) * dt
        
        cDAstriatum[k] = cDAstriatum[k-1] + deltaC
        
        
    
    plt.figure(3)
    plt.plot(t,cDAstriatum, t, cDAsoma)
    plt.xlabel('time, s')
    plt.ylabel('DA, nM')
    plt.title('DA conc over time')
#    plt.xticks(np.arange(11))
#    plt.axis([0,10,0,450])
    plt.draw()
    plt.waitforbuttonpress()
    
    plt.figure(4)
    plt.plot(t,D2pre)
    plt.xlabel('time, s')
    plt.ylabel('D2^{pre}, nM')
    plt.title('Presynaptic D2over time')
 #   plt.xticks(np.arange(11))
 #   plt.axis([0,10,0,450])
    plt.draw()
    plt.waitforbuttonpress()


    plt.figure(5)
    plt.plot(Tcoc, NAcore_coc, t, cDAstriatum.tolist())
    plt.show()
    
    
    
def main():
    DA_modeling3()

main() 