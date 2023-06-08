# Copyright (c) 2023 Matthias Heinz
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from sys import argv


def nljmt_vals(emax: int):
    nljmt_vals_list = []
    for e in range(emax + 1):
        for l in range(e % 2, e + 1, 2):
            n = (e - l) // 2
            if l != 0:
                jjvals = [2 * l - 1, 2 * l + 1]
            else:
                jjvals = [2 * l + 1]
            for jj in jjvals:
                for mm in range(-1 * jj, jj + 1, 2):
                    for t in [1, -1]:
                        nljmt_vals_list.append((n, l, jj, mm, t))
    
    return nljmt_vals_list

def print_usage_and_exit(code):
    print(f"Usage: {__file__} [emax]")
    exit(code)


if len(argv) != 2 or argv[1].lower() in ["-h", "--help", "help"]:
    print_usage_and_exit(-1)

try: 
    emax = int(argv[1])
except ValueError:
    print("Could not parse value for emax from {}. Exiting.".format(argv[1]))
    print_usage_and_exit(-1)

nljmts = nljmt_vals(emax)

fstring = "{:>4} {:>4}"
print("#" + fstring.format("p", "M_p"))
for i, nljmt in enumerate(nljmts):
    n, l, jj, mm, t = nljmt
    print(" " + fstring.format(i, mm))


