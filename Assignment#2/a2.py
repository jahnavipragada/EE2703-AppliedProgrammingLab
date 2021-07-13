"""
	EE2703 - APPLIED PROGRAMMING LAB - 2020
	ASSIGNMENT-2 ( Solving the circuits and printing all variables )
	EE19B049 ( Jahnavi Pragada )
"""
import sys	
import numpy as np
import math

#Checking for input file
if len(sys.argv) == 2:									
	if sys.argv[1].split(".")[1] != "netlist":		
		print("ERROR:Incorrect input file type")
	else:
		start = -1; end = -2; GND = 0; node = 0; interoutput = [];	x=[]; ac = 0; AC = 0; m=0; v=0	
		CIRCUIT = ".circuit";END = ".end";ALT = ".ac"	#Variables

#Saving tokens			
		with open(sys.argv[1]) as file: 
			lines = file.readlines()
			
			for i in range(0,len(lines)):
				if lines[i][:len(CIRCUIT)]==CIRCUIT:
				   start = i   					#Storing the index of line with .circuit in variable start
				elif lines[i][:len(END)]==END:
				   end = i			   			#Storing the index of line with .end in variable end
				elif lines[i][:len(ALT)]==ALT:
					ac = lines[i].split()		#Storing tokens of line with .ac separately
					AC =i						#Storing the index of line with .ac in variable AC
					w=2*math.pi*float(ac[-1])	#Angular frequency of ac source

			if AC<end:
				AC = 0			#if .ac is with in the circuit then it is useless.So removed
			if start >= end: 
			    print("INVALID CIRCUIT IN THE INPUT FILE")
			else:
				for i in range(start+1,end):
					res = (lines[i].split("#")[0]).split()		
					interoutput.append(res)		#Removing comments and saving tokens
					
#Finding number of nodes in circuit and initiating matrixes of required sizes
				for l in range(0,len(interoutput)):
					
						if interoutput[l][1] == "GND": i = 0	#Reading node values of first side
						else: i = int(interoutput[l][1])							
						if interoutput[l][2] == "GND": j = 0	#Reading node values of second side						
						else: j = int(interoutput[l][2])
					
						if node<max(i,j):
							node = max(i,j)		#Assigning the max value of above to node 

						if interoutput[l][0][0] == "V" : v+=1	#No. of voltage sources
				
				M = [ [ 0 for i in range(node+v) ] for j in range(node+v) ]
				b = [ [ 0 for i in range(node+v) ] for j in range(1) ]
					
				for l in range(0,len(interoutput)):	

#Effect of Passive components on MNA matrix
					if interoutput[l][0][0] == "R" or interoutput[l][0][0] == "C" or interoutput[l][0][0] == "L":
						if interoutput[l][0][0] == "R":	#Assigning Impedence value to k
							k = float(interoutput[l][3])
						if interoutput[l][0][0] == "C":
							k = complex(0,-1/(w*float(interoutput[l][3])))
						if interoutput[l][0][0] == "L":
							k = complex(0,(w*float(interoutput[l][3])))

						if interoutput[l][1] == "GND":
							i = 0
						else:
							i = int(interoutput[l][1])
						if interoutput[l][2] == "GND":
							j = 0
						else:
							j = int(interoutput[l][2])

						if i*j != 0:
							M[i-1][i-1] += 1/k
							M[i-1][j-1] += -1/k
							M[j-1][i-1] += -1/k
							M[j-1][j-1] += 1/k
						if i == 0:
							M[j-1][j-1] += 1/k
						if j == 0:
							M[i-1][i-1] +=1/k

#Process vor Voltage Source
					if interoutput[l][0][0] == "V":
						m+=1
						if interoutput[l][1] == "GND":
							i = 0
						else:
							i = int(interoutput[l][1])
							M[int(node+m-1)][i-1] = 1
							M[i-1][int(node+m-1)] = -1
							if interoutput[l][3] =="ac":								
								b[0][int(node+m-1)] = complex(float(interoutput[l][-2])*math.cos(float(interoutput[l][-1])),float(interoutput[l][-2])*math.sin(float(interoutput[l][-1])))
							else:								
								b[0][int(node+m-1)] = float(interoutput[l][-1])
						if interoutput[l][2] == "GND":
							j = 0
						else:
							j = int(interoutput[l][2])
							M[int(node+m-1)][j-1] = 1
							M[j-1][int(node+m-1)] = -1
							if interoutput[l][3] == "ac":
								b[j-1][0] = complex(float(interoutput[l][-2])*math.cos(float(interoutput[l][-1])),float(interoutput[l][-2])*math.sin(float(interoutput[l][-1])))
							else:
								b[j-1][0] = -float(interoutput[l][-1])	

#Solving and Printing Variables	
				o = np.linalg.solve(M,b[0])
				
				for i in range(0,node+m):
					if AC==0:
						if i<node:print("Voltage at node %d is"%(i+1))
						if i>=node:print("Current through V%d source is"%(i-node+1))
						print(float("%.2f"%o[i]))
					else:
						if i<node:print("Voltage at node %d is"%(i+1))
						if i>=node:print("Current through V%d source is"%(i-node+1))
						print(o[i]) 
						
				
elif len(sys.argv) ==1 : print("Usage: %s \nError: No Input Found \nExpected:FileName.py FileName.netlist" % sys.argv[0])
else: print("Usage: %s \nError:Too Many Inputs Found \nExpected:FileName.py FileName.netlist" % sys.argv)
