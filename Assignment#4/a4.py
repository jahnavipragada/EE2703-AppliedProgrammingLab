from scipy import integrate
from pylab import *

#Defining required functions
def f1(x):
	return exp(x)
def f2(x):
	return cos(cos(x))
def an1(x,n):
	return f1(x)*cos(n*x)
def bn1(x,n):
	return f1(x)*sin(n*x)
def an2(x,n):
	return f2(x)*cos(n*x)
def bn2(x,n):
	return f2(x)*sin(n*x)
	""" Finding Actual values of fourier series by integration method"""
#Defining range of x
x = linspace(-2*pi,4*pi,1200)
xt = linspace(0,2*pi,400)
t = tile(xt,3)	
#Assigning return values of function to variable
act1 = f1(x)
act2 = f2(x)
#Required variables
f1_coeff = zeros((51,1))
f2_coeff = zeros((51,1))
f1_ser = 0
f2_ser = 0
index = 0
n = arange(1,52)
#Process of finding
for k in range(26):
	ak1 = integrate.quad(an1,0,2*pi,args=(k))[0]/pi	#values of coefficients
	bk1 = integrate.quad(bn1,0,2*pi,args=(k))[0]/pi
	ak2 = integrate.quad(an2,0,2*pi,args=(k))[0]/pi
	bk2 = integrate.quad(bn2,0,2*pi,args=(k))[0]/pi
	
	if k==0:
		f1_ser += ak1/2
		f2_ser += ak2/2
		f1_coeff[index][0] = ak1/2
		f2_coeff[index][0] = ak2/2
		index += 1
	else:
		f1_ser += ak1*cos(k*x) + bk1*sin(k*x)
		f2_ser += ak2*cos(k*x) + bk2*sin(k*x)
		f1_coeff[index][0] = ak1
		f2_coeff[index][0] = ak2
		f1_coeff[index+1][0] = bk1
		f2_coeff[index+1][0] = bk2
		index +=2

	""" Predicting values of fourier series by using lstsq """
#Defining range of y
y = linspace(0,2*pi,401)
y = y[:-1]
#Assigning return values of function to variable
pred1 = f1(y)
pred2 = f2(y)
#Obtaining Matrix
M = zeros((400,51))
M[:,0] = 1
for k in range(1,26):
	M[:,2*k-1] = cos(k*y)
	M[:,2*k] = sin(k*y)
#Finding out coefficient matrix & series values
f1_coeff_pred = lstsq(M,pred1,rcond=None)[0]
f2_coeff_pred = lstsq(M,pred2,rcond=None)[0]
f1_ser_pred = dot(M,f1_coeff_pred)
f2_ser_pred = dot(M,f2_coeff_pred)

	# Difference between the values found in 2 process 
diff1 = abs(f1_coeff - f1_coeff_pred)
diff2 = abs(f2_coeff - f2_coeff_pred)

maxdiff1 = diff1.max()
maxdiff2 = diff2.max()

print("The maximum deviation between the coefficient values of exp(x) obtained in both the methods is " , maxdiff1) 
print("The maximum deviation between the coefficient values of cos(cos(x)) obtained in both the methods is " , maxdiff2)



			#All plots that are asked
			
figure(1)
semilogy(x,f1(x),label='Actual value')
semilogy(x,f1(t),label='Periodic extension')
semilogy(xt,f1_ser_pred,'ob',label='Estimated value')
title("exp(x)")
xlabel(r'$x\rightarrow$',size=15)
ylabel(r'$e^x\rightarrow$',size=15)
grid(True)
legend()

figure(2)
plot(x,f2(x),label='Actual value')
plot(xt,f2_ser_pred,'og',label='Estimated value')
plot(x,f2(t),label='Periodic extension')
title("cos(cos(x))")
xlabel(r'$x\rightarrow$',size=15)
ylabel(r'$cos(cos(x))\rightarrow$',size=15)
grid(True)
legend()

figure(3)
semilogy(n,abs(f1_coeff),'or',label='Actual')
semilogy(n,abs(f1_coeff_pred),'ob',label='Predicted')
title("Semilog plot of coeff.s exp(x)")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid(True)
legend()

figure(4)
loglog(n,abs(f1_coeff),'or',label='Actual')
loglog(n,abs(f1_coeff_pred),'ob',label='Predicted')
title("loglog plot of coeff. exp(x)")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid(True)
legend()

figure(5)
semilogy(n,abs(f2_coeff),'or',label='Actual')
semilogy(n,abs(f2_coeff_pred),'og',label='Predicted')
title("Semilog plot of coeff. cos(cos(x))")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid(True)
legend()

figure(6)
loglog(n,abs(f2_coeff),'or',label='Actual')
loglog(n,abs(f2_coeff_pred),'og',label='Predicted')
title("loglog plot of coeff. cos(cos(x))")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid(True)
legend()


show()

