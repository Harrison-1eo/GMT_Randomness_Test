"""
 @project: task_functions.py
 @description: 任务函数，用于接受检测任务并返回检测结果
 @author: Harrison-1eo
 @date: 2023-06-20
 @version: 1.0
"""

from detect import *
import json
import threading

detect_function = [
    (monobit_frequency, '单比特频数检测'),
    (frequency_within_a_block, '块内频数检测'),
    (poker, '扑克检测'),
    (serial, '重叠子序列检测'),
    (runs, '游程总数检测'),
    (runs_distribution, '游程分布检测'),
    (longest_run_of_ones, '块内最大1游程检测'),
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
    """
    description: 检测函数，用于接受检测任务并返回检测结果
    param {str} bits: 待检测的比特流
    param {list[int]} function: 待检测的函数列表，列表中的元素为函数的序号 0-14
    param {float} alpha: 显著性水平
    param {str} mode: 检测模式
    """
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
            except Exception as e:
                output.append((detect_function[fuc][1] + f'({index})', 'Error', str(e), fuc_name, cng))

    return output


def detect_threads(bits: str, function: list[int], alpha: float, mode: str, threads_num: int = 4) -> list:
    """
    description: 使用多线程检测
    """
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

    methods = []
    for fuc in function:
        fuc_name = detect_function[fuc][0].__name__
        for index, cng in enumerate(config[fuc_name]):
            methods.append((detect_function[fuc][0], cng, detect_function[fuc][1], index))

    def run_thread():
        while True:
            with lock:
                if not methods:
                    break
                method, cng, fuc_name, index = methods.pop(0)
            try:
                res, p, q, ote = method(bits, alpha=alpha, **cng)
                output.append((fuc_name + f'({index})', res, p, method.__name__, cng, ote))
            except Exception as e:
                output.append((fuc_name + f'({index})', 'Error', str(e), method.__name__, cng))

    # 创建4个线程并启动它们
    lock = threading.Lock()

    threads = []
    for _ in range(threads_num):
        thread = threading.Thread(target=run_thread)
        thread.start()
        threads.append(thread)

    # 等待所有线程执行完毕
    for thread in threads:
        thread.join()

    return output

