#import required libraries
import numpy as np
import matplotlib.pyplot as plt
import kernel_smooth as ks
#Part a of Dreyer 2013 model using script from before, upgraded with autoreceptors, i.e. receptors in the dopamine neurons' presynapse that
#modulate internal processes in the cell controlled by the cells own firing and dop release
#define main function, takes no arguments
def DA_modeling2a():
    No=3000 # molecules released pr release
    P=0.08 #vesicle release prob
    alfa=0.2 #DA can be release into 20% of availble volume, thus only in free extracellular space. 
    #ie it cannot be released into the cell.
    #power operator in python is **
    Na=6.022*10**23 #advogrados number
    n=100 #number of neurons projecting
    p1=0.001 # density function of terms on axon
    # 1um^3=10^15L
    
    gamma0=((No*P)/(alfa*Na))*p1*1e24 #dop release for a neural spike
    G=n*gamma0 #DA in nM if all DA neurons fire one AP simultaniously     
    Vmax=n*40 #MM uptake param
    km=160 #MM.nM -||-
    Tmax=20 #s
    dt=0.001 #in s
    t=np.arange(0,Tmax+dt,dt)    
    Nmax=t.size    
    cDA=np.zeros(Nmax).tolist() #convert np array to list as otherwise the plot function gets confused 
    D2pre = np.zeros(Nmax) #occupancy of autoreceptors
    Pr = np.zeros(Nmax) #release prob
        
    kon = 1e-2 #on rate for DA binding to presynaptic AR
    koff = 0.4 #off rate for -||-
    Pmin = 0.02 #lowest value for Pr, when AR are fully activated
    Pmax = 0.15 #highest value for Pr, when AR are fully deactivated
    Pr[0] = Pmax #pr starts at max

#    kmcoc=1000 #nM.15 mg/kg coc ip
    nu=4*np.ones(Nmax) #Hz, initiate firing rate vector to baseline, i.e. 4 Hz

#    gamma0=[x*p1*1e24*No/(alfa*Na) for x in Pr]
    #manually assign bursting and pause
    tph = [3, 5, 7, 13]
    dtph = [1, 0.2, 0.2, 0.2]
    nuph = [0, 20, 60, 20]   
     
    for k in range(0,len(tph)):
        indx = np.where((tph[k] < t) & (t < tph[k] + dtph[k]))
        nu[indx] = nuph[k]
    
	#create firing functions as poisson distributions
    RAS = np.zeros((n,Nmax))
    for k in range(0,n):
        RAS[k] = np.random.poisson(nu*dt)
    #total firing
	#F = sum(RAS,0)/dt
    
	#plot firing rates
    plt.figure(1)
    plt.plot(t,nu)
    plt.xlabel('time, s')
    plt.ylabel('Frequency, Hz')
    plt.title('DA neuron firing freq over time')
#    plt.xticks(np.arange(0,16,1))
#    plt.yticks(np.arange(0,21,2))
    plt.draw()
    plt.waitforbuttonpress()
    
	#plot summed firing as well as smoothed version of F
    plt.figure(2)
    plt.plot(t,F, t, ks.kernel_smooth(F,10))
    plt.title('summed firing freq of n neurons over time')
    plt.xlabel('time, s')
    plt.ylabel('summed firing freq of n neurons')
    plt.draw()
    plt.waitforbuttonpress()

    
    
	#solve equations for dopamine concentration and AR occupancy, as well as resulting firing prob
    for k in range(1,Nmax):
		#change in AR occ. is difference between number of occ times off rate and empty AR sites time kon times cDA
        deltaD2pre = ( cDA[k-1]*kon*(1-D2pre[k-1]) - koff*D2pre[k-1] ) * dt    
        D2pre[k] = D2pre[k-1] + deltaD2pre
		#Pr determined from linear interpolation
        Pr[k] = (Pmin - Pmax)*D2pre[k] + Pmax 
		#update cDA given new Pr
        deltaC = ( gamma0/P*Pr[k-1]*F[k-1] - Vmax*cDA[k-1]/(km+cDA[k-1]) ) * dt
        cDA[k] = cDA[k-1] + deltaC
    
    #plot cDA time evolution
    plt.figure(3)
    plt.plot(t,cDA)
    plt.xlabel('time, s')
    plt.ylabel('DA, nM')
    plt.title('DA conc over time')
#    plt.xticks(np.arange(11))
#    plt.axis([0,10,0,450])
    plt.draw()
    plt.waitforbuttonpress()
    
	#plot AR occupancy time evolution
    plt.figure(4)
    plt.plot(t,D2pre)
    plt.xlabel('time, s')
    plt.ylabel('D2^{pre}, nM')
    plt.title('Presynaptic D2over time')
 #   plt.xticks(np.arange(11))
 #   plt.axis([0,10,0,450])
    plt.draw()
    plt.waitforbuttonpress()
    
	#plot release prob time evo
    plt.figure(5)
    plt.plot(t,Pr)
    plt.xlabel('time, s')
    plt.ylabel('Pr')
#    plt.title('Synaptic release prob')
 #   plt.xticks(np.arange(11))
 #   plt.axis([0,10,0,450])
    plt.draw()
    plt.waitforbuttonpress()
    plt.close("all")
    
def main():
    DA_modeling2a()
    
main()
