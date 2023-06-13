# Copyright (c) 2023 Matthias Heinz
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from sys import argv


def nlj_vals(emax: int):
    nlj_vals_list = []
    for e in range(emax + 1):
        for l in range(e % 2, e + 1, 2):
            n = (e - l) // 2
            if l != 0:
                jjvals = [2 * l - 1, 2 * l + 1]
            else:
                jjvals = [2 * l + 1]
            for jj in jjvals:
                nlj_vals_list.append((n, l, jj))
                
    return nlj_vals_list


def me2j_modelspace(emax: int):
    nlj = nlj_vals(emax)
    
    modelspace = {}
    index_counter = 0
    for i, nlj1 in enumerate(nlj):
        for j, nlj2 in enumerate(nlj[:i + 1]):
            for k, nlj3 in enumerate(nlj[:i + 1]):
                max_l = k
                if k == i:
                    max_l = j
                for l, nlj4 in enumerate(nlj[:max_l + 1]):
                    # Parity check
                    if (nlj1[1] + nlj2[1]) % 2 != (nlj3[1] + nlj4[1]) % 2:
                        continue
                    
                    min_jj = max(abs(nlj1[2] - nlj2[2]), abs(nlj3[2] - nlj4[2]))
                    max_jj = min(nlj1[2] + nlj2[2], nlj3[2] + nlj4[2])
                    
                    for jj in range(min_jj, max_jj + 1, 2):
                        # T=0 np channel
                        modelspace[(i, j, k, l, jj, 0, 0)] = index_counter
                        # nn channel
                        modelspace[(i, j, k, l, jj, 2, 2)] = index_counter + 1
                        # T=2 np channel
                        modelspace[(i, j, k, l, jj, 2, 0)] = index_counter + 2
                        # pp channel
                        modelspace[(i, j, k, l, jj, 2, -2)] = index_counter + 3
                        index_counter += 4
                        
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

num_mes = len(me2j_modelspace(emax))

num_mes_printed = 0
with open(fin) as f:
    for i, line in enumerate(f):
        if num_mes - num_mes_printed >= 10:
            print(line.rstrip())
            if i != 0:
                num_mes_printed += 10
        elif num_mes > num_mes_printed:
            rest_count = num_mes - num_mes_printed
            line_nums = [float(x) for x in line.strip().split()[:rest_count]]
            final_line = "".join(["{:>14.8f}".format(x) for x in line_nums])
            print(final_line)
            num_mes_printed += len(line_nums)
        else:
            break

