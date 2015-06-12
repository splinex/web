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

def restoreOriginalConfigs():
    for i in range(1,6):
    	call(["cp", "original_configs/v" + str(i) + ".xml", "v" + str(i) + ".xml"])  
    
     
def shiftConfigs():
    print ("shiftConfigs")
    for i in range(0,5):
        next = (i + 1)%5
        config="v" + str(i + 1) + ".xml"
        tmp_config=str(next + 1) + "_new.xml"
        call(["mv", config, tmp_config])  
    for i in range(1,6):
    	tmp_config=str(i) + "_new.xml"
    	config="v" + str(i) + ".xml"
    	call(["mv", tmp_config, config])   
        
def tsToMp4(inputfile):
    currentFile = inputfile
    global currentFileId
    global current_shift
    fileId = currentFileId
    if inputfile in file_list : 
        fileId = file_list.index(inputfile)
    else:
        currentFileId=(currentFileId+1)%5
        file_list[currentFileId] = inputfile 
        fileId = currentFileId
        current_shift+=1
        if current_shift > 4: shiftConfigs()
        
    print ('process ', inputfile, " ", fileId)
    file_name = splitext(inputfile)[0]
    input_path = os.path.join(dir_path, inputfile)
    out_path_tmp = os.path.join(dir_path, str(fileId+1) + "_tmp.mp4")
    out_path = os.path.join(dir_path, str(fileId+1) + ".mp4")
    call(["ffmpeg", "-y", "-i", input_path, "-strict", "-2", "-vf", "hflip,vflip,format=yuv420p", "-metadata:s:v" ,"rotate=0", "-codec:v", "nvenc", out_path_tmp])

#     call(["ffmpeg", "-y", "-i", input_path, "-map", "0:0", "-strict", "-2", "-vcodec", "copy", out_path_tmp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    call(["mv", out_path_tmp, out_path])

    
def parsePlaylist( playlist ):  
    with open(playlist, 'r') as f:    
        for line in f:
            line = line.rstrip()
            if line.endswith('.ts'):
                tsToMp4(line)
    f.close()

restoreOriginalConfigs()
parsePlaylist(playlist_filename)

for f in before:
    fpath = os.path.join(dir_path,f)
    mtime[f]=os.stat(fpath).st_mtime  

while 1:
  time.sleep (10)
  for f in before:
    fpath = os.path.join(dir_path,f)  
    ctime=os.stat(fpath).st_mtime  
    if ctime != mtime[f]:
        tsToMp4(f)
        mtime[f]=ctime
        
  after = [fn for fn in os.listdir(path_to_watch) if any([fn.endswith(ext) for ext in chunk_extenstions])];
  
  for f in after:
    if not f in before:
        fpath = os.path.join(dir_path,f)
        mtime[f]=os.stat(fpath).st_mtime  
        tsToMp4(f)

  before = after

