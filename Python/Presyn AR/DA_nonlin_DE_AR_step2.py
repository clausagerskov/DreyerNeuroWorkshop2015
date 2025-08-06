#import required libraries
import numpy as np
import matplotlib.pyplot as plt
import kernel_smooth as ks

#Part a of Dreyer 2013 model using script from before, upgraded with autoreceptors, i.e. receptors in the dopamine neurons' presynapse that
#modulate internal processes in the cell controlled by the cells own firing and dop release.
#part b introduces somatic and striatal dop parts, giving somatodendritic autoinhibition by ARs in addition to the presyn AR from part a
#define main function, takes no arguments
def DA_modeling2b():
    
    No=3000 # molecules released pr release
    P=0.08 #release prob
    alfa=0.2 #DA can be release into 20% of availble volume, thus only in free extracellular space. 
    #ie it cannot be released into the cell.
    #power operator in python is **
    Na=6.022*10**23 #advogrados tal
    n=100
    p1=0.001 # density function
    # 1um^3=10^15L
    
    gamma0=((No*P)/(alfa*Na))*p1*1e24
    Vmax=n*40 
    
    G=n*gamma0 #DA in nM if all DA neurons fire one AP simultaniously 
    gamma_soma = 20 #somatic DA release conc
    Vmax_soma = 200
    A = 0.008 #experimentally observed constant for calculating nu_eff

    km=160 #MM.nM
    Tmax=20 #s
    dt=0.01 #in s
    t=np.linspace(0,Tmax,Tmax/dt+1)        
    Nmax=t.size    
	#somatic cDA conc
    cDAsoma = np.zeros(Nmax).tolist() #convert np array to list as otherwise the plot function gets confused 
    #striatal volume cDA conc
    cDAstriatum = np.zeros(Nmax).tolist()
    #occ of presyn ARs
    D2pre = np.zeros(Nmax)
    #release prob
    Pr = np.zeros(Nmax)
    
    kon = 10e-3
    koff = 0.4
    Pmin = 0.03
    Pmax = 0.15
    Pr[0] = Pmax

	#firing rate in the absence of somatodendritic AR autoinhibition
    nu_in = 5*np.ones(Nmax)
	#effective firing rate from autoinhibition
    nu_eff = np.copy(nu_in)
        
    
    tph = [3, 3.8, 7, 14]
    dtph = [0.2, 0.2, 1.5, 0.2]
    nuph = [25, 25, 60, 25]
        
    for k in range(0,len(tph)):
        indx = np.where((tph[k] < t) & (t < tph[k] + dtph[k]))
        nu_in[indx] = nuph[k]
    


    # Calculation of real (effective) firing rates based on somatodendritic autoinhibition
    # Trick: We can calculate s.d. DA before everything else because there is
    # no reverse interaction
    for k in range(1,Nmax):
		#somatic cDA depends on nu_eff and still contains reuptake part
        deltaC = ( gamma_soma*nu_eff[k-1] - Vmax_soma*cDAsoma[k-1]/(km+cDAsoma[k-1]) ) * dt
        cDAsoma[k] = cDAsoma[k-1] + deltaC
		#nu_eff is achieved from autoinhibitory GIRK channels that inhibit firing dep. on cDAsoma
		#max(-,0) because we cannot have negative firing rates
        nu_eff[k] = max([nu_in[k] - A*cDAsoma[k], 0])

	#construct the firing functions from nu_eff
    RAS = np.zeros((n,Nmax))
    for k in range(0,n):
        RAS[k] = np.random.poisson(nu_eff*dt)
    F = sum(RAS,0)/dt

	#plot intrinsic/ideal nu vs actual nu, nu_eff as a result of autoinhibition
    plt.figure(1)
    plt.plot(t, nu_in, t,nu_eff)
    plt.xlabel('time, s')
    plt.ylabel('Frequency, Hz')
    plt.title('DA neuron firing freq over time')
#    plt.xticks(np.arange(0,16,1))
#    plt.yticks(np.arange(0,21,2))
    plt.draw()
    plt.waitforbuttonpress()
    
	#same as other two scripts
    plt.figure(2)
    plt.plot(t,F, t, ks.kernel_smooth(F,10))
    plt.title('summed firing freq of n neurons over time')
    plt.xlabel('time, s')
    plt.ylabel('summed firing freq of n neurons')
    plt.draw()
    plt.waitforbuttonpress()
    

	#striatal cDA time evolution is evolving as before, except that firing patterns are change through autoinhib
    for k in range(1,Nmax):
        dD2pre = ( kon*cDAstriatum[k-1]*(1-D2pre[k-1]) - koff*D2pre[k-1] ) * dt
        D2pre[k] = D2pre[k-1] + dD2pre
        
        Pr[k] = (Pmin - Pmax)*D2pre[k] + Pmax
        
        deltaC = (gamma0/P*Pr[k-1]*F[k-1] - Vmax*cDAstriatum[k-1]/(km + cDAstriatum[k-1]) ) * dt
        
        cDAstriatum[k] = cDAstriatum[k-1] + deltaC
        
        
    #compare striatal and somatic cDA
    plt.figure(3)
    plt.plot(t,cDAstriatum, t, cDAsoma)
    plt.xlabel('time, s')
    plt.ylabel('DA, nM')
    plt.title('DA conc over time')
#    plt.xticks(np.arange(11))
#    plt.axis([0,10,0,450])
    plt.draw()
    plt.waitforbuttonpress()
    
	#show AR occ.
    plt.figure(4)
    plt.plot(t,D2pre)
    plt.xlabel('time, s')
    plt.ylabel('D2^{pre}, nM')
    plt.title('Presynaptic D2over time')
 #   plt.xticks(np.arange(11))
 #   plt.axis([0,10,0,450])
    plt.draw()
    plt.waitforbuttonpress()
    plt.close("all")
    
    
    
def main():
    DA_modeling2b()

main()

