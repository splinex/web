#!/usr/bin/python3
import os, time
import subprocess
from subprocess import call
from os.path import basename
from os.path import dirname
from os.path import  splitext

timeout = 1
playlist_filename = "m3u8/1_hq.m3u8"
dir_path = dirname(playlist_filename)
    
last_modified = 0 
currentFileId = -1
file_list = ['', '', '', '', '']
current_shift = 0

path_to_watch = "m3u8/"
chunk_extenstions = ['ts'] ;
before = [fn for fn in os.listdir(path_to_watch) if any([fn.endswith(ext) for ext in chunk_extenstions])];
mtime = {}

def tsToMp4(inputfile):
    print ("process " + inputfile)
    dir_path = dirname(playlist_filename)
    file_name = splitext(inputfile)[0]
    input_path = os.path.join(dir_path, inputfile)
    out_path = os.path.join(dir_path, file_name + ".mp4")
    call(["ffmpeg", "-y", "-i", input_path, "-strict", "-2", "-vcodec", "copy", out_path])
    
def parsePlaylist( playlist ):  
    with open(playlist, 'r') as f:    
        for line in f:
            line = line.rstrip()
            if line.endswith('.ts'):
                tsToMp4(line)
    f.close()
        
   

parsePlaylist(playlist_filename)

for f in before:
    fpath = os.path.join(dir_path,f)
    mtime[f]=os.stat(fpath).st_mtime  

while 1:
  time.sleep (10)
  for f in before:
    fpath = os.path.join(dir_path,f)  
    if os.path.isfile(fpath):
        ctime=os.stat(fpath).st_mtime  
        if ctime != mtime[f]:
            tsToMp4(f)
            mtime[f]=ctime
        
  after = [fn for fn in os.listdir(path_to_watch) if any([fn.endswith(ext) for ext in chunk_extenstions])];
  added = [f for f in after if not f in before]
  
  for f in added:
    fpath = os.path.join(dir_path,f)
    if os.path.isfile(fpath):
        mtime[f]=os.stat(fpath).st_mtime
        tsToMp4(f)
            
  removed = [f for f in before if not f in after]
  for f in removed:
    fpath = os.path.join(dir_path,f) + ".mp4"
    if os.path.isfile(fpath):
        call(["rm", fpath])   

  before = after

