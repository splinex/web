#!/usr/bin/python3
from _sha1 import sha1
import os, time
import subprocess
from subprocess import call
from os.path import basename
from os.path import dirname
from os.path import splitext

timeout = 1
call("mkdir mq",shell=True)
call("mkdir lq",shell=True)
playlist_filename = "hq/1.m3u8"
dir_path = dirname(playlist_filename)
    

def tsToMp4(inputfile):
    print ("process " + inputfile)
    dir_path = dirname(playlist_filename)
    file_name = splitext(inputfile)[0]
    input_path = os.path.join(dir_path, inputfile)
    out_path_mp4 = os.path.join(dir_path, file_name + ".mp4")
    out_path_mq = os.path.join(dir_path, os.path.join("../mq", file_name + ".ts"))
    out_path_lq = os.path.join(dir_path, os.path.join("../lq", file_name + ".ts"))
    callstr = "ffmpeg -y -i " + input_path  \
             + " -c:v copy " + out_path_mp4       \
              + " -c:v nvenc -preset:v hp -vf scale=iw/2:ih/2 -copyts -copytb 0 " + out_path_mq    \
              + " -c:v nvenc -preset:v hp -vf scale=iw/4:ih/4 -copyts -copytb 0 " + out_path_lq
    call(callstr, shell=True)
    
def parsePlaylist( playlist ):  
    with open(playlist, 'r') as f:    
        for line in f:
            line = line.rstrip()
            if line.endswith('.ts'):
                tsToMp4(line)
    f.close()
    
    
# parsePlaylist (playlist_filename)   
call("cp " + playlist_filename + " mq/",shell=True)
call("cp " + playlist_filename + " lq/",shell=True)