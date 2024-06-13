# Copyright (c) 2023 Matthias Heinz
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

f1 = "me3jp_index_new.txt"
# f2 = "me3jp_e2_E4.txt"
f2 = "jimsrg_e2_E4.txt"

with open(f1) as fin:
    data_1 = [[int(x) for x in line.strip().split()] for line in fin]

with open(f2) as fin:
    data_2 = [[int(x) for x in line.strip().split()] for line in fin]

for i, row in enumerate(data_1):
    for j, val in enumerate(row):
        if data_2[i][j] != val:
            print("Difference at i = {}, j = {}".format(i, j))
