def cocaine_in_rat_brain(*arg):
    import numpy as np
    #modellerer coke i hjernen over tiden t i sekunder.... t0 er infusionstid og D er dosis i
    #mg/kg; Data fra PAN et al 1991, Differences in the Pharmacokinetics of Cocaine, J. Neurochem. Modellen er for IV dosering!!!
    t = 0
    t0 = 0
    Dose = 7.5
    if len(arg)==3:
        t = arg[0]
        t0 = arg[1]
        Dose = arg[2]       
    if len(arg)==2:
        t = arg[0]
        t0 = arg[1]
        Dose = 7.5
    if len(arg)<2:
        t = arg[0]
        t0 = 0        
        Dose = 7.5
    if ( len(arg) == 0 or not(type(arg[0])==np.ndarray) ):
        print "Error: Function takes atleast one ndarray argument"
        return 0
    
    
    
    d_v2 = 124*Dose/7.5
    k12 = 0.332/60
    k21 = 0.182/60
    kel = 0.468/60
    
    sumk = k12+k21+kel
    D = np.sqrt(sumk**2 - 4*k21*kel)    
    
    a = 0.5*(sumk + D)
    b = 0.5*(sumk - D)
    
    expA = np.exp( -a*np.array([t[k]-t0 for k in range(0, len(t))]) )
    expB = np.exp( -b*np.array([t[k]-t0 for k in range(0, len(t))]) )
    
    C = d_v2*k12/(a-b) * ( expB - expA ) 
    
    tcoc = 1*(t>t0)
    
    c2 = np.multiply(C,tcoc)
    
    return c2