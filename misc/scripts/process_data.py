#!/usr/bin/env python
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
# Author sdjngws (gewenshuo)
# Modified by npujcong@gmail.com(congjian)
# Date 2019/05/17 23:44:34
#
######################################################################

import codecs
import os
import sys

punc_list = ["?","!",".","。","！","？",",","，","\"",":","：",";","；","“","”","<",">","《","》","'","[","]","(",")","-","——","‘","’","_","（","）"]

def getBIO(line1,lines2,fout):
    # 我们@预计@下半年@四大@周期@支撑@经济@L型#韧性@仍强
    line_tmp = line1
    for i in range(len(punc_list)):
        line_tmp = line_tmp.replace(punc_list[i],"")
    tokens = line_tmp.split("@")
    tmp = ""
    cnt = 0
    flag = 1
    for i in range(len(lines2)):
        if len(lines2[i].strip().split()) < 2:
            fout.write("\n")
            flag = 1
            continue
        if lines2[i].strip().split()[0] in punc_list:
            fout.write(lines2[i]+"\tO\n")
            flag = 1
            tmp = ""
            continue
        tmp += lines2[i].strip().split()[0]
        if tmp == tokens[cnt]:
            if flag == 0:
                fout.write(lines2[i]+"\tI\n")
                flag = 1
            elif flag == 1:
                fout.write(lines2[i]+"\tB\n")
            tmp = ""
            cnt += 1
        else:
            if flag == 1:
                fout.write(lines2[i]+"\tB\n")
                flag = 0
            elif flag == 0:
                fout.write(lines2[i]+"\tI\n")

def getpw(line1,lines2,fout):
    line1 = line1.replace("#1","@")
    line1 = line1.replace("#2","@")
    line1 = line1.replace("#3","@")
    getBIO(line1,lines2,fout)

def getpp(line1,lines2,fout):
    line1 = line1.replace("#1","")
    line1 = line1.replace("#2","@")
    line1 = line1.replace("#3","@")
    getBIO(line1,lines2,fout)

def getip(line1,lines2,fout):
    line1 = line1.replace("#1","")
    line1 = line1.replace("#2","")
    line1 = line1.replace("#3","@")
    getBIO(line1,lines2,fout)

def get_prev_rhyBIO(fin1,fin2,fout):
    lines1 = fin1.readlines()
    lines2 = fin2.readlines()
    assert len(lines1) == len(lines2)
    for i in range(len(lines1)):
        list1 = lines1[i].split('\t')
        if len(list1) < 2:
            fout.write(lines1[i])
            continue
        list2 = lines2[i].strip().split('\t')
        fout.write(list1[0]+'\t'+list1[1]+'\t'+list1[2]+'\t'+list2[3]+'\t'+list1[3])

def get_prev_rhyBIOs(fin1,fin2,fin3,fout):
    lines1 = fin1.readlines()
    lines2 = fin2.readlines()
    lines3 = fin3.readlines()
    assert len(lines1) == len(lines2) == len(lines3)
    for i in range(len(lines1)):
        list1 = lines1[i].split('\t')
        if len(list1) < 2:
            fout.write(lines1[i])
            continue
        list2 = lines2[i].strip().split('\t')
        list3 = lines3[i].strip().split('\t')
        fout.write(list1[0]+'\t'+list1[1]+'\t'+list1[2]+'\t'+list2[3]+'\t'+list3[3]+'\t'+list1[3])


def main(fn1, fn2, out_dir):
    fin1 = codecs.open(fn1,"r","utf-8")
    in_lines1 = [line.strip() for line in fin1.readlines()]
    fin2 = codecs.open(fn2,"r","utf-8")
    in_lines2 = []
    tmp = []
    for line in fin2.readlines():
        if len(line.strip().split()) > 2:
            tmp.append(line.strip())
        else:
            tmp.append(line)
            in_lines2.append(tmp)
            tmp = []
    if len(tmp) > 0:
        in_lines2.append(tmp)
    assert len(in_lines1)==len(in_lines2)

    fout1 = codecs.open(os.path.join(out_dir,"pw.utf8"), "w", "utf-8")
    fout2 = codecs.open(os.path.join(out_dir,"pp.utf8"), "w", "utf-8")
    fout3 = codecs.open(os.path.join(out_dir,"ip.utf8"), "w", "utf-8")
    for i in range(len(in_lines1)):
        getpw(in_lines1[i],in_lines2[i],fout1)
        getpp(in_lines1[i],in_lines2[i],fout2)
        getip(in_lines1[i],in_lines2[i],fout3)
    fout1.close()
    fout2.close()
    fout3.close()

    fin1 = codecs.open(os.path.join(out_dir, "pw.utf8"), "r", "utf-8")
    fin2 = codecs.open(os.path.join(out_dir, "pp.utf8"), "r", "utf-8")
    fin3 = codecs.open(os.path.join(out_dir, "ip.utf8"), "r", "utf-8")
    fout1 = codecs.open(os.path.join(out_dir, "pp-final.utf8"), "w", "utf-8")
    fout2 = codecs.open(os.path.join(out_dir, "ip-final.utf8"), "w", "utf-8")

    get_prev_rhyBIO(fin2,fin1,fout1)
    fin1.seek(0)
    fin2.seek(0)
    get_prev_rhyBIOs(fin3,fin1,fin2,fout2)
    fout1.close()
    fout2.close()

if __name__ == '__main__':
    fn1 = sys.argv[1] # sentence_roboo.utf8
    fn2 = sys.argv[2] # data_roboo.utf8
    out_dir=sys.argv[3] # out_put_dir
    main(fn1,fn2,out_dir)
