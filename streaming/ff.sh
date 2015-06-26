#!/bin/sh
work_dir=/var/www/krpano/live
playlist=/var/www/krpano/m3u8/mq/1.m3u8
rm -rf $work_dir
mkdir $work_dir
cd $work_dir
ffmpeg -i $playlist -c:v copy -hls_time 30 -hls_segment_filename "chunk%03d.ts" -hls_flags delete_segments 1.m3u8
