#!/usr/bin/env python -w
# python GeckLib.py Human_GeCKOv2_Library_A_3_mageck.txt ../BarCode1.fastq ../BarCode1.fastq,../BarCode1.fastq L1
# Usage: python GeckLib.py Human_GeCKOv2_Library_A_3_mageck.txt test.fastq Control.fastq out.txt

import sys, os

arrA=sys.argv[2].replace(","," ")
TEMP_T = "TEMP_T_"+sys.argv[4]
cmd = "cat "+arrA+"| jellyfish count -m 20 -s 100M -t 32 -o "+TEMP_T+" /dev/fd/0"
os.system(cmd)
cmd1 = "jellyfish dump -c -t "+TEMP_T+" -o Test"+sys.argv[4]+".cov"
os.system(cmd1)
cmdDel="rm -r "+"TEMP_T_"+sys.argv[4]
os.system(cmdDel)

arr=sys.argv[3].replace(","," ")
TEMP_C = "TEMP_C_"+sys.argv[4]
cmdC = "cat "+arr+"| jellyfish count -m 20 -s 100M -t 32 -o "+TEMP_C+" /dev/fd/0"
os.system(cmdC)
cmd2 = "jellyfish dump -c -t "+TEMP_C+" -o Control"+sys.argv[4]+".cov"
os.system(cmd2)
cmdDel="rm -r "+"TEMP_C_"+sys.argv[4]
os.system(cmdDel)

count1 =0
keys = list()
values = list()
values2 = list()
f = open(sys.argv[1],'r')
# HGLibA_37592	CGAGTCGTTCTTGCTCTTCG	POLR2J
for line in f:
	line=line.rstrip('\n') # Deletes the new line character
	a=line.split("\t") # Splits with tab
	keys.append(a[1])
	values.append(a[2])
	values2.append(a[0])
	count1=count1+1

Gene_Lib = dict(zip(keys,values))
sgRNA_Lib = dict(zip(keys,values2)) 


#######################
counttest =0
testkey=list()
testvalue=list()
Test="Test"+sys.argv[4]+".cov"
f2 = open(Test, 'r')
for line2 in f2:
    line2=line2.rstrip('\n') # Deletes the new line character
    a2=line2.split("\t") # Splits with tab
    testkey.append(a2[0])
    testvalue.append(int(a2[1]))
    counttest=counttest+1

test_lib = dict(zip(testkey,testvalue))

########################
countControl=0
controlkey=list()
controlvalue=list()
Control="Control"+sys.argv[4]+".cov"
f3=open(Control,'r')
for line2 in f3:
        line2=line2.rstrip('\n') # Deletes the new line character
        a2=line2.split("\t") # Splits with tab
        controlkey.append(a2[0])
        controlvalue.append(int(a2[1]))
        countControl=countControl+1
f3.close()
control_lib = dict(zip(controlkey,controlvalue))


Outname = sys.argv[4]
FDW = open(".".join([Outname, "count.txt"]),'w')
FDWGene = open(".".join([Outname, "Gene.txt"]),'w')

FDW.write("sgRNA\tGene\t"+Outname+"\tCTRL\n")
FDWGene.write("sgRNA\tGene\t"+Outname+"\tCTRL\n")

for key in Gene_Lib:
  	if key in test_lib and key in control_lib:
	        FDW.write(sgRNA_Lib[key]+"\t"+Gene_Lib[key]+"\t"+str(test_lib[key])+"\t"+str(control_lib[key])+"\n")
		FDWGene.write(sgRNA_Lib[key]+"\t"+Gene_Lib[key]+"\t"+str(test_lib[key])+"\t"+str(control_lib[key])+"\n")
	elif key in test_lib:
                FDW.write(sgRNA_Lib[key]+"\t"+Gene_Lib[key]+"\t"+str(test_lib[key])+"\t"+str(0)+"\n")
		FDWGene.write(sgRNA_Lib[key]+"\t"+Gene_Lib[key]+"\t"+str(test_lib[key])+"\t"+str(0)+"\n")
	elif key in control_lib:
                FDW.write(sgRNA_Lib[key]+"\t"+Gene_Lib[key]+"\t"+str(0)+"\t"+str(control_lib[key])+"\n")
	else:
		FDW.write(sgRNA_Lib[key]+"\t"+Gene_Lib[key]+"\t"+str(0)+"\t"+str(0)+"\n")




cmdDel="rm -r "+"Test"+sys.argv[4]+".cov"
os.system(cmdDel)
cmdDel="rm -r "+"Control"+sys.argv[4]+".cov"
os.system(cmdDel)
