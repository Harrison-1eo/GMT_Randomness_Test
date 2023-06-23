"""
 @project: LinearComplexity.py
 @description: 13. 线性复杂度检测。用于检测各等长子序列的线性复杂度分布是否符合随机性的要求
 @author: Harrison-1eo
 @date: 2023-05-23
 @version: 1.0
"""
from scipy.special import gammaincc as igamc


def berelekamp_massey(bits):
    n = len(bits)
    b = [0 for x in bits]  # initialize b and c arrays
    c = [0 for x in bits]
    b[0] = 1
    c[0] = 1

    L = 0
    m = -1
    N = 0
    while (N < n):
        d = int(bits[N])
        for i in range(1, L + 1):
            d = d ^ (c[i] & int(bits[N - i]))
        if (d != 0):
            t = c[:]
            for i in range(0, n - N + m):
                c[N - m + i] = c[N - m + i] ^ b[i]
            if (L <= (N / 2)):
                L = N + 1 - L
                m = N
                b = t
        N = N + 1

    return L, c[0:L]


def classify(T):
    v = [0, 0, 0, 0, 0, 0, 0]
    for t in T:
        if t <= -2.5:
            v[0] += 1
        elif t <= -1.5:
            v[1] += 1
        elif t <= -0.5:
            v[2] += 1
        elif t <= 0.5:
            v[3] += 1
        elif t <= 1.5:
            v[4] += 1
        elif t <= 2.5:
            v[5] += 1
        else:
            v[6] += 1
    return v


def linear_complexity(bit_stream: str, alpha=0.01, **args):
    m = args['m']

    n = len(bit_stream)
    N = n // m
    
    lc = [0 for _ in range(N)]
    for i in range(N):
        lc[i] = berelekamp_massey(bit_stream[i * m:(i + 1) * m])[0]
        
    u = m / 2 + (9 + (-1) ** (m+1)) / 36 - (m / 3 + 2 / 9) / 2 ** m
    t = [0 for _ in range(N)]
    for i in range(N):
        t[i] = (-1) ** m * (lc[i] - u) + 2 / 9
    
    v = classify(t)
    pi = [0.010417, 0.03125, 0.125, 0.5, 0.25, 0.0625, 0.020833]
    V = [(v[i] - N * pi[i]) ** 2 / (N * pi[i]) for i in range(7)]
    
    p_value = igamc(3, sum(V) / 2)
    q_value = p_value

    log = f'线性复杂度检测:\n' \
            f'\t线性复杂度序列: {lc}\n' \
            f'\t统计量: {t}\n' \
            f'\t分类: {v}\n' \
            f'\t期望: {pi}\n' \
            f'\t统计量: {V}\n' \
            f'\tP-value: {p_value}\n' \
            f'\tQ-value: {q_value}\n\n'


    if p_value < alpha:
        return False, p_value, q_value, log
    else:
        return True, p_value, q_value, log
    
    
if __name__ == '__main__':
    e = '11001100000101010110110001001100111000000000001001001101010100010001001111010110100000001101011111001100111001101101100010110010'
    
    print(linear_complexity(e, m=5))
    
    