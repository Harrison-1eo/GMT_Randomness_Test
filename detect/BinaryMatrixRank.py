"""
 @description: 10. 矩阵秩检测法。用来检测待检序列中给定长度的子序列之间的线性独立性。
                   由待检序列构造矩阵,然后检测矩阵的行或列之间的线性独立性,矩阵秩的偏移程度可以给出关于线性独立性的量的认识,从而影响对二元序列随机性好坏的评价。
 @author: Harrison-1eo
 @date: 2023/5/22
 @version: 1.0
"""
from scipy.special import gammaincc as igamc
import numpy as np


def matrix_rank_f2(matrix):
    """
    高斯消元法，在F2域上求矩阵的秩
    """

    num_rows, num_cols = matrix.shape

    rank = 0
    for i in range(num_rows):
        # 在当前行 i 中查找第一个非零元素
        j = np.argmax(matrix[i, :])
        if matrix[i, j] == 0:
            continue

        # 将当前行 i 和第一行交换
        matrix[[i, rank], :] = matrix[[rank, i], :]

        # 使用行变换消除其他行中的当前列元素
        for k in range(num_rows):
            if k != rank and matrix[k, j] != 0:
                matrix[k, :] = (matrix[k, :] + matrix[rank, :]) % 2

        rank += 1

    return rank


def binary_matrix_rank(bit_stream: str, alpha=0.01, **args):
    """
    矩阵秩检测法
    :param bit_stream: 待检测序列
    :param alpha: 显著性水平
    :return: 检测结果
    """
    n = len(bit_stream)
    matrix_num = int(n / (32 * 32))

    print('matrix_num:', matrix_num)

    if matrix_num == 0:
        raise ValueError("输入序列长度不足，无法构造矩阵")

    # 构造矩阵
    F_m = 0
    F_m_1 = 0
    for i in range(matrix_num):
        X = np.zeros((32, 32), dtype=int)
        for j in range(32):
            for k in range(32):
                X[j][k] = int(bit_stream[i * 32 * 32 + j * 32 + k])

        rank = matrix_rank_f2(X)

        if rank == 32:
            F_m += 1
        elif rank == 31:
            F_m_1 += 1

    print('F_m:', F_m)
    print('F_m_1:', F_m_1)

    V = 0
    V += (F_m - 0.2888 * matrix_num) ** 2 / (0.2888 * matrix_num)
    V += (F_m_1 - 0.5776 * matrix_num) ** 2 / (0.5776 * matrix_num)
    V += ((matrix_num - F_m - F_m_1) - 0.1336 * matrix_num) ** 2 / (0.1336 * matrix_num)

    p_value = igamc(1, V / 2)
    q_value = p_value

    log = f'矩阵秩检测法：\n' \
            f'\t输入序列长度：{n}\n' \
            f'\t矩阵个数：{matrix_num}\n' \
            f'\tF_m：{F_m}\n' \
            f'\tF_m_1：{F_m_1}\n' \
            f'\tV：{V}\n' \
            f'\tp_value：{p_value}\n' \
            f'\tq_value：{q_value}\n\n'


    if p_value < alpha:
        return False, p_value, q_value, log
    else:
        return True, p_value, q_value, log


if __name__ == '__main__':
    from randomness.bits2data import e
    print(binary_matrix_rank(e))
