"""
 @project: ApproximateEntropy.py
 @description: 12. 近似熵检测。近似熵检测通过比较 m 位可重叠子序列模式的频数和 m+1位可重叠子序列模式的频数来评价其随机性。
                   对任意一个m来说,随机序列的近似应该近似等于ln2。
 @author: Harrison-1eo
 @date: 2023-05-23
 @version: 1.0
"""
import math
from scipy.special import gammaincc as igamc


def count_subsequences(bits, m):
    """
    Counts the frequency of all subsequences of length m in the binary string bits.
    """
    counts = {}
    for i in range(len(bits) - m + 1):
        subseq = bits[i:i+m]
        if subseq in counts:
            counts[subseq] += 1
        else:
            counts[subseq] = 1
    return counts


def approximate_entropypoker(bit_stream: str, alpha=0.01, **args):
    m = args['m']

    bits = bit_stream + bit_stream[:m - 1]
    
    counts_m = count_subsequences(bits, m)
    for key in counts_m:
        counts_m[key] /= len(bit_stream)
        
    phi_m = 0
    for key in counts_m:
        phi_m += counts_m[key] * math.log(counts_m[key])
    
    bits = bit_stream + bit_stream[:m]
    
    counts_m1 = count_subsequences(bits, m + 1)
    for key in counts_m1:
        counts_m1[key] /= len(bit_stream)
        
    phi_m1 = 0
    for key in counts_m1:
        phi_m1 += counts_m1[key] * math.log(counts_m1[key])
        
    apen = phi_m - phi_m1
    v = 2 * len(bit_stream) * (math.log(2) - apen)
    
    p_value = igamc(2 ** (m - 1), v / 2)
    q_value = p_value

    log = f'近似熵检测:\n' \
        f'\tphi_m = {phi_m}\n' \
        f'\tphi_m1 = {phi_m1}\n' \
        f'\tapen = {apen}\n' \
        f'\tv = {v}\n' \
        f'\tp_value = {p_value}\n' \
        f'\tq_value = {q_value}\n\n'

    if p_value < alpha:
        return False, p_value, q_value, log
    else:
        return True, p_value, q_value, log
    
    
if __name__ == '__main__':
    e = '11001001000011111101101010100010001000010110100011' \
        '00001000110100110001001100011001100010100010111000'
        
    print(approximate_entropypoker(e, m=2))
    
    
        