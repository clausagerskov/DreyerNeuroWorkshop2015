#import required libraries
import numpy as np
import matplotlib.pyplot as plt
import kernel_smooth as ks

#first model is simple non-dimentional approximated concentration time evolution
#consisting of a spike release and reuptake. Instead of explicit space solving, 
#we look at average volume concentration (ref. Dreyer 2010). Also different from
#reference is that tonic level is represented as a baseline spike freq.
#define main function, takes no arguments
def DA_modeling1():
    
    No=3000 # dopamine transmitter molecules released pr release
    P=0.08 #vesicle release prob 
    alfa=0.2 #vol fract of extracellular space
             #DA can be release into 20% of availble volume, thus only in free extracellular space. 
             #ie it cannot be released into the cell.
    #power operator in python is **
    Na=6.022*10**23 #advogrados number
    n=100 #number of projecting neurons
    p1=0.001 # density of terminals on a single axon
   	
    # 1um^3=10^15L
    gamma0=((No*P)/(alfa*Na))*p1*1e24 #gamma0*F(t) = I(t) in the paper Dreyer 2010
                                      #represents dopamine release from one AP neuron spike
    
    G=gamma0*n #DA in nM if all DA neurons fire one AP simultaniously 
    Vmax=n*40 #Michaelis-Menten uptake parameter
    km=160 #MM.nM Michaelis-Menten uptake parameter
    
    Tmax=20 #s Simulation end time
    dt=0.01 #in s, simulation time step size
   	#create an array of values with start 0 and end Tmax, and spacing dt
    #(stop set to Tmax + dt, as arange gives 
    #array [start, end[, e.g. not including endpoint, 
    #python does not generally include endpoints where MATLAB does)
    #furthermore, python starts counting at 0, not 1
    t=np.linspace(0,Tmax,(Tmax/dt+1)) #times of simulation
    Nmax=t.size # amount of time steps
    cDA=np.zeros(Nmax).tolist() #vector to hold concentration values at all simulated times
                                #convert np array to list as otherwise the plot function gets confused 
    nu=4*np.ones(Nmax) #Hz, neuron firing frequency vector for all times, i.e. tonic baseline
    
   	#manual insertion of bursts and pauses
    tph = [3, 5, 7, 13] #times of change in act from baseline
    dtph = [1, 0.2, 0.2, 0.2] #length of burst/pause event
    nuph = [0, 20, 60, 20] # avr event frequency
    
    #insert burst and pause events into the firing freq. vector
    for k in range(0,len(tph)):
        indx = np.where((tph[k] < t) & (t < tph[k] + dtph[k]))
        nu[indx] = nuph[k]
    
    #create matrix to hold neuron activities for n neurons over Nmax time steps
    RAS = np.zeros((n,Nmax))
    #each neuron's activity is a poisson random distribution defined with 
    #the firing freq and the time interval dt (see numpy.random.poisson doc, 
    #f(k,lam) = lam^k*exp(-lam)/k!). Bursts and pauses are simulated as 
    #synchronous for all neurons
    for k in range(0,n):
        RAS[k] = np.random.poisson(nu*dt)
    #average firing of all neurons for time interval dt
    F = sum(RAS,0)/dt
    
    #plot the temporal evolution of firing rates
    plt.figure(1)
    plt.plot(t,nu)
    plt.xlabel('time, s')
    plt.ylabel('Frequency, Hz')
    plt.title('DA neuron firing freq over time')
    #    plt.xticks(np.arange(0,11,1))
    #    plt.yticks(np.arange(0,21,2))
    plt.draw()
    plt.waitforbuttonpress()
    
    #smooth poisson function with gaussian kernel 
    smX = ks.kernel_smooth(F,10)
    
    #plot raw F together with smoothed version
    plt.figure(2)
    plt.plot(t,F,t,smX)
    plt.title('summed firing freq of n neurons over time')
    plt.xlabel('time, s')
    plt.ylabel('summed firing freq of n neurons')
    plt.draw()
    plt.waitforbuttonpress()
    
    #solve numerically the time evolution of the dopamine concentration
    #modelled as a release part I(t) = gamma0*F(t) - MM(t), where MM(t) is a 
    #Michaelis-Menten reupdate model, i.e. new dop release minus reuptake
    for k in range(1,Nmax):
        deltaC = ( gamma0*F[k-1] - Vmax*cDA[k-1]/(km+cDA[k-1]) ) * dt
        cDA[k] = cDA[k-1] + deltaC
    
    #plot resulting dopamine concentration evolution
    plt.figure(3)
    plt.plot(t,cDA)
    plt.xlabel('time, s')
    plt.ylabel('DA, nM')
    plt.title('DA conc over time')
    #    plt.xticks(np.arange(11))
    #plt.axis([0,20])
    plt.draw()
    plt.waitforbuttonpress()
    plt.close("all")
def main():
    DA_modeling1()
    
main()