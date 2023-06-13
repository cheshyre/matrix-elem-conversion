from typing import List, Tuple, Dict
from functools import lru_cache
import datetime
from sys import argv


# Quantum numbers are nljt1, nljt2, nljt3, nljt4, J
ME2JPIndex = Tuple[int, int, int, int, int]


@lru_cache()
def nljt_vals(emax: int) -> List[Tuple[int, int, int, int]]:
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

    
@lru_cache()
def me2jp_modelspace(emax: int) -> Dict[ME2JPIndex, int]:
    nljt = nljt_vals(emax)
    
    modelspace = {}
    index_counter = 0
    for i, nljt1 in enumerate(nljt):
        for j, nljt2 in enumerate(nljt[:i + 1]):
            for k, nljt3 in enumerate(nljt[:i + 1]):
                max_l = k
                if k == i:
                    max_l = j
                for l, nljt4 in enumerate(nljt[:max_l + 1]):
                    # Parity check
                    if (nljt1[1] + nljt2[1]) % 2 != (nljt3[1] + nljt4[1]) % 2:
                        continue
                    
                    # Isospin check
                    if nljt1[3] + nljt2[3] != nljt3[3] + nljt4[3]:
                        continue
                    
                    min_jj = max(abs(nljt1[2] - nljt2[2]), abs(nljt3[2] - nljt4[2]))
                    max_jj = min(nljt1[2] + nljt2[2], nljt3[2] + nljt4[2])
                    for jj in range(min_jj, max_jj + 1, 2):
                        modelspace[(i, j, k, l, jj)] = index_counter
                        index_counter += 1
                        
    return modelspace

        
def print_usage_and_exit(code):
    print(f"Usage: {__file__} [file] [emax]")
    exit(code)


if len(argv) != 3 or (len(argv) == 2  and argv[1].lower() in ["-h", "--help", "help"]):
    print_usage_and_exit(-1)

fin = argv[1]
try: 
    emax = int(argv[2])
except ValueError:
    print("Could not parse value for emax from {}. Exiting.".format(argv[1]))
    print_usage_and_exit(-1)


me2jp_ms = me2jp_modelspace(emax)
me2jp_me = [0.0] * len(me2jp_ms)
header = ""
read_counter = 0

with open(fin) as f:
    for i, line in enumerate(f):
        if i == 0:
            header = line.strip()
        else:
            line_mes = [float(x) for x in line.strip().split()]
            for x in line_mes:
                me2jp_me[read_counter] = x
                read_counter += 1

# print(read_counter)
# print(len(me2jp_ms))

def is_in_coupling_range(jja, jjb, jjab):
    return (jjab >= abs(jja - jjb) and jjab <= jja + jjb)


def get_me(a, b, c, d, jj, nljts, me2jp_ms, me2jp_me):
    phase = 1
    if b > a:
        jja = nljts[a][2]
        jjb = nljts[b][2]
        phase *= (-1) ** (((jja + jjb + jj) // 2) + 1)
        temp = a
        a = b
        b = temp
    if d > c:
        jjc = nljts[c][2]
        jjd = nljts[d][2]
        phase *= (-1) ** (((jjc + jjd + jj) // 2) + 1)
        temp = c
        c = d
        d = temp
    if c > a or (c == a and (d > b)):
        temp = (c, d)
        c, d = (a, b)
        a, b = temp

    return phase * me2jp_me[me2jp_ms[(a, b, c, d, jj)]]


nljts = nljt_vals(emax)

for tz in [-1, 0, 1]:
    ttz = 2 * tz
    for parity in [0, 1]:
        for j in range(0, 2 * emax + 2, 1):
            jj = 2 * j
            for a, qn_a in enumerate(nljts):
                for b, qn_b in enumerate(nljts):
                    if qn_a[3] + qn_b[3] != ttz:
                        continue
                    if (qn_a[1] + qn_b[1]) % 2 != parity:
                        continue
                    if not is_in_coupling_range(qn_a[2], qn_b[2], jj):
                        continue
                    for c, qn_c in enumerate(nljts):
                        for d, qn_d in enumerate(nljts):
                            if qn_c[3] + qn_d[3] != ttz:
                                continue
                            if (qn_c[1] + qn_d[1]) % 2 != parity:
                                continue
                            if not is_in_coupling_range(qn_c[2], qn_d[2], jj):
                                continue
                            print("{:>3d} {:>3d} {:>3d} {:>3d} {:>3d} {:>3d} {:>3d} {:>22.10f} {:>22.10f}".format(
                                j, parity, tz, a, b, c, d,
                                get_me(a, b, c, d, jj, nljts, me2jp_ms, me2jp_me)
                                , 0.0
                            ))



