# Copyright (c) 2023 Matthias Heinz
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from sys import argv


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

def print_usage_and_exit(code):
    print(f"Usage: {__file__} [emax]")
    exit(code)


def make_orbital_string(n, l, jj, t) -> str:
    L_TO_LS = {
        0: "s",
        1: "p",
        2: "d",
        3: "f",
        4: "g",
        5: "h",
        6: "i",
    }
    T_TO_TS = {
        -1: "p",
        1: "n",
    }

    if l in L_TO_LS:
        return "{}{}{}{}/2".format(T_TO_TS[t], n, L_TO_LS[l], jj)
    return ""


if len(argv) != 2 or argv[1].lower() in ["-h", "--help", "help"]:
    print_usage_and_exit(-1)

try: 
    emax = int(argv[1])
except ValueError:
    print("Could not parse value for emax from {}. Exiting.".format(argv[1]))
    print_usage_and_exit(-1)

nljjts = nljt_vals(emax)

fstring = "{:>4} {:>4} {:>4} {:>4} {:>4} {:>8}"
print("#" + fstring.format("p", "n_p", "l_p", "jj_p", "tz_p", "orb"))
for i, nljjt in enumerate(nljjts):
    n, l, jj, t = nljjt
    print(" " + fstring.format(i, n, l, jj, t, make_orbital_string(n, l, jj, t)))


