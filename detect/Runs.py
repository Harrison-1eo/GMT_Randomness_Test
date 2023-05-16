"""
 @description: 5.游程总数检测方法。游程是指序列中连续出现的0或1的最长子序列。
                 游程总数检测主要检测序列中游程的总数是否符合随机性要求。
 @author: Harrison-1eo
 @date: 2023/5/9
 @version: 1.0
"""
from math import sqrt
from scipy.special import erfc


def runs(bit_stream: str, alpha=0.01):
    """
    @description: 游程总数检测
    @param bit_stream: 比特流
    @param alpha: 显著性水平
    @return: 游程总数检测结果
    """
    n = len(bit_stream)
    Vn = 0
    for i in range(n - 1):
        if bit_stream[i] == bit_stream[i + 1]:
            Vn += 0
        else:
            Vn += 1
    Vn += 1

    sum = 0
    for i in range(n):
        if bit_stream[i] == '1':
            sum += 1
    pi = sum / n

    V = (Vn - 2 * n * pi * (1 - pi)) / (2 * sqrt(n) * pi * (1 - pi))
    p_value = erfc(abs(V) / sqrt(2))
    q_value = erfc(V / sqrt(2)) / 2

    if p_value < alpha:
        return False, p_value, q_value
    else:
        return True, p_value, q_value


if __name__ == '__main__':
    e = '1100110000010101011011000100110011100000000000100100110101010001'\
        '0001001111010110100000001101011111001100111001101101100010110010'
    print(runs(e))
