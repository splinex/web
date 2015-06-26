#!/bin/sh
cd $1
rm -rf mq
mkdir  mq
ffmpeg -i hq/1.m3u8 -b 2000000 -c:v nvenc -preset:v hp -vf scale=iw/2:ih/2 -hls_time 5 -hls_segment_filename "mq/chunk%03d.ts" -hls_flags delete_segments mq/1.m3u8
