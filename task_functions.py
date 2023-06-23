from detect import *
import json
detect_function = [
    (monobit_frequency, '单比特频数检测'),
    (frequency_within_a_block, '块内频数检测'),
    (poker, '扑克检测'),
    (serial, '重叠子序列检测'),
    (runs, '游程总数检测'),
    (runs_distribution, '游程分布检测'),
    (longest_run_of_ones, '块内最大1游程检测方法'),
    (binary_derivative, '二元推导检测'),
    (autocorrelation, '自相关检测'),
    (binary_matrix_rank, '矩阵秩检测法'),
    (cumulative, '累加和检测'),
    (approximate_entropypoker, '近似熵检测'),
    (linear_complexity, '线性复杂度检测'),
    (maurer_universal, 'Maurer通用统计检测'),
    (discrete_fourier_transform, '离散傅里叶变换检测')
]
detect_mode = ["20000", "1000000", "100000000"]


def detect(bits: str, function: list[int], alpha: float, mode: str):
    with open('mode_settings.json') as config_file:
        config_settings = json.load(config_file)

    output = []
    n = len(bits)

    if mode == '自动选择':
        for i in detect_mode:
            if n <= int(i):
                mode = i
                break
        else:
            mode = detect_mode[-1]

    config: dict = config_settings[mode]
    for fuc in function:
        fuc_name = detect_function[fuc][0].__name__
        for index, cng in enumerate(config[fuc_name]):
            try:
                res, p, q, ote = detect_function[fuc][0](bits, alpha=alpha, **cng)
                output.append((detect_function[fuc][1] + f'({index})', res, p, fuc_name, cng, ote))
                if res is False:
                    break
            except Exception as e:
                output.append((detect_function[fuc][1] + f'({index})', 'Error', str(e), fuc_name, cng))

    return output




