#!/usr/bin/python
import sys, getopt
import os, time
import subprocess
from subprocess import call
import re

IMAGE_WIDTH=2048
IMAGE_HEIGHT=2048

def parseConfig( filename ):  
    with open(filename, 'r') as f:    
        for line in f:
            match = re.search('radius="(\d+\.\d+)".*cx="(\d+.\d+)".*cy="(\d+.\d+)"', line) #width="(\d+).*height="(\d+) radius(.+)\s+cx="(\d+)"\s+cy="(\d+)"\s+phi="(\d+)"
            if match : 
                radius = float(match.group(1)) + 1
                cx = float(match.group(2)) / IMAGE_WIDTH 
                cy = float(match.group(3)) / IMAGE_HEIGHT
                print line
                print '<geometry radius="' + str(radius) + '" cx="' + str(cx)+ '" cy="' + str(cy) + '" phi="-0.0235619"/>'
#                 print (match.group(1) ,  match.group(2),  match.group(3))
    f.close()


def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'fix_absolute_path.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'fix_absolute_path.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
         
   parseConfig(inputfile)      
         
if __name__ == "__main__":
   main(sys.argv[1:])         
         