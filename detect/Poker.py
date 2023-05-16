"""
 @description: 3.扑克检测。用来检测长度为m的2^m类子序列的个数是否相近。
                 对于随机的序列，2^m类子序列的个数应该接近。
 @author: Harrison-1eo
 @date: 2023/5/9
 @version: 1.0
"""

import numpy as np
from scipy.special import gammaincc as igamc


def poker(bit_stream: str, m, alpha=0.01):
    """
    @description: 扑克检测
    @param bit_stream: 比特流
    @param alpha: 显著性水平
    @return: 扑克检测结果
    """
    n = len(bit_stream)
    N = n // m

    # 统计每个子序列出现的次数
    count = {}
    for i in range(N):
        sub = bit_stream[i * m: i * m + m]
        if sub in count:
            count[sub] += 1
        else:
            count[sub] = 1

    # 计算统计量
    V = 0
    for key in count:
        V += count[key] ** 2

    V *= 2 ** m / N
    V -= N

    # 计算p值和q值
    p_value = igamc((2 ** m - 1) / 2, V / 2)
    q_value = p_value

    if p_value < alpha:
        return False, p_value, q_value
    else:
        return True, p_value, q_value


if __name__ == '__main__':
    e = '11001100000101010110110001001100111000000000001001001101010100010001001111010110100000001101011111001100111001101101100010110010'
    print(poker(e, 4))