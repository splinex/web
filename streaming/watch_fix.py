#!/usr/bin/python3
import sys, getopt
from _sha1 import sha1
import os, time
import subprocess
from subprocess import call
from os.path import basename
from os.path import dirname
from os.path import exists
from os.path import splitext

def tsToMp4(inputfile, dir_path, override=True):
    print ("process " + inputfile)
    file_name = splitext(inputfile)[0]
    input_path = os.path.join(dir_path, inputfile)
    out_path_mp4 = os.path.join(dir_path, file_name + ".mp4")
    if(exists(out_path_mp4)  and override == False):
        return
    callstr = "ffmpeg -loglevel quiet -y -i " + input_path  \
              + " -c:v copy " + out_path_mp4       
    call(callstr, shell=True)
    
    
def parsePlaylist( playlist ):  
    dir_path = dirname(playlist)
    with open(playlist, 'r') as f:    
        for line in f:
            line = line.rstrip()
            if line.endswith('.ts'):
                tsToMp4(line, dir_path, True)
    f.close()
    
def makeScreenshot(input_path):
    callstr = "ffmpeg -y -i " + input_path  \
              + " -ss 0 -vframes 1 -vcodec mjpeg -f image2 -loglevel quiet " + input_path + ".jpg"
    call(callstr, shell=True)

def start_watch(playlist_filename):
    updateScreenshotInterval = 10
    timeout = 1   
    last_modified = 0 
    last_time = 0
    currentFileId = -1
    chunk_extenstions = ['ts']
    mtime = {}

    dir_path = dirname(playlist_filename)
    playlist_basename = basename(playlist_filename)

    parsePlaylist(playlist_filename)

    before = [fn for fn in os.listdir(dir_path) if any([fn.endswith(ext) for ext in chunk_extenstions])];
    for f in before:
        fpath = os.path.join(dir_path,f)
        mtime[f]=os.stat(fpath).st_mtime  

    while 1:
      time.sleep(timeout)
      for f in before:
        fpath = os.path.join(dir_path,f)  
        if os.path.isfile(fpath):
            ctime=os.stat(fpath).st_mtime  
            if ctime != mtime[f]:
                tsToMp4(f, dir_path)
                mtime[f]=ctime
        
      after = [fn for fn in os.listdir(dir_path) if any([fn.endswith(ext) for ext in chunk_extenstions])];
      added = [f for f in after if not f in before]
      added.sort()
      for f in added:
        fpath = os.path.join(dir_path,f)
        if os.path.isfile(fpath):
            mtime[f]=os.stat(fpath).st_mtime
            tsToMp4(f, dir_path)
            
      removed = [f for f in before if not f in after]
      for f in removed:
        fpath_mp4_hq = os.path.join(dir_path,os.path.splitext(f)[0]) + ".mp4"
        if os.path.isfile(fpath):
            call(["rm", fpath_mp4_hq])  
            
      
      current_time = time.time()
      if current_time - last_time > updateScreenshotInterval:
        print("makeScreenshot: " + str(current_time))
        makeScreenshot(playlist_filename)
        last_time = current_time

      before = after
  
  
def main(argv):
   inputfile = ''
   outputfile = ''
   help='watch.py -i <playlist_file>'
   try:
      opts, args = getopt.getopt(argv,"hi:",["ifile="])
   except getopt.GetoptError:
      print (help)
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print (help)
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
         
   if(inputfile==''):
      print (help)    
      sys.exit(2)
      
   start_watch(inputfile)   
           
         
if __name__ == "__main__":
   main(sys.argv[1:]) 
