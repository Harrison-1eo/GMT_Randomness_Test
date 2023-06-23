"""
 @description: 15. 离散傅里叶变换检测
 @author: Harrison-1eo
 @date: 2023/6/1
 @version: 1.0
"""
from scipy.fft import fft
import math


def discrete_fourier_transform(bit_stream: str, alpha=0.01, **args):
    n = len(bit_stream)

    X = [1 if bit == '1' else -1 for bit in bit_stream]
    f = fft(X)
    mod = [abs(f[i]) for i in range(n//2)]

    T = math.sqrt(2.995732274 * n)

    n0 = 0.95 * n / 2
    n1 = sum([1 if num < T else 0 for num in mod])

    V = (n1 - n0) / math.sqrt(n * 0.95 * 0.05 / 3.8)

    p_value = math.erfc(abs(V) / math.sqrt(2))
    q_value = math.erfc(V / math.sqrt(2)) / 2

    log = f'离散傅里叶变换检测:\n' \
            f'\t样本长度 n = {n}\n' \
            f'\t统计量 V = {V}\n' \
            f'\tP-value = {p_value}\n' \
            f'\tQ-value = {q_value}\n\n'

    if p_value < alpha:
        return False, p_value, q_value, log
    else:
        return True, p_value, q_value, log


if __name__ == '__main__':
    from randomness.bits2data import e
    print(discrete_fourier_transform(e))