
#!/bin/sh
in=tcp://127.0.0.1:1035
out_dir=/var/www/krpano/m3u8
out=/var/www/krpano/m3u8/1.m3u8
rm -rf  $out_dir/*
screen ./Editor360 -i $in -o $out -l 5 -q 0 -p RedBeam -b 6000000
