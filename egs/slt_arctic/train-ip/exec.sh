#!/bin/sh

cp test.data test.gt
awk '{print $1"\t"$2"\t"$3"\t"$4"\t"$5}' test.gt > test.input

# /home/work_nfs/wshge/workspace/CRF++-0.58/bins/crf_learn -c 0.5 -f 7.0 template train.data ip_model
/home/work_nfs/wshge/workspace/CRF++-0.58/bins/crf_test -m ip_model test.input > test.log

#/home/disk1/liuyang/workspace/software/crf++/bin/crf_learn -a MIRA template train.data model >train2.log
#/home/disk1/liuyang/workspace/software/crf++/bin/crf_test  -m model test.data > test2.log
#rm -f model
