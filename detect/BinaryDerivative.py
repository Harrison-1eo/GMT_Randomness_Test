"""
 @description: 8. 二元推导检测。二元推导检测的目的是判定第k次二元推导序列中0和1的个数是否接近一致。
                  对于一个随机的序列,无论进行多少次推导,其 0、1的个数都应该接近一致。
 @author: Harrison-1eo
 @date: 2023/5/22
 @version: 1.0
"""
import math


def binary_derivative(bit_stream: str, alpha=0.01, **args):
    k = args['k']

    n = len(bit_stream)
    n_k = n - k

    bit_stream = [int(i) for i in bit_stream]

    for i in range(k):
        for j in range(n - 1):
            bit_stream[j] = bit_stream[j] ^ bit_stream[j + 1]

    bit = [1 if bit_stream[i] == 1 else 0 for i in range(n - k)]
    Sn_k = bit.count(1) - bit.count(0)

    V = Sn_k / math.sqrt(n_k)

    p_value = math.erfc(abs(V) / math.sqrt(2))
    q_value = math.erfc(V / math.sqrt(2)) / 2

    log = f'二元推导检测:\n' \
            f'\tSn_k: {Sn_k}\n' \
            f'\tV: {V}\n' \
            f'\tp_value: {p_value}\n' \
            f'\tq_value: {q_value}\n\n'

    if p_value < alpha:
        return False, p_value, q_value, log
    else:
        return True, p_value, q_value, log


if __name__ == '__main__':
    e = '1100110000010101011011000100110011100000000000100100110101010001' \
        '0001001111010110100000001101011111001100111001101101100010110010'

    print(binary_derivative(e, k=3))
