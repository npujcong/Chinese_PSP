import os
import codecs
import argparse

def getTrainAndTest(fid, trainid, testid, test_ratio):
    fin = codecs.open(fid,"r","utf-8")
    fout1 = codecs.open(trainid,"w","utf-8")
    fout2 = codecs.open(testid,"w","utf-8")
    test_ckpt = int(1 / test_ratio)
    cnt = 0
    for line in fin.readlines():
        if len(line.split()) < 2:
    	    cnt += 1
        if cnt % test_ckpt == 0:
            fout2.write(line)
        else:
    	    fout1.write(line)
    print(fid+" cnt:"+str(cnt))
    fout1.close()
    fout2.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", default="pw_final.utf8")
    parser.add_argument("--out_dir", default="train-pw")
    parser.add_argument("--test_ratio", type=float, default=0.1)
    args = parser.parse_args()
    train_file = os.path.join(args.out_dir, "train.data")
    test_file = os.path.join(args.out_dir, "test.data")
    getTrainAndTest(args.input_file, train_file, test_file, args.test_ratio)
