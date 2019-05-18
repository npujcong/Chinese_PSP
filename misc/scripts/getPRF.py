import sys
import os
import codecs

test_out = sys.argv[1]
test_gt = sys.argv[2]

f_out = codecs.open(test_out, "r", "utf-8")
f_gt = codecs.open(test_gt, "r", "utf-8")

TP = 0 # True Postive, 被判定为正样本，实际上也是正样本
FP = 0 # False Postive, 被判定为正样本，但实际上是负样本
FN = 0 # False Negative, 被判定为负样本，但实际上上是正样本

for line_out, line_gt in zip(f_out.readlines(), f_gt.readlines()):
    if len(line_out.strip().split()) < 2:
        continue
    out = line_out.strip().split()[-1]
    gt = line_gt.strip().split()[-1]

    if out == "B" and gt == "B":
        TP += 1
    elif out == "B" and gt != "B":
        FP += 1
    elif out != "B" and gt == "B":
        FN += 1

precision = round(float(TP) / float(TP+FP), 4)
recall = round(float(TP) / float(TP+FN), 4)
F = round(2 * precision * recall / (precision + recall), 4)

print("Precision\tRecall\tF1")
print(str(precision)+ "\t" + str(recall)+ "\t" + str(F))
