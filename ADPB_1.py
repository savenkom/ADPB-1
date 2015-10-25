import sys
import re
f=open(sys.argv[1], 'r')
contents = f.readlines()
#print contents
infile=str(sys.argv[1])
if 'bedgraph' in infile.lower():
    file_out=open(sys.argv[1].replace('.bedgraph', '.wig'), mode='w')
    step=0
    for i in range(len(contents)):
		
		if contents[i][0:5]=='track':
			#print "first line"
			#start_type=re.search(r"[^a-zA-Z](type=)[^a-zA-Z]",contents[i]).start(1)
			start_type=contents[i].find("type=")			
			ss=contents[i][start_type+5:start_type+13]
			#print ss
			file_out.write(contents[0].replace(ss, 'wiggle_0'))
		else:
			line=contents[i].strip().split('\t')
			
			
			chr_first=line[0]
			start=line[1]        
			span=int(line[2]) - int(line[1])
			if i<len(contents)-1:
				next_line=contents[i+1].strip().split('\t')
				step_new=abs(int(next_line[1])-int(start))
			else:
				step_new=1
			if step_new!=step:
				file_out.write('fixedStep'+'\t'+'chrom='+str(chr_first)+'\t'+'start='+str(start)+'\t'+'step='+str(step_new)+'\t'+'span='+str(span)+'\n')
				step=step_new
			file_out.write(str(line[3])+'\n')
            
    file_out.close()            
elif 'wig' in infile.lower():
    file_out=open(sys.argv[1].replace('.wig', '2.bedgraph'), mode='w')
    chrom=''
    start=0
    step=0
    span=0
	
    for i in range(len(contents)):	
		#print contents[i][0:5]	
		if contents[i][0:5]=='track':
			
			file_out.write(contents[0].replace('wiggle_0', 'bedgraph'))
		else:
			#print contents[i]
			line=contents[i].strip().split()
			if line[0]=='fixedStep':
				chrom=line[1][6:]
				start=int(line[2][6:])
				step=int(line[3][5:])
				span=int(line[4][5:])
			elif line[0]=='variableStep':
				chrom=line[1][6:]
				span=int(line[2][5:])
			else:
				if len(line)==1:
					value=float(line[0])
					file_out.write(chrom+'\t'+str(start)+'\t'+str(start+span)+'\t'+str(value)+'\n')
					start=start+step
				else:
					#print line
					start=int(line[0])
					value=float(line[1])
					file_out.write(chrom+'\t'+str(start)+'\t'+str(start+span)+'\t'+str(value)+'\n')
    file_out.close()                
else:
    print "Nieprawidlowy format pliku"
