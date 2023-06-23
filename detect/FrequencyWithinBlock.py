"""
 @description: 2.块内频数检测。用与检测序列的m位子序列中1的个数是否接近m/2。
                对于随机序列来说，其任意长度的m位子序列中1的个数都应该接近m/2。
 @author: Harrison-1eo
 @date: 2023/5/9
 @version: 1.0
"""

import numpy as np
from scipy.special import gammaincc as igamc


def frequency_within_a_block(bit_stream: str, alpha=0.01, **args):
    """
    @description: 块内频数检测
    @param bit_stream: 比特流
    @param m: 块大小
    @param alpha: 显著性水平
    @return: 块内频数检测结果
    """
    m = args['m']

    n = len(bit_stream)
    N = n // m

    pi = np.zeros(N)
    for i in range(N):
        for j in range(m):
            if bit_stream[i * m + j] == '1':
                pi[i] += 1
        pi[i] /= m

    V = 0
    for i in range(N):
        V += (pi[i] - 0.5) ** 2

    V *= 4 * m
    p_value = igamc(N / 2, V / 2)
    q_value = p_value

    log = f'块内频数检测：\n' \
            f'\t块大小：{m}\n' \
            f'\t比特流长度：{n}\n' \
            f'\t块数：{N}\n' \
            f'\tV：{V}\n' \
            f'\tp_value：{p_value}\n' \
            f'\tq_value：{q_value}\n\n'

    if p_value < alpha:
        return False, p_value, q_value, log
    else:
        return True, p_value, q_value, log


if __name__ == '__main__':
    e = '1100100100001111110110101010001000100001011010001100001000110100110001001100011001100010100010111000'
    print(frequency_within_a_block(e, 10))
