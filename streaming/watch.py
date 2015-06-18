#!/usr/bin/python3
import sys, getopt
from _sha1 import sha1
import os, time
import subprocess
from subprocess import call
from os.path import basename
from os.path import dirname
from os.path import splitext

def tsToMp4(inputfile, dir_path):
    print ("process " + inputfile)
    file_name = splitext(inputfile)[0]
    input_path = os.path.join(dir_path, inputfile)
    out_path_mp4 = os.path.join(dir_path, file_name + ".mp4")
    out_path_mq = os.path.join(dir_path, os.path.join("mq", file_name + ".ts"))
    out_path_lq = os.path.join(dir_path, os.path.join("lq", file_name + ".ts"))
    callstr = "ffmpeg -y -i " + input_path  \
              + " -c:v copy " + out_path_mp4       \
              + " -c:v nvenc -preset:v hp -vf scale=iw/2:ih/2 " + out_path_mq    \
              + " -c:v nvenc -preset:v hp -vf scale=iw/4:ih/4 " + out_path_lq
    call(callstr, shell=True)
    
def parsePlaylist( playlist ):  
    dir_path = dirname(playlist)
    with open(playlist, 'r') as f:    
        for line in f:
            line = line.rstrip()
            if line.endswith('.ts'):
                tsToMp4(line, dir_path)
    f.close()

def start_watch(playlist_filename):
    timeout = 1    
    last_modified = 0 
    currentFileId = -1
    chunk_extenstions = ['ts'] ;

    dir_path = dirname(playlist_filename)
    before = [fn for fn in os.listdir(dir_path) if any([fn.endswith(ext) for ext in chunk_extenstions])];
    mtime = {}
    
    lq_dir_path = os.path.join(dir_path,"lq")
    mq_dir_path = os.path.join(dir_path,"mq")
    call(["mkdir ",lq_dir_path])
    call(["mkdir ",mq_dir_path])

    parsePlaylist(playlist_filename)

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
  
      for f in added:
        fpath = os.path.join(dir_path,f)
        if os.path.isfile(fpath):
            mtime[f]=os.stat(fpath).st_mtime
            tsToMp4(f, dir_path)
            
      removed = [f for f in before if not f in after]
      for f in removed:
        fpath = os.path.join(dir_path,os.path.splitext(f)[0]) + ".mp4"
        if os.path.isfile(fpath):
            call(["rm", fpath])   
            
      call(["cp" , playlist_filename, lq_dir_path])
      call(["cp" , playlist_filename, mq_dir_path])

      before = after
  
  
def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:",["ifile="])
   except getopt.GetoptError:
      print 'watch.py -i <playlist_file>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'watch.py -i <playlist_file>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
         
   start_watch(inputfile)      
         
if __name__ == "__main__":
   main(sys.argv[1:]) 
