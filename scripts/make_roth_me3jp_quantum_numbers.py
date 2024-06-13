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
    print(f"Usage: {__file__} [emax] [E3max]")
    exit(code)


if len(argv) == 2 and argv[1].lower() in ["-h", "--help", "help"]:
    print_usage_and_exit(0)

if len(argv) != 3:
    print_usage_and_exit(1)

emax = int(argv[1])
e3max = int(argv[2])

nljjts = nljt_vals(emax)

fstring = "{:>7} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>4} {:>4} {:>4}"
print("#" + fstring.format("i", "nljt1", "nljt2", "nljt3", "nljt4", "nljt5", "nljt6", "JJ12", "JJ45", "JJ"))
counter = 0
for i1, nljjt1 in enumerate(nljjts):
    n1, l1, jj1, t1 = nljjt1
    e1 = 2 * n1 + l1

    max2 = i1
    max4 = i1

    for i2, nljjt2 in enumerate(nljjts[:max2 + 1]):
        n2, l2, jj2, t2 = nljjt2
        e2 = 2 * n2 + l2

        jj12_min = abs(jj1 - jj2)
        jj12_max = jj1 + jj2

        max3 = i2

        for i3, nljjt3 in enumerate(nljjts[:max3 + 1]):
            n3, l3, jj3, t3 = nljjt3
            e3 = 2 * n3 + l3

            if e1 + e2 + e3 > e3max:
                continue

            for i4, nljjt4 in enumerate(nljjts[:max4 + 1]):
                n4, l4, jj4, t4 = nljjt4
                e4 = 2 * n4 + l4

                max5 = i4
                if i4 == i1:
                    max5 = i2

                for i5, nljjt5 in enumerate(nljjts[:max5 + 1]):
                    n5, l5, jj5, t5 = nljjt5
                    e5 = 2 * n5 + l5

                    jj45_min = abs(jj4 - jj5)
                    jj45_max = jj4 + jj5

                    max6 = i5
                    if i4 == i1 and i5 == i2:
                        max6 = i3

                    for i6, nljjt6 in enumerate(nljjts[:max6 + 1]):
                        n6, l6, jj6, t6 = nljjt6
                        e6 = 2 * n6 + l6

                        # E3max cut
                        if e4 + e5 + e6 > e3max:
                            continue

                        # Parity
                        if (l1 + l2 + l3) % 2 != (l4 + l5 + l6) % 2:
                            continue

                        # Isospin
                        if t1 + t2 + t3 != t4 + t5 + t6:
                            continue

                        for jj12 in range(jj12_min, jj12_max + 1, 2):
                            for jj45 in range(jj45_min, jj45_max + 1, 2):
                                jj_min = max(
                                    abs(jj12 - jj3),
                                    abs(jj45 - jj6)
                                )
                                jj_max = min(
                                    jj12 + jj3,
                                    jj45 + jj6
                                )
                                if jj_max < jj_min:
                                    continue
                                for jj in range(jj_min, jj_max + 1, 2):
                                    # print(" " + fstring.format(
                                    #     counter, i1, i2, i3, i4, i5, i6, jj12, jj45, jj))
                                    counter += 1


print(counter)

