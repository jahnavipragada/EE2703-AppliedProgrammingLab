"""
	EE2703 - APPLIED PROGRAMMING LAB - 2020
	ASSIGNMENT-1 ( Reading the Input file to construct circuit )
	EE19B049 ( Jahnavi Pragada )
"""



import sys							#Getting the user input data

if len(sys.argv) == 2:						#Checking whether input is given or not
	if sys.argv[1].split(".")[1] != "netlist":		#Checking whether input file is netlist or not
		print("ERROR:Incorrect input file type") 	#If not then printing error message
	else:							#If yes then process begins
		start = -1		#Initialising a variable name "start" and assigning "-1" to it 
		end = -2		#Initialising a variable name "end" and assigning "-2" to it
		output = []		#Initialising an array these three variables will be used later on
		CIRCUIT = ".circuit"
		END = ".end"
							
		with open(sys.argv[1]) as file:  #Given Input file is stored in "file" 
			lines = file.readlines() #Read th file
			
			for i in range(0,len(lines)):		#Determining the section contains the circuit
				if lines[i][:len(CIRCUIT)]==CIRCUIT:
				   start = i   
				elif lines[i][:len(END)]==END:
				   end = i			   
				   break
			
			if start >= end:	#If .end comes .before circuit then the Circuit is Invalid  
			    print("INVALID CIRCUIT IN THE INPUT FILE")
			else:
				for i in range(start+1,end): #range is given in this way to avoid .circuit & .end
					res = (lines[i].split("#")[0]).split() #Removing comments and splitting the words and storing in res list			
					res.reverse()		#Reversing the list
					output.append(res)	#reversed list is added into ouput array
				output.reverse()		#Output array is reversed
				print(*output,sep="\n") 	#Printing the array vertically
							
elif len(sys.argv) ==1 : print("Usage: %s \nError: No Input Found \nExpected:FileName.py FileName.netlist" % sys.argv[0])		#Printing error msg for not giving input
else: print("Usage: %s \nError:Too Many Inputs Found \nExpected:FileName.py FileName.netlist" % sys.argv)	#Printing error msg for giving multiple inputs
