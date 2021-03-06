#-----------------------------------------------------------+
#                                                           |
# template.py - Python template                             |
#                                                           |
#-----------------------------------------------------------+
#                                                           |
# AUTHOR: Vikas Gupta                                        |
# CONTACT: vikas0633@gmail.com                              |
# STARTED: 09/06/2013                                       |
# UPDATED: 09/06/2013                                       |
#                                                           |
# DESCRIPTION:                                              | 
# Short script to convert and copy the wheat BACs           |
# Run this in the parent dir that the HEX* dirs exist       |
#                                                           |
# LICENSE:                                                  |
#  GNU General Public License, Version 3                    |
#  http://www.gnu.org/licenses/gpl.html                     |  
#                                                           |
#-----------------------------------------------------------+

# Example:
# python ~/script/python/100b_fasta2flat.py -i 02_Stegodyphous_cdna.refined.fa.orf.tr_longest_frame

### import modules
import os,sys,getopt, re

import threading

from multiprocessing import Process, Queue, Manager
from threading import Thread
import classGene
### global variables
global infile

### make a logfile
import datetime
now = datetime.datetime.now()
o = open(str(now.strftime("%Y-%m-%d_%H%M."))+'logfile','w')


def get_size(file):
    size = {}
    for line in open(file,'r'):
        line = line.strip()
        if len(line) > 0:
            if line[0] != '#':
                token = line.split('\t')
                
                if token[0] not in size:
                    size[token[0]] = int(token[4])
                    
                else:
                    if int(token[4]) > size[token[0]]:
                        size[token[0]] = int(token[4])
    size_sorted={}
    for w in sorted(size, key=size.get, reverse=False):
        size_sorted[w]=size[w]
    return size_sorted


### write logfile

def logfile(infile):
    o.write("Program used: \t\t%s" % "100b_fasta2flat.py"+'\n')
    o.write("Program was run at: \t%s" % str(now.strftime("%Y-%m-%d_%H%M"))+'\n')
    o.write("Infile used: \t\t%s" % infile+'\n')
            
    
def help():
    print '''
            python 100b_fasta2flat.py -i <infile>
            '''
    sys.exit(2)

def temp(file):
    num_lines = sum(1 for line in open(file))
    return num_lines

### main argument to 

def options(argv):
    global infile, threads
    infile = ''
    threads = 2
    
    try:
        opts, args = getopt.getopt(argv,"hi:t:",["infile=","threads="])
    except getopt.GetoptError:
        help()
    for opt, arg in opts:
        if opt == '-h':
            help()
        elif opt in ("-i", "--infile"):
            infile = arg
        elif opt in ("-t", "--threads"):
            threads = int(arg)
            
    
    logfile(infile)
            
def count_genes():
    count_contig = 1
    count_same_contig = 0
    count_different_contig = 0
    count_replace = 0
    count_replaced = 0
    new_contig = True
    first_line = True
    gene = {}
    for line in open(infile,'r'):
        line  = line.strip()
        token = line.split('\t')
        contig_1 = "g".join(token[1].split('g')[:-1])
        contig_2 = "g".join(token[2].split('g')[:-1])
        if len(token)>3:
            gene[token[2]] = ''
            if first_line == False:
                if last_contig_1 == contig_1:
                    count_contig += 1
                    if last_contig_2 == contig_2:
                        count_same_contig += 1
                        if token[3] != 'No_Hit':
                            if 1 < int(token[3]) <= 10:
                                count_replace += 1
                            if int(token[3]) == 1:
                                count_replaced += 1
                    else:
                        count_different_contig += 1
                    
            
            last_contig_1 = contig_1
            last_contig_2 = contig_2
            first_line = False

    print "Total number of contigs proccessed: \t"+ str(count_contig)
    print "Total number of genes in matching contigs: \t" +  str(count_same_contig)
    print "Total number of genes with bestreciprocal blast hit = 1: \t" + str(count_replaced)
    print "Total number of genes with reciprocal hit 1< and <10: \t"+ str(count_replace)
    print "Total number of genes present in different proginator contigs: \t " + str(count_different_contig)

if __name__ == "__main__":
    

    options(sys.argv[1:])
    
    start_time = datetime.datetime.now()
    print >> sys.stderr, "Running temp script: " + str(datetime.datetime.now())
    print >> sys.stderr, "Input count: " + str(temp(infile))
    
    
    count_genes()
    
    print >> sys.stderr, "Output count: " + str(temp(infile))
    print >> sys.stderr, "Completed temp script: " + str(datetime.datetime.now())
    print >> sys.stderr, "Time take to complete: " + str(datetime.datetime.now() - start_time)

    