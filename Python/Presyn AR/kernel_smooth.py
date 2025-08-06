def kernel_smooth(X, w):
    import numpy as np
    # smX = kernel_smooth(X, w)
    # Udglatter signalet X ved en Gaussisk kernel af bredde w.
    # Det udglattede signal er normaliseret
    
    if w == 0:
        smX = X
        return smX
    w = 10
    L = 3 # antal standardafvigelser i kernel
    
    i = np.linspace(-(L*w),L*w,2*L*w+1)

    f = 1/np.sqrt(2*np.pi*w**2) * np.exp( -np.multiply(i,i)/( 2*w**2 ) )

    paddedX = np.append(np.zeros(L*w), X)
    paddedX = np.append(paddedX, np.zeros(L*w))
    #print len(paddedX), len(X)
    smX = np.zeros(len(X))
    for k in range(0,len(X)):
            jrange = [(i[h] + L*w+k) for h in range(0,len(i))]
            paddedXSelection = [paddedX[j] for j in (jrange)]
            smX[k] = np.dot(f,paddedXSelection)
    return smX