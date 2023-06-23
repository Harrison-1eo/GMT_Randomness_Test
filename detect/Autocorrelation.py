"""
 @description: 9. 自相关检测。自相关检测用来检测待检序列与将其左移(逻辑左移)d位后所得新序列的关联程度。
                  一个随机序列应该和将其左移任意位所得的新序列都是独立的，故其关联程度也应该很低，
                  即初始序列与将其左移d位后所得新序列进行异或操作形成的新序列中，0、1的个数应该接近一致。
 @author: Harrison-1eo
 @date: 2023/5/22
 @version: 1.0
"""
from math import sqrt, erfc


def autocorrelation(bit_stream: str, alpha=0.01, **args):
    d = args['d']

    n = len(bit_stream)
    n_d = n - d

    bit_stream = [int(i) for i in bit_stream]

    ad = 0
    for i in range(n_d):
        ad += bit_stream[i] ^ bit_stream[i + d]

    V = 2 * (ad - n_d / 2) / sqrt(n_d)

    p_value = erfc(abs(V) / sqrt(2))
    q_value = erfc(V / sqrt(2)) / 2

    log = f'自相关检测：\n' \
          f'\tad：{ad}\n' \
          f'\t自相关统计量：{V}\n' \
          f'\tP-value：{p_value}\n'\
          f'\tQ-value：{q_value}\n\n'

    if p_value < alpha:
        return False, p_value, q_value, log
    else:
        return True, p_value, q_value, log


if __name__ == '__main__':
    e = '1100110000010101011011000100110011100000000000100100110101010001' \
        '0001001111010110100000001101011111001100111001101101100010110010'

    print(autocorrelation(e, d=1))
