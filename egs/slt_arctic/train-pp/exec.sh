#!/bin/sh

current_working_dir=$(pwd)
cpsp_dir=$(dirname $(dirname $(dirname $current_working_dir)))
crf_dir=$cpsp_dir/tools/CRF++-0.58/build/bin

cp test.data test.gt
awk '{print $1"\t"$2"\t"$3"\t"$4}' test.gt > test.input

$crf_dir/crf_learn -c 0.5 -f 7.0 template train.data pp_model
$crf_dir/crf_test  -m pp_model test.input > test.log
