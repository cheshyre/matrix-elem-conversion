# Copyright (c) 2023 Matthias Heinz
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

f1 = "ornl_magic_nn_roth_flat_sorted.txt"
f2 = "da_magic_nn_roth_flat_sorted.txt"

def get_key(line):
    return tuple([int(x) for x in line.strip().split()[:7]])

def get_val(line):
    return float(line.strip().split()[7])

with open(f2) as f:
    da_vals = {get_key(line): get_val(line) for line in f}

with open(f1) as f:
    ornl_vals = {get_key(line): get_val(line) for line in f}

diffs = [ornl_vals[x] - da_vals[x] for x in ornl_vals]
abs_diffs = [abs(x) for x in diffs]

with open("big_diffs.txt", "w") as f:
    for i, x in enumerate(ornl_vals):
        if abs_diffs[i] > 1e-1:
            f.write("{} {} {}\n".format(x, da_vals[x], ornl_vals[x]))

max_diff = max(abs_diffs)
avg_diff = sum(abs_diffs) / len(abs_diffs)

print(max_diff)
print(avg_diff)