
#!/bin/sh
in=udp://127.0.0.1:1034
out_dir=/var/www/krpano/m3u8
out=/var/www/krpano/m3u8/1.m3u8
rm -rf  $out_dir/*
screen -L ./Editor360 -i $in -o $out -l 5 -q 0 -p 3516
