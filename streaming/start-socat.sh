#!/bin/sh
while :;  do socat -d -d tcp-l:$1,reuseaddr tcp-l:$2,reuseaddr; echo 123; sleep 1; done 
