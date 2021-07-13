"""
	EE2703 - APPLIED PROGRAMMING LAB - 2021
	Final Exam
	EE19B049 ( Jahnavi Pragada )
"""

# Importing the modules
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

					#Part_2	
#Generating a mesh for volume with dimensions 3*3*1000
x=np.linspace(-1,1,num=3)         # x is assigned 3 points from -1 to 1 seperated by 1 cm.
y=np.linspace(-1,1,num=3)         # y is assigned 3 points from -1 to 1 seperated by 1 cm.
z=np.linspace(0,5000,num=1000)    # z is assigned 1000 points from 1 to 1000 seperated by 1cm.
X,Y,Z=np.meshgrid(x,y,z)          # Breaking the volume into a 3 by 3 by 1000 mesh.



					#Part_3&4
pi = np.pi
rad=10                            #radius given is 10cm      
secs =100                         #loop is divided into 100 sections
l = np.array(list(range(secs)))   #array of size secs 
phi = l*2*pi/secs                 # phi is the angle made by each part of loop with origin.

#Obtaining the vectors required rl and dl where l indexes the segments of the loop
r_l = rad*np.array([np.cos(phi), np.sin(phi), np.zeros(len(phi))]).T                    #defining rl vector
d_l = 2*pi*rad*(1/secs)*np.array([-np.sin(phi), np.cos(phi), np.zeros(len(phi))]).T     #defining dl vector

#Ploting the graph of current in loop
I = 4*pi*(1/(4*pi*1e-7))*np.array([-np.cos(phi)*np.sin(phi), np.cos(phi)*np.cos(phi)]).T #current in each element
plt.figure(0)                                                                            # creating and naming the figure window	
plt.quiver(r_l[:,0],r_l[:,1],I[:,0],I[:,1],label='current vectors')                      # plotting the current vectors using quiver function
plt.xlabel("x $\longrightarrow$")                                                        # naming x-label to the plot
plt.ylabel("y $\longrightarrow$")                                                        # naming y-label to the plot
plt.title("Quiver Plot of Current in the Loop")                                          # giving title to the plot
plt.grid()                                                                               # enabling grid in the axes
plt.show()                                                                               # displaying the output plot



					#Part_5&6
#Calculating Radius vector magnitude and term that is inside sigma of "A" vector. 
def calc(l):                                                        # defining the function calc
    k = 1/rad                                                        #k=1/r as per given data
    x_l, y_l, z_l = r_l[l]                                           #vectors in xyz co-ordinates
    R_ijkl = np.sqrt((X-x_l)**2 + (Y - y_l)**2 + (Z - z_l)**2)       # finding Rijkl i.e the norm ∣∣rijk−rl∣∣
    A_ijkl = np.cos(l*2*pi/100)*np.exp(-1j*k*R_ijkl)/R_ijkl          #magnetic potential at a point
    return A_ijkl                                                    #this is the value returned when function is called



					#Part_7
#Finding A by adding all the terms calculated in above function. 
A_x = np.zeros(X.shape)
A_y = np.zeros(Y.shape)
A_z = np.zeros(Z.shape)
for n in range(secs):                        # for n value ranging from 1 to secs.
  A_ijkl = calc(n)                           # calling the calc function for every value from 1 to secs.            
  A_x = A_x + A_ijkl*d_l[n,0]                # incrementing x component of magnetic potential
  A_y = A_y + A_ijkl*d_l[n,1]                # incrementing y component of magnetic potential
  A_z = A_z + A_ijkl*d_l[n,2]                # incrementing z component of magnetic potential
'''Justification : Equation 1 given is sigma of ((np.cos(l*2*pi/100)*np.exp(-1j*k*Rijkl))*d_l/Rijkl). Using FOR loop we added every term and stored in variables A_x,A_y,A_z.'''



					#Part_8&9
#Finding and ploting the magnetic field along Z-axis
Bz = 0.25*(A_y[1,0,:]-A_x[0,1,:]-A_y[-1,0,:]+A_x[0,-1,:])# computing the Bz values by vectorized operation given in question.

plt.figure(1)                                 # creating and naming the figure window
plt.loglog(z, np.abs(Bz),label= 'Magnetic Field Bz')# plotting Bz vs z in loglog plot
plt.xlabel("z $\longrightarrow$")             # naming x-label to the plot
plt.ylabel("Bz $\longrightarrow$")            # naming y-label to the plot
plt.title("loglog plot of Magnetic field")    # giving title to the plot
plt.grid()                                    # enabling grid in the axes
plt.show()                                   # displaying the output plot



					#Part_10
#Fitting the field to given type
B = np.hstack([np.ones(len(Bz[999:]))[:,np.newaxis],np.log(z[999:])[:,np.newaxis]])
log_c , b = np.linalg.lstsq(B,np.log(np.abs(Bz[999:]))) [0]
c=np.exp(log_c)



