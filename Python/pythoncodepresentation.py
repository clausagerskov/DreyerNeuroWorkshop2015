# -*- coding: utf-8 -*-
#-----import statements-----#

# this is a comment
# get the needed libraries to do math and plot figures we write
import numpy as np
import matplotlib.pyplot as plt
#import csv
import kernel_smooth as ks

#-----creating/assigning new variables-----#
a = 2 # assign variable a the integer value 41
b = 5 # b is integer 13
a = b # assign a the value stored in b (not always the result of = !!)

#-----basic scalar operations and "printing"-----#
c = a * b
d = a ** b
e = a / b

print "value of a:", a # prints 41 on screen
print "value of b:", b # prints 13 on screen
print "value of c = a*b:", c # prints a times b
print "value of d = a^b:", d # prints a^b
print "value of e = a/b:", e # prints what on screen?

# compare to this statement
a = 2. # assign the variable a to the floating point value 2.0
       # i.e. now python cares about the decimal values

print "value of a/b:", a / b # so in python filetypes matter (as opposed to matlab)

#-----vectors and vector operations-----#

# we can define a list of values, a vector, by writing
vecA = [1, 5, 3, 6]
print "\nvalue of vecA:", vecA # print the full vecA vector on screen
print "value of vecA[1]:", vecA[1] # print the SECOND value of vecA on screen
print "value of vecA[0]:", vecA[0] # print the first value of vecA on screen
print "length of vecA:", len(vecA) # how large is the vecA vector?

# combining vectors
vecB = [2, 5, 1, 7] 
vecC = [vecA, vecB]
print "length of vecC:", len(vecC), "x",len(vecC[0]) #
print "vectC:", vecC
print "first row of vecC:", vecC[0][0], vecC[0][1], vecC[0][2], vecC[0][3]
print "second row of vecC:", vecC[1][0], vecC[1][1], vecC[1][2], vecC[1][3]

#print vecA*vecB # doesnt work!
print "vecA times 2:", vecA*2, "\n" # doubles the number of vector elements
              # i.e. now is size 8 vector

#-----numpy-----#
#solution: numpy library! (or if you insist on using lists then do [x*2 for x in vecA])
# numpy allows for more complicated math and easier matrix creation
matA = np.ones((2,2)) # matA = 2 by 2 matrix of ones
vecB = np.zeros(2) + 2 # vecB = 2d vector of zeros added value 2
matC = np.identity(2) # matC = identity matrix
matD = np.array([2, 7, 1, 4])


print "matA:", matA, "size of matA:", np.shape(matA),"\n", \
        "vecB:", vecB, "size of vecB:", np.shape(vecB), "\n", \
        "matC:", matC, "size of matC:", np.shape(matC)
print "matA.vecB:", np.dot(matA, vecB) # dot product operation
print "matA*3:", matA*3, "\n"
# but beware of numpy arrays (matrices)
matA = matC # this does not mean "assign value of matC to matA"!
            # it means "make matA variable point to 
            # the same memory location as matC"
   
#hvad sker der hvis man skriver: matD*matD? Elementvis multiplikation?
         
# this has the following consequence:
matA += 2
print "matA + 2:", matA
print "matC:", matC, "\n"

# instead do copy()
matC = np.identity(2) # matC = identity matrix
matA = np.copy(matC) 
print "matA:", matA, "\n", "matC:", matC, "\n"
matA += 2
print "matA after adding:",matA, "\n", "matC after adding:", matC, "\n"

#-----making increasing arrays/linspaces-----#
vecD = np.arange(0,10,1)
print "vecD:", vecD

vecE = np.arange(0,5,0.5)
print "vecE:", vecE
#OR if you want to make sure you have consistent endpoints:
vecF = np.linspace(0,10,11)
print vecF
#linspace has endpoint included as standard and uses n_steps instead of stepsize
# it is possible to convert from stepsize to n_steps by: 
#            n_steps = max/stepsize + 1


#-----strings-----#
a = "hello world"
print a

#-----if statements (logical statements)-----#
statement = False
if (statement == True): # or more compactly just statement
    print "it's true!"
elif (statement == False): # alt. statement != True or more compactly not(statement)
    print "it's false!"
else:
    print "variable is not boolean!"
    
# combining multiple truth checks with and or
st1 = True
st2 = False
if (st1 and st2):
    print "both statements are true"
if (st1 or st1):
    print "atleast one statement is true (logical or)"
if ( (st1 and not(st2)) or (st2 and not(st1)) ):
    print "statement1 or statement2 is true (logical xor)"
    if(st1):print "statement1 is true"
    else:print "statement2 is true"


# logic tables:
#       st1 | st2
# and:   1  |  1    ->  1
#        0  |  1    ->  0
#        1  |  0    ->  0   
#        0  |  0    ->  0
#
# or:    1  |  1    ->  1
#        1  |  0    ->  1
#        0  |  1    ->  1
#        0  |  0    ->  0
#
# xor:   1  |  1    ->  0
#        1  |  0    ->  1
#        0  |  1    ->  1
#        0  |  0    ->  0
    

#-----loops-----#
# while loop = doing something as long as a statement is true
t = 0
while t < 10: # each run of the loop the validity of this statement is checked
    print "t: %i" % t
    t += 1
#beware of infinite loops!
#while t < 5:
#    print "t: %i" % t # forgot to add t += 1 so condition is never false. Do not run this! 
print "\n"
# for loop
for t in range(0,10): # at the moment does the same thing, but more powerful
    print "t: %i" % t

print "\n"
# nested for loops can run through matrices
vecC = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
for x in range(0, len(vecC)):
    for k in range(0, len(vecC[0])):
        print vecC[x][k]

print "\n"

for t in [5., 10., 4., 2.5, 3.]: # for loop can loop through any list
    for k in ["horses", "cats", "pigs", "squirrels"]:
        print t, k
        
#-----plotting-----#
# to plot figures in python we imported the matplotlib library
# in the beginnning of this script
# it is made to be similar to plotting in matlab
#first we create something to plot

plt.close("all")
dt = 0.01
t = np.linspace(0,2.5,2.5/dt+1)
n = 100
Nmax = len(t)
nu = 5*np.ones(Nmax)
RAS = np.zeros((n,Nmax))
for k in range(0,100):
    RAS[k] = np.random.poisson(nu*dt)
F = sum(RAS,0)/dt

plt.figure(1) # first we create a figure window (this will not show yet)
plt.plot(t,F,t, ks.kernel_smooth(F, 10) )
plt.xlabel('time')
plt.ylabel('probability')
plt.title('random distribution')
#plt.xticks(np.arange(11))
#plt.axis([0,10,0,450])
plt.show()
#or if running from terminal
#plt.draw()
#plt.waitforbuttonpress()
plt.figure(2) # first we create a figure window (this will not show yet)
plt.plot(t,np.sin(t),'r-')
plt.show()
#-----data files-----#
# how to import/export csv files

#importing
csvfile = "C:\Users\Claus\Dropbox\Kursus\Python\datafile.csv"
M = np.genfromtxt(csvfile, dtype=float, delimiter=',')
print M
print M[0][3]
print len(M),"by",len(M[0])

#exporting
np.savetxt("C:\Users\Claus\Dropbox\Kursus\Python\exporteddata.csv", M, delimiter=',')

#-----other useful functions-----#
# the where function
Tmax = 15
dt=0.1
t = np.arange(0,Tmax,dt)
nu_in = np.zeros(len(t))
tph = [3, 3.8, 7, 14]
dtph = [0.2, 0.2, 1.5, 0.2]
nuph = [25, 25, 60, 25]
    
for k in range(0,len(tph)):
    indx = np.where((tph[k] < t) & (t < tph[k] + dtph[k]))
    nu_in[indx] = nuph[k]

#-----creating functions-----#
def exampleFunction(matSize, x, y):
    unMat = np.identity(matSize)
    return unMat, x+y

def main():
        M, z = exampleFunction(10,2,6)
        print M, "\n", z
    
main()