import re
import sys, os

# nohup python /data2/sequencer/GECKO_DR/Summarizer.py A_CAll &

keys = list()
values = list()
count1=0
count=0

type = sys.argv[1]

for i in range(1,9):
		file = open("".join([str(i),type,".count_normalized.txt"]), "r")
		for line in file:
			line=line.rstrip('\n')
			if "_CAll" in line:
				count=count+1
			else:
				a = line.split("\t")
				if int(float(a[2])) != 0:
        				keys.append(a[0])
        				values.append(a[1])
		        		count1=count1+1
		file.close()

Gene_Lib = dict(zip(keys,values))
#FDW = open(".".join([Outname, "count.txt"]),'w')			
FDW = open("GeneExp.txt",'w')
FDW2 = open("GeneExp_HM.txt",'w')

for keys in Gene_Lib:
	FDW.write(keys+"\t"+Gene_Lib[keys]+"\t")
	FDW2.write(keys+"\t"+Gene_Lib[keys]+"\t")
	for i in range(1,9):
		file = open("".join([str(i),type,".count_normalized.txt"]), "r")
		count =0
                for line in file:
                        line=line.rstrip('\n')
                        a = line.split("\t")
			if a[0] == keys:
				FDW.write("{:.2f}".format(float(a[2]))+"\t")
				if float(a[2]) > float(a[3]):
					FDW2.write("1\t")
				elif float(a[2]) < float(a[3]):
					FDW2.write("-1\t")
				else:
					FDW2.write("0\t")
				count=1	
		if count==0:
			FDW.write("0"+"\t")
			FDW2.write("0"+"\t")
		file.close
	FDW.write("\n")
	FDW2.write("\n")
