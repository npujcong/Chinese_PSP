#!/bin/bash
# -*- coding: utf-8 -*-

######################################################################
#
# Copyright ASLP@NPU. All Rights Reserved
#
# Licensed under the Apache License, Veresion 2.0(the "License");
# You may not use the file except in compliance with the Licese.
# You may obtain a copy of the License at
#
#   http://www.apache.org/license/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author npujcong@gmail.com(congjian)
# Date 2019/05/18 16:41:37
#
######################################################################

# pw->pp-ip

train_pw=train-pw
train_pp=train-pp
train_ip=train-ip

current_working_dir=$(pwd)
cpsp_dir=$(dirname $(dirname $current_working_dir))
crf_dir=$cpsp_dir/tools/CRF++-0.58/build/bin
cascade_dir=cascade-test

[ ! -e $cascade_dir ] && mkdir -p $cascade_dir

# pw test
cp $train_pw/test.input $cascade_dir/pw.input
cp $train_pw/test.gt $cascade_dir/pw.gt
$crf_dir/crf_test -m $train_pw/pw_model \
    $cascade_dir/pw.input > $cascade_dir/pw.output

# pp test
cp $train_pp/test.gt $cascade_dir/pp.gt
$crf_dir/crf_test -m $train_pp/pp_model \
    $cascade_dir/pw.output > $cascade_dir/pp.output

# ip test
cp $train_ip/test.gt $cascade_dir/ip.gt
$crf_dir/crf_test -m $train_ip/ip_model \
    $cascade_dir/pp.output > $cascade_dir/ip.output

# compute prf
echo "*************pw result**************"
python $cpsp_dir/misc/scripts/getPRF.py \
    $cascade_dir/pw.output \
    $cascade_dir/pw.gt

echo "*************pp result**************"
python $cpsp_dir/misc/scripts/getPRF.py \
    $cascade_dir/pp.output \
    $cascade_dir/pp.gt

echo "*************ip result**************"
python $cpsp_dir/misc/scripts/getPRF.py \
    $cascade_dir/ip.output \
    $cascade_dir/ip.gt
