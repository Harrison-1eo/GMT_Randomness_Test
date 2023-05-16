"""
 @description: 4.重叠子序列检测方法。将长度为n的待检测序列划分为n个可叠加的m位子序列。
                 对于随机序列来说，可叠加的m位子序列的每一类模式出现的概率应该接近。
 @author: Harrison-1eo
 @date: 2023/5/9
 @version: 1.0
"""
from scipy.special import gammaincc as igamc


def _statistic_func(bit_stream: str, n, m):
    bit_stream = bit_stream + bit_stream[:m - 1]
    
    if m == 0:
        return 0
    else:
        count = {}
        for i in range(len(bit_stream) - m + 1):
            sub = bit_stream[i: i + m]
            if sub in count:
                count[sub] += 1
            else:
                count[sub] = 1
        V = 0
        for key in count:
            V += count[key] ** 2
    V *= (2 ** m) / n
    V -= n

    return V


def serial(bit_stream: str, m, alpha=0.01):
    """
    @description: 重叠子序列检测方法
    @param bit_stream: 比特流
    @param m: 子序列长度
    @param alpha: 显著性水平
    @return: 重叠子序列检测结果
    """
    n = len(bit_stream)
    
    # 统计m位、m-1位、m-2位子序列出现的次数
    V_m = _statistic_func(bit_stream, n, m)
    V_m_1 = _statistic_func(bit_stream, n, m - 1)
    V_m_2 = _statistic_func(bit_stream, n, m - 2)

    delta_1 = V_m - V_m_1
    delta_2 = V_m - 2 * V_m_1 + V_m_2

    # 计算p值和q值
    p_value_1 = igamc(2 ** (m - 2), delta_1 / 2)
    p_value_2 = igamc(2 ** (m - 3), delta_2 / 2)
    q_value_1 = p_value_1
    q_value_2 = p_value_2

    if p_value_1 < alpha or p_value_2 < alpha:
        return False, p_value_1, p_value_2, q_value_1, q_value_2
    else:
        return True, p_value_1, p_value_2, q_value_1, q_value_2


if __name__ == '__main__':
    e = '1100110000010101011011000100110011100000000000100100110101010001' \
        '0001001111010110100000001101011111001100111001101101100010110010'
    print(serial(e, 2))
