#!/bin/sh
# Copyright 2016 ASLP@NPU.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: npujcong@gmail.com (congjian)

prefix=unisound
current_working_dir=$(pwd)
cpsp_dir=$(dirname $(dirname $current_working_dir))

crf_dir=$cpsp_dir/tools/CRF++-0.58/build/bin
thulac_dir=$cpsp_dir/tools/THULAC/
model_dir=$cpsp_dir/models

# word segment
$thulac_dir/build/thulac \
  -seg_only \
  -model_dir $thulac_dir/models \
  -input raw/$prefix-raw.utf8 \
  -output data/$prefix-seg.utf8

# pos tag
$crf_dir/crf_test -m $model_dir/aslp-pos-model data/$prefix-seg.utf8 > data/$prefix-pos.utf8
mv data/$prefix-pos.utf8 data/$prefix-pos.utf8.bk
awk '{print $1"\t"$3"\t"$2}' data/$prefix-pos.utf8.bk > data/$prefix-pos.utf8

# get data (pw, pp, ip)
python $cpsp_dir/misc/scripts/process_data.py \
    raw/$prefix-rhy.utf8 \
    data/$prefix-pos.utf8 \
    data
cp data/pw.utf8 data/pw-final.utf8

# split test and train set
for item in pw pp ip
do
    python $cpsp_dir/misc/scripts/split_train_test.py \
        --input_file=data/$item-final.utf8 \
        --out_dir=train-$item \
        --test_ratio=0.1
done
