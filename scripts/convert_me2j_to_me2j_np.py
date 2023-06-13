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


def me2j_np_modelspace(emax: int):
    nlj = nlj_vals(emax)
    
    t_n = 1
    t_p = -1
    
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
                        # npnp
                        modelspace[(i, j, k, l, jj, t_n, t_p, t_n, t_p)] = index_counter
                        # pnpn
                        modelspace[(i, j, k, l, jj, t_p, t_n, t_p, t_n)] = index_counter + 1
                        # nnnn
                        modelspace[(i, j, k, l, jj, t_n, t_n, t_n, t_n)] = index_counter + 2
                        # pnnp
                        modelspace[(i, j, k, l, jj, t_p, t_n, t_n, t_p)] = index_counter + 3
                        # nppn
                        modelspace[(i, j, k, l, jj, t_n, t_p, t_p, t_n)] = index_counter + 4
                        # pppp
                        modelspace[(i, j, k, l, jj, t_p, t_p, t_p, t_p)] = index_counter + 5
                        index_counter += 6
                        
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

me2j_ms = me2j_modelspace(emax)
me2j_np_ms = me2j_np_modelspace(emax)

me2j_me = [0.0] * len(me2j_ms)
header = ""
read_counter = 0

with open(fin) as f:
    for i, line in enumerate(f):
        if i == 0:
            header = line.strip()
        else:
            line_mes = [float(x) for x in line.strip().split()]
            for x in line_mes:
                me2j_me[read_counter] = x
                read_counter += 1

me2j_np_me = [0.0] * len(me2j_np_ms)

for i, j, k, l, jj, t_i, t_j, t_k, t_l in me2j_np_ms:
    if t_i + t_j == 0 and t_i == t_k:
        me = 0.5 * (
            me2j_me[me2j_ms[(i, j, k, l, jj, 2, 0)]]
            + me2j_me[me2j_ms[(i, j, k, l, jj, 0, 0)]]
        )
    elif t_i + t_j == 0 and t_i != t_k:
        me = 0.5 * (
            me2j_me[me2j_ms[(i, j, k, l, jj, 2, 0)]]
            - me2j_me[me2j_ms[(i, j, k, l, jj, 0, 0)]]
        )
    else:
        me = me2j_me[me2j_ms[(i, j, k, l, jj, 2, t_i + t_j)]]
    me2j_np_me[me2j_np_ms[(i, j, k, l, jj, t_i, t_j, t_k, t_l)]] = me

header = header.replace("me2j", "me2j_np")
print(header)
write_counter = 0
target_write_counter = len(me2j_np_ms)
for i in range(0, target_write_counter, 10):
    batch_start = i
    batch_end = min(target_write_counter, i + 10)
    print("".join(["{:>14.8f}".format(x) for x in me2j_np_me[batch_start:batch_end]]))



