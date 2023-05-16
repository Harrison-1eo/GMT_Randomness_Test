"""
 @description: 6.游程分布检测方法。游程分布检测用于检测序列中相同长度的游程分布是否均匀。
                 在随机序列中，相同长度的游程数目应该接近一致，且游程长度每增加一比特，其数目应该减半。
 @author: Harrison-1eo
 @date: 2023/5/9
 @version: 1.0
"""
from math import sqrt
from scipy.special import gammaincc as igamc


def _separate_runs(bit_stream: str) -> list:
    """
    @description: 分离游程
    @param bit_stream: 比特流
    @return: 游程列表
    """
    runs = []
    current_run = ''

    # 将输入字符串拆分成游程
    for bit in bit_stream:
        if current_run == '':
            current_run = bit
        elif current_run[-1] == bit:
            current_run += bit
        else:
            runs.append(current_run)
            current_run = bit
    runs.append(current_run)
    return runs


def _statistic_runs(runs: list, mode: int, k):
    """
    @description: 统计游程长度
    @param runs: 游程列表
    @mode: 0: 0游程，1: 1游程
    @return:
    """
    run_lengths = [len(run) for run in runs if run[0] == str(mode)]

    run_length_counts = {}
    run_length_bigger_k = 0
    for length in run_lengths:
        if length > k:
            length = k

        if length in run_length_counts:
            run_length_counts[length] += 1
        else:
            run_length_counts[length] = 1

    for i in range(k + 1):
        if i not in run_length_counts:
            run_length_counts[i] = 0

    return run_length_counts


def runs_distribution(bit_stream: str, alpha=0.01):
    """
    @description: 游程分布检测
    @param bit_stream: 比特流
    @param alpha: 显著性水平
    @return: 游程分布检测结果
    """
    n = len(bit_stream)

    max_i = -1
    for i in range(1, n + 1):
        ei = (n - i + 3) / (2 ** (i + 2))
        if ei >= 5:
            max_i = i

    if max_i == -1:
        raise ValueError("输入比特流长度过短，无法进行游程分布检测")
    k = max_i

    runs = _separate_runs(bit_stream)

    # 统计游程长度分布
    bi = _statistic_runs(runs, 0, k)
    gi = _statistic_runs(runs, 1, k)

    T = 0
    for i in range(1, k + 1):
        T += bi[i] + gi[i]

    ei = [0 for _ in range(k + 1)]
    for i in range(1, k):
        ei[i] = T / (2 ** (i + 1))
    ei[k] = T / (2 ** k)

    V = 0
    for i in range(1, k + 1):
        V += ((bi[i] - ei[i]) ** 2 + (gi[i] - ei[i]) ** 2) / ei[i]

    p_value = igamc(k - 1, V / 2)
    q_value = p_value

    if p_value < alpha:
        return False, p_value, q_value
    else:
        return True, p_value, q_value


if __name__ == '__main__':
    e = '1100110000010101011011000100110011100000000000100100110101010001'\
        '0001001111010110100000001101011111001100111001101101100010110010'

    print(runs_distribution(e))




