#!/bin/sh
setup_dir=`pwd`
workdir=/var/www/work_gpu/IC360
scripts_workdir=/var/www/work_gpu/web

cd  $workdir/ &&  git pull && git submodule update
cd  $workdir/build && make -j8
cp debug/Editor360 $setup_dir

cd $scripts_workdir && git pull
cd $setup_dir

cp $scripts_workdir/streaming/watch.py ./
