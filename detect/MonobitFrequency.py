"""
 @description: 1. 单比特频数检测。检测比特流中0和1的频数是否相近。
                  对于随机序列来说，0和1的频数应该接近相等。
 @author: Harrison-1eo
 @date: 2023/5/9
 @version: 1.0
"""

import numpy as np
from math import erfc


def monobit_frequency(bit_stream: str, alpha=0.01, **args):
    """
    @description: 单比特频数检测
    @param bit_stream: 比特流
    @param alpha: 显著性水平
    @return: 单比特频数检测结果
    """

    S = 0
    for bit in bit_stream:
        if bit == '0':
            S -= 1
        else:
            S += 1

    V = S / np.sqrt(len(bit_stream))

    p_value = erfc(abs(V) / np.sqrt(2))
    q_value = erfc(V / np.sqrt(2)) * 0.5

    log = f'单比特频数检测：\n' \
            f'  比特流长度：{len(bit_stream)}\n' \
            f'  比特流中1的个数：{bit_stream.count("1")}\n' \
            f'  比特流中0的个数：{bit_stream.count("0")}\n' \
            f'  S：{S}\n' \
            f'  V：{V}\n' \
            f'  p_value：{p_value}\n' \
            f'  q_value：{q_value}\n\n'


    if p_value < alpha:
        return False, p_value, q_value, log
    else:
        return True, p_value, q_value, log


if __name__ == '__main__':
    e = '11001100000101010110110001001100111000000000001001001101010100010001001111010110100000001101011111001100111001101101100010110010'
    print(monobit_frequency(e))