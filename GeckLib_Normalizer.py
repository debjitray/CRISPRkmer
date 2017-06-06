import re
import sys, os

# Usage : python GeckLib_Normalizer.py 1A_CAll

A_Call = sys.argv[1]


cmd = "mageck test -k "+A_Call+".count.txt -t "+A_Call+" -c CTRL -n "+A_Call
os.system(cmd)

file = open(".".join([A_Call, "log"]), "r")

Sample = 0
Control= 0

for line in file:
	if "Initial (total) size factor" in line:
		a = line.split(" ")
		Sample = a[12]
		Control = a[11]

file.close()

file = open(".".join([A_Call,"count.txt"]), "r")
FDW = open(".".join([A_Call, "count_normalized.txt"]),'w')

for line in file:
	line=line.rstrip('\n')
	a=line.split("\t")
	if A_Call in line:
		FDW.write(line)
		FDW.write("\n")
	else:
		a=line.split("\t")
		FDW.write(a[0]+"\t"+a[1]+"\t"+str(float(a[2])*float(Sample))+"\t"+str(float(a[3])*float(Control))+"\n")
