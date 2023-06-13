from typing import List, Tuple, Dict
from functools import lru_cache
import datetime
from sys import argv


# Quantum numbers are nlj1, nlj2, nlj3, nlj4, J, t1, t2, t3, t4
ME2JNPIndex = Tuple[int, int, int, int, int, int, int, int, int]

# Quantum numbers are nljt1, nljt2, nljt3, nljt4, J
ME2JPIndex = Tuple[int, int, int, int, int]


@lru_cache()
def nlj_vals(emax: int) -> List[Tuple[int, int, int]]:
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
                for t in [0, 1]:
                    nljt_vals_list.append((n, l, jj, t))
                
    return nljt_vals_list


@lru_cache()
def me2j_np_modelspace(emax: int) -> Dict[ME2JNPIndex, int]:
    nlj = nlj_vals(emax)
    
    t_n = 0
    t_p = 1
    
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


def convert_me2j_np_index_to_me2jp_index(mej2_np_index: ME2JNPIndex, jjvals: Tuple[int, int, int, int], hermiticity: int = 1) -> Tuple[ME2JPIndex, int]:
    nlj1, nlj2, nlj3, nlj4, jj, t1, t2, t3, t4 = mej2_np_index
    nljt1 = 2 * nlj1 + t1
    nljt2 = 2 * nlj2 + t2
    nljt3 = 2 * nlj3 + t3
    nljt4 = 2 * nlj4 + t4
    
    j1, j2, j3, j4 = jjvals
    
    mel_phase = 1
    
    # Use antisymmetry (+1 is antisymmetry, j3 + j4 + jj is CG symmetry)
    if nljt3 < nljt4:
        nljt3, nljt4 = nljt4, nljt3
        mel_phase *= (-1) ** (((j3 + j4 + jj) // 2) + 1)
    
    if nljt1 < nljt2:
        nljt1, nljt2 = nljt2, nljt1
        mel_phase *= (-1) ** (((j1 + j2 + jj) // 2) + 1)
        
    # Use anti-Hermiticity
    if nljt1 < nljt3 or (nljt1 == nljt3 and nljt2 < nljt4):
        nljt1, nljt2, nljt3, nljt4 = nljt3, nljt4, nljt1, nljt2
        mel_phase *= hermiticity
        
    return (nljt1, nljt2, nljt3, nljt4, jj), mel_phase


@lru_cache()
def create_me2j_np_to_me2jp_mapping(emax: int, hermiticity: int = 1) -> Dict[int, Tuple[int, int]]:
    me2jnp = me2j_np_modelspace(emax)
    me2jp = me2jp_modelspace(emax)
    
    nlj = nlj_vals(emax)
    
    output_mapping = {}
    for x in me2jnp:
        nlj1, nlj2, nlj3, nlj4, _, _, _, _, _ = x
        x_i = me2jnp[x]
        
        jjvals = (nlj[nlj1][2], nlj[nlj2][2], nlj[nlj3][2], nlj[nlj4][2])
        y, phase = convert_me2j_np_index_to_me2jp_index(x, jjvals)
        y_i = me2jp[y]
        
        output_mapping[x_i] = (y_i, phase)
        
    return output_mapping


def convert_me2j_np_to_me2jp(emax: int, mels: List[float], hermiticity: int = 1) -> List[float]:
    np_to_p_map = create_me2j_np_to_me2jp_mapping(emax, hermiticity)
    
    output_dim = len(me2jp_modelspace(emax))
    
    output_mels = [0.0] * output_dim
    
    for i, x in enumerate(mels):
        j, phase = np_to_p_map[i]
        output_mels[j] = phase * x
    
    return output_mels


def convert_me2jp_to_me2j_np(emax: int, mels: List[float], hermiticity: int = 1) -> List[float]:
    np_to_p_map = create_me2j_np_to_me2jp_mapping(emax, hermiticity)
    
    output_dim = len(me2j_np_modelspace(emax))
    
    output_mels = [0.0] * output_dim
    
    for i, _ in enumerate(output_mels):
        j, phase = np_to_p_map[i]
        output_mels[i] = phase * mels[j]
    
    return output_mels


def write_file(filename: str, mels: List[float]):
    date_str = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
    ext = filename.split(".")[-1]
    if ext == "me2jp":
        format_spec = "me2jp-f2"
    elif ext == "me2j_np":
        format_spec = "me2j_np-f1"
    else:
        print(f"Unsupported extension: {format_spec}")
        exit()
    
    with open(filename, "w") as f:
        f.write(f"generated by me2j_np <-> me2jp conversion code on {date_str} - {format_spec}\n")
        for i in range(0, len(mels), 10):
            if i + 10 <= len(mels):
                f.write(" ".join([f"{x:12.8f}" for x in mels[i:i + 10]]) + "\n")
            else:
                f.write(" ".join([f"{x:12.8f}" for x in mels[i:]]) + "\n")


def read_file(filename: str) -> List[float]:
    mels = []
    with open(filename) as f:
        for i, line in enumerate(f):
            if i != 0:
                mels += [float(x) for x in line.strip().split()]
                
    return mels
        

if len(argv) != 3:
    print("Usage:")
    print("\tpython3 me2j_np_to_me2jp.py [emax] [filename]")
    exit()

myemax = int(argv[1])
myfilename = argv[2]

mels = read_file(myfilename)

ext = myfilename.split(".")[-1]
rest_filename  = ".".join(myfilename.split(".")[:-1])
if ext == "gz":
    print("gzipped files not yet supported.")
    exit()

if ext == "me2j_np":
    outmels = convert_me2j_np_to_me2jp(myemax, mels)
    out_filename = rest_filename + ".me2jp"
    write_file(out_filename, outmels)
elif ext == "me2jp":
    outmels = convert_me2jp_to_me2j_np(myemax, mels)
    out_filename = rest_filename + ".me2j_np"
    write_file(out_filename, outmels)
    
    
# print(convert_me2j_np_index_to_me2jp_index(
#     (0, 1, 1, 0, 2, 0, 0, 0, 0), (1, 1, 1, 1)
# ))



# print(nlj_vals(2))
# print(len(nlj_vals(2)))
# print(len(nljt_vals(2)))
# print(len(me2j_np_modelspace(2)))
# print(len(me2j_np_modelspace(4)))
# print(len(me2j_np_modelspace(6)))
# print(len(me2jp_modelspace(2)))
# print(len(me2jp_modelspace(4)))
# print(len(me2jp_modelspace(6)))
                        
# nlj = nlj_vals(2)
# counts_dict = {}
# for x in me2j_np_modelspace(2):
#     nlj1, nlj2, nlj3, nlj4, _, _, _, _, _ = x
#     jjvals = (nlj[nlj1][2], nlj[nlj2][2], nlj[nlj3][2], nlj[nlj4][2])
#     y, phase = convert_me2j_np_index_to_me2jp_index(x, jjvals)
#     outindex = me2jp_modelspace(2)[y]
#     if y in counts_dict:
#         counts_dict[y] += 1
#     else:
#         counts_dict[y] = 1

# for x in counts_dict:
#     if counts_dict[x] > 1:
#         pass
#         # print("overcounted")
#         # print(x)
#         # print(counts_dict[x])
        