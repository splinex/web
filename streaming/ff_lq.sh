#!/bin/sh
cd $1
rm -rf lq
mkdir  lq
ffmpeg -i hq/1.m3u8 -c:v nvenc -preset:v hp -vf scale=iw/4:ih/4 -hls_time 5 -hls_segment_filename "lq/chunk%03d.ts" -hls_flags delete_segments lq/1.m3u8
