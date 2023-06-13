# Copyright (c) 2023 Matthias Heinz
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

emax = 6

ornl_states_string = """ 1   0   0   1  -1          24.00000000          0.000000000    
   2   0   0   1   1          24.00000000          0.000000000    
   3   0   1   3  -1          40.00000000          0.000000000    
   4   0   1   3   1          40.00000000          0.000000000    
   5   0   1   1  -1          40.00000000          0.000000000    
   6   0   1   1   1          40.00000000          0.000000000    
   7   0   2   5  -1          56.00000000          0.000000000    
   8   0   2   5   1          56.00000000          0.000000000    
   9   1   0   1  -1          56.00000000          0.000000000    
  10   1   0   1   1          56.00000000          0.000000000    
  11   0   2   3  -1          56.00000000          0.000000000    
  12   0   2   3   1          56.00000000          0.000000000    
  13   0   3   7  -1          72.00000000          0.000000000    
  14   0   3   7   1          72.00000000          0.000000000    
  15   1   1   3  -1          72.00000000          0.000000000    
  16   1   1   3   1          72.00000000          0.000000000    
  17   1   1   1  -1          72.00000000          0.000000000    
  18   1   1   1   1          72.00000000          0.000000000    
  19   0   3   5  -1          72.00000000          0.000000000    
  20   0   3   5   1          72.00000000          0.000000000    
  21   0   4   9  -1          88.00000000          0.000000000    
  22   0   4   9   1          88.00000000          0.000000000    
  23   0   4   7  -1          88.00000000          0.000000000    
  24   0   4   7   1          88.00000000          0.000000000    
  25   1   2   5  -1          88.00000000          0.000000000    
  26   1   2   5   1          88.00000000          0.000000000    
  27   1   2   3  -1          88.00000000          0.000000000    
  28   1   2   3   1          88.00000000          0.000000000    
  29   2   0   1  -1          88.00000000          0.000000000    
  30   2   0   1   1          88.00000000          0.000000000    
  31   0   5  11  -1          104.0000000          0.000000000    
  32   0   5  11   1          104.0000000          0.000000000    
  33   0   5   9  -1          104.0000000          0.000000000    
  34   0   5   9   1          104.0000000          0.000000000    
  35   1   3   7  -1          104.0000000          0.000000000    
  36   1   3   7   1          104.0000000          0.000000000    
  37   1   3   5  -1          104.0000000          0.000000000    
  38   1   3   5   1          104.0000000          0.000000000    
  39   2   1   3  -1          104.0000000          0.000000000    
  40   2   1   3   1          104.0000000          0.000000000    
  41   2   1   1  -1          104.0000000          0.000000000    
  42   2   1   1   1          104.0000000          0.000000000    
  43   0   6  13  -1          120.0000000          0.000000000    
  44   0   6  13   1          120.0000000          0.000000000    
  45   0   6  11  -1          120.0000000          0.000000000    
  46   0   6  11   1          120.0000000          0.000000000    
  47   1   4   9  -1          120.0000000          0.000000000    
  48   1   4   9   1          120.0000000          0.000000000    
  49   1   4   7  -1          120.0000000          0.000000000    
  50   1   4   7   1          120.0000000          0.000000000    
  51   2   2   5  -1          120.0000000          0.000000000    
  52   2   2   5   1          120.0000000          0.000000000    
  53   2   2   3  -1          120.0000000          0.000000000    
  54   2   2   3   1          120.0000000          0.000000000    
  55   3   0   1  -1          120.0000000          0.000000000    
  56   3   0   1   1          120.0000000          0.000000000"""

ornl_states = [tuple([int(x) for x in line.strip().split()[1:5]]) for line in ornl_states_string.split("\n")]
ornl_states_map = {i + 1: x for i, x in enumerate(ornl_states)}


def nljt_vals(emax: int):
    nljt_vals_list = []
    for e in range(emax + 1):
        for l in range(e % 2, e + 1, 2):
            n = (e - l) // 2
            if l != 0:
                jjvals = [2 * l - 1, 2 * l + 1]
            else:
                jjvals = [2 * l + 1]
            for jj in jjvals:
                for t in [1, -1]:
                    nljt_vals_list.append((n, l, jj, t))
                
    return nljt_vals_list

nljts = nljt_vals(emax)

nljts_inv_map = {x: i for i, x, in enumerate(nljts)}

# print(ornl_states_map)
# print(nljts_inv_map)

with open("ornl_to_nljt_map.txt", "w") as fout:
    for x in ornl_states_map:
        fout.write("{:>4d} {:>4d}\n".format(x, nljts_inv_map[ornl_states_map[x]]))

in_file = "vn3loEM_srg18_N06_hw16.dat"
with open(in_file) as f:
    for line in f:
        ints = [int(x) for x in line.strip().split()[:7]]
        floats = [float(x) for x in line.strip().split()[7:]]
        ints[3] = nljts_inv_map[ornl_states_map[ints[3]]]
        ints[4] = nljts_inv_map[ornl_states_map[ints[4]]]
        ints[5] = nljts_inv_map[ornl_states_map[ints[5]]]
        ints[6] = nljts_inv_map[ornl_states_map[ints[6]]]
        print(" ".join(["{:>3d}".format(x) for x in ints]) + " ".join(["{:>22.10f}".format(x) for x in floats]))
