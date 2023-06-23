"""
 @description: 7. 块内最大1游程检测方法。块内最大1游程是指序列中连续出现的1的最长子序列。
                  将待检测序列分成n/m个块，统计每个块内最大1游程的长度，计算统计量V。
 @author: Harrison-1eo
 @date: 2023/6/23
 @version: 1.2
"""
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


MPI8     = [(1, 0.2148),    (2, 0.3672),    (3, 0.2305),    (4, 0.1875)]
MPI128   = [(4, 0.1174),    (5, 0.2430),    (6, 0.2493),    (7, 0.1752),    (8, 0.1027),    (9, 0.1124)]
MPI10000 = [(10, 0.0882),   (11, 0.2092),   (12, 0.2483),   (13, 0.1933),   (14, 0.1208),   (15, 0.0675),   (16, 0.0727)]
MPIs     = {8:MPI8, 128:MPI128, 10000:MPI10000}
Ks       = {8:3, 128:5, 10000:6}
K_starts = {8:1, 128:4, 10000:10}


def longest_run_of_ones(bit_stream: str, alpha=0.01, **args):
    """
    @description: 块内最大1游程检测
    @param bit_stream: 比特流
    @param m: 块大小
    @param alpha: 显著性水平
    @return: 检测结果
    """
    m = args['m']

    if m not in MPIs.keys():
        raise ValueError('m must be 8, 128 or 10000')

    n = len(bit_stream)
    N = n // m

    # 分块
    blocks = [bit_stream[i * m: i * m + m] for i in range(N)]

    # 统计每个块内最大0游程和1游程的长度
    # max_0run_length = [max([len(run) for run in _separate_runs(block) if run[0] == '0']) for block in blocks]
    max_1run_length = [max([len(run) for run in _separate_runs(block) if run[0] == '1']) for block in blocks]

    K = Ks[m]
    K_start = K_starts[m]
    MPI = MPIs[m]

    K_list = [0] * (K + 1)
    for length in max_1run_length:
        if K_start <= length <= K_start + K:
            K_list[length - K_start] += 1
        elif length > K_start + K:
            K_list[K] += 1
        else:
            K_list[0] += 1

    # 计算统计量V
    V = sum([(K_list[i] - N * MPI[i][1]) ** 2 / (N * MPI[i][1]) for i in range(K + 1)])

    # 计算P-value
    p_value = igamc(K / 2, V / 2)
    q_value = p_value

    log = f'块内最大1游程检测方法：\n' \
            f'\t块大小：{m}\n' \
            f'\t块数：{N}\n' \
            f'\t统计量V：{V}\n' \
            f'\tP-value：{p_value}\n' \
            f'\tQ-value：{q_value}\n\n'

    if p_value < alpha:
        return False, p_value, q_value, log
    else:
        return True, p_value, q_value, log


if __name__ == '__main__':
    e = '1100110000010101011011000100110011100000000000100100110101010001' \
        '0001001111010110100000001101011111001100111001101101100010110010'
    print(longest_run_of_ones(e, m=8))

