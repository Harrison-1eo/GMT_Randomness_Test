"""
 @project: MaurerUniversal.py
 @description: 14. Maurer 通用统计检测。Maurer 通用统计检测用于检测待检序列能否被无损压缩。
                   因为随机序列是不能被显著压缩,因此如果待检序列能被显著地压缩,则认为该序列不随机。
 @author: Harrison-1eo
 @date: 2023-05-23
 @version: 1.0
"""

import math
expected_value = [0,            0.73264948, 1.5374383, 2.40160681,
                  3.31122472,   4.25342659, 5.2177052, 6.1962507,
                  7.1836656,    8.1764248,  9.1723243, 10.170032,
                  11.168765,    12.168070,  13.167693, 14.167488,
                  15.167379]

variance = [0,      0.690, 1.338, 1.901, 2.358, 2.705, 2.954, 3.125,
            3.238,  3.311, 3.356, 3.384, 3.401, 3.410, 3.416, 3.419,
            3.421]


def maurer_universal(bit_stream: str, alpha=0.01, **args):
    L = args['L']
    Q = args['Q']

    n = len(bit_stream)

    if n < L * Q:
        raise ValueError("输入序列长度不足以进行检测")
    K = n // L - Q

    T = [0] * (2 ** L)
    Q_list = [int(bit_stream[i * L:(i + 1) * L], 2) for i in range(Q)]
    K_list = [int(bit_stream[(Q + i) * L:(Q + i + 1) * L], 2) for i in range(K)]
    for num in range(Q):
        # 找出Q_list中最后出现num的位置
        for i in range(Q - 1, -1, -1):
            if Q_list[i] == num:
                T[num] = i + 1
                break

    rel_len = []
    for index, num in enumerate(K_list):
        if T[num] != 0:
            rel_len.append(Q + index + 1 - T[num])
        T[num] = Q + index + 1

    fn = sum([math.log2(l) for l in rel_len]) / K
    c = 0.7 - 0.8 / L + (4 + 32 / L) * (K ** (-3 / L)) / 15
    sigma = c * math.sqrt(variance[L] / K)

    V = (fn - expected_value[L]) / sigma
    p_value = math.erfc(abs(V) / math.sqrt(2))
    q_value = math.erfc(V / math.sqrt(2)) / 2

    log = f'通用统计检测：\n' \
            f'\t输入序列长度：{n}\n' \
            f'\t分组长度：{L}\n' \
            f'\t分组数：{Q}\n' \
            f'\t期望值：{expected_value[L]}\n' \
            f'\t方差：{variance[L]}\n' \
            f'\t统计量：{V}\n' \
            f'\tP-value：{p_value}\n' \
            f'\tQ-value：{q_value}\n\n'


    if p_value < alpha:
        return False, p_value, q_value, log
    else:
        return True, p_value, q_value, log


if __name__ == '__main__':
    from randomness.bits2data import e

    print(maurer_universal(e))
