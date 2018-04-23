import sys
import os

def compare(labels, inferred):
    tp = 0
    fp = 0
    fn = 0
    print(labels)
    print(inferred)
    print()
    for y in inferred:
        if y in labels:
            tp += 1
        else:
            fp += 1
    for y in labels:
        if y not in inferred:
            fn += 1
    return tp, fp, fn

true_labels = [x.strip().split(" ") for x in open(sys.argv[1], 'r').readlines()]
inferred_labels = [x.strip().split(" ") for x in open(sys.argv[2], 'r').readlines()]

tp = 0
fp = 0
fn = 0
for y, yp in zip(true_labels, inferred_labels):
    tp_, fp_, fn_ = compare(y, yp)
    tp += tp_
    fp += fp_
    fn += fn_

recall = tp / (tp + fn)
precision = tp / (tp + fp)
f1 = 2 * (precision * recall) / (precision + recall)

print("Precision: {}\nRecall: {}\nF1: {}".format(precision, recall, f1))
