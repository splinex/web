
#!/bin/sh
in=tcp://127.0.0.1:1033
out_dir=/var/www/krpano/test/m3u8*
out=/var/www/krpano/test/m3u8/1.m3u8
rm -rf  $out_dir/*
screen ./Editor360 -i $in -o $out -r 10 -l 30 -q 1 -u 5 -o
