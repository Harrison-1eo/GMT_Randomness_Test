"""
 @description: 11. 累加和检测。
 @author: Harrison-1eo
 @date: 2023/5/22
 @version: 1.0
"""
import math
from scipy.stats import norm


def cumulative(bit_stream: str, alpha=0.01, **args):
    mode = 'forward'
    n = len(bit_stream)
    
    bit_stream = [1 if i == '1' else -1 for i in bit_stream]
    
    s = [0] * n
    if mode == 'forward':
        for i in range(n):
            s[i] = abs(sum(bit_stream[:i]))
    elif mode == 'backward':
        for i in range(n):
            s[i] = abs(sum(bit_stream[n-i:]))
    else:
        raise ValueError('mode must be "forward" or "backward"')
        
    z = max(s)
    
    sum1 = 0
    for i in range(int((-n/z+1)/4), int((n/z-1)/4)+1):
        phi1 = norm.cdf(((4*i+1)*z)/math.sqrt(n))
        phi2 = norm.cdf(((4*i-1)*z)/math.sqrt(n))
        sum1 += phi1 - phi2
        
    sum2 = 0
    for i in range(int((-n/z-3)/4), int((n/z-1)/4)+1):
        phi1 = norm.cdf(((4*i+3)*z)/math.sqrt(n))
        phi2 = norm.cdf(((4*i+1)*z)/math.sqrt(n))
        sum2 += phi1 - phi2
    
    p_value = 1 - sum1 + sum2
    q_value = p_value

    log = f'累加和检测：\n' \
            f'\t输入比特串长度：{n}\n' \
            f'\t最大累加和：{z}\n' \
            f'\tP-value：{p_value}\n' \
            f'\tQ-value：{q_value}\n\n'

    if p_value < alpha:
        return False, p_value, q_value, log
    else:
        return True, p_value, q_value, log
    

if __name__ == '__main__':
    e = '11001001000011111101101010100010001000010110100011' \
        '00001000110100110001001100011001100010100010111000'
        
    print(cumulative(e, 100, "backward"))

    
    
    
    
    
