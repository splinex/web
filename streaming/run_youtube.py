#!/usr/bin/python
import subprocess as sp
from glob import iglob
from subprocess import call
from pprint import pprint
import sys, getopt
import shutil
import json
import os
import time

def concat(chunks, outfile, dirpath):
    destination = open(outfile, 'wb')
    for filename in chunks:
        shutil.copyfileobj(open(dirpath+filename, 'rb'), destination)
    destination.close()
    
def main(argv):
   print "ARGV: " , argv
   help_string = 'run.py  -i <inputfile> -d <path>'
   inputfile = ''
   dirpath = ''
   quality = 1
   try:
      opts, args = getopt.getopt(argv,"hi:d:", ["--input-file","--dir"])
   except getopt.GetoptError:
      print help_string
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print help_string
         sys.exit(2)
      elif opt in ("-i", "--input-file"):
         inputfile = arg
      elif opt in ("-d", "--dir"):
         dirpath = arg
   if(inputfile==''):
      print help_string
      sys.exit(2)
   dirpath=os.getcwd() + "/" + dirpath         
   inputfile=dirpath + inputfile

   try:
       with open(inputfile) as data_file:    
          data = json.load(data_file)
          
       if(len(data["filelist"]) == 0):    
          sys.exit(1) 
           
       outputfile=dirpath + data["uid"] + ".ts" 
       data["filepath"] = outputfile + "_youtube.mp4"
       result_file=dirpath + data["uid"] + ".txt"
       data["result_file"] = result_file
       pprint(data)
       with open(inputfile, 'w') as outfile:
          json.dump(data, outfile) 
       
       concat(data["filelist"], outputfile, dirpath)
       if('quality' in data):
           quality = data['quality']
       
       start = time.time()
       call(["./Allie", "-i", outputfile, "-o", outputfile + ".mp4", "-q", str(quality) , "-p", data["profile"], "-s", result_file ])
       call(["./cutaudio.sh", outputfile, outputfile + ".mp4", outputfile + "_audio.mp4"]) 
       call(["./360VideosMetadata.py", "-i",  outputfile + "_audio.mp4", outputfile + "_youtube.mp4"])
       end = time.time()
       print "Processing time: ", end - start
       
       start = time.time()
       call(["./youtubeworker", "--data-file", inputfile])
       end = time.time()
       print "Youtube upload time: " , end - start
       sys.exit(0)   	
   except sp.CalledProcessError as e:
       print "Error code: " + e.returncode, e 
       sys.exit(e.returncode)       
      	
if __name__ == "__main__":
   main(sys.argv[1:])

