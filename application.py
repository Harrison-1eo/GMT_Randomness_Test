"""
 @description: GUI界面，用于接受用户输入并调用检测函数
 @author: Harrison-1eo
 @date: 2023/6/23
 @version:  1.0: 通过文本框输入内容，实现基本检测功能
            1.1: 通过文件输入内容，实现基本检测功能
            1.2: 完善错误处理，增加检测条件
            1.3: 调整代码结构，减少重复代码
            2.0: 增加多线程功能，提高检测速度
"""
import tkinter as tk
import os
import time
from tkinter import filedialog
from task_functions import *


class randomnessApp:
    def __init__(self):
        """
        description: 初始化函数，用于创建主窗口
        """
        
        self.root = tk.Tk()
        self.root.title("随机性检测")

        # 设置主窗口字体和大小
        self.root.geometry("300x400")
        self.root.grab_set()

        # 创建标题标签
        title_label = tk.Label(self.root, text="随机性检测工具", font=("微软雅黑", 20))
        title_label.pack(pady=10)

        file_button = tk.Button(self.root, text="通过文件输入", command=self.file_detect_window, width=15, height=3,
                                bg="#5cb85c",
                                fg="#FFFFFF", activebackground="#4cae4c", activeforeground="#FFFFFF",
                                font=("微软雅黑", 12))
        file_button.pack(pady=10)

        input_button = tk.Button(self.root, text="通过文本框输入", command=self.input_detect_window, width=15, height=3,
                                 bg="#5bc0de",
                                 fg="#FFFFFF", activebackground="#46b8da", activeforeground="#FFFFFF",
                                 font=("微软雅黑", 12))
        input_button.pack(pady=10)

        author_button = tk.Button(self.root, text="关于程序", command=self.author_window, width=15, height=3,
                                  bg="#d9534f",
                                  fg="#FFFFFF", activebackground="#c9302c", activeforeground="#FFFFFF",
                                  font=("微软雅黑", 12))
        author_button.pack(pady=10)

    def input_detect_window(self):
        """
        description: 通过文本框输入内容，实现基本检测功能
        """
        
        
        # 关闭窗口时的回调函数
        def on_closing():
            self.root.deiconify()
            input_window.destroy()

        input_window = tk.Toplevel(self.root)
        input_window.title("通过文本框输入")

        self.root.withdraw()  # 隐藏主窗口
        input_window.protocol("WM_DELETE_WINDOW", on_closing)  # 指定关闭窗口时的回调函数
        input_window.grab_set()

        # 左侧frame
        selected_methods, method_checkboxes = self.frame_left(input_window)

        frame_right = tk.Frame(input_window)
        frame_right.pack(side=tk.RIGHT, padx=10, pady=10)

        # 创建标题标签
        title_label_r = tk.Label(frame_right, text="输入01串：")
        title_label_r.pack(anchor=tk.W)

        frame_text = tk.Frame(frame_right)
        frame_text.pack()

        # 创建一个滚动条
        scrollbar = tk.Scrollbar(frame_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建输入框
        text_input = tk.Text(frame_text, width=30, height=15)
        text_input.pack()

        # 将滚动条与文本框关联
        text_input.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_input.yview)

        frame_alpha = tk.Frame(frame_right)
        frame_alpha.pack(anchor=tk.W)

        alpha_label = tk.Label(frame_alpha, text="α：")
        alpha_label.pack(anchor=tk.W, side=tk.LEFT)

        alpha_entry = tk.Entry(frame_alpha, width=15, justify=tk.CENTER)
        alpha_entry.pack(side=tk.LEFT)
        alpha_entry.insert(0, "0.01")

        def gen_test_bits():
            self.gen_test_data(input_window, text_input)
            # text_input.insert('end', bits)

        test_bits = tk.Button(frame_alpha, text="生成测试数据", command=gen_test_bits)
        test_bits.pack(side=tk.RIGHT, padx=10)

        mode_label = tk.Label(frame_right, text="检测模式：")
        mode_label.pack(anchor=tk.W)

        frame_mode = tk.Frame(frame_right)
        frame_mode.pack()

        modes = ["自动选择", "20000", "1000000", "100000000", "自定义"]
        selected_mode = tk.StringVar(value=modes[0])
        for mode in modes:
            mode_button = tk.Radiobutton(frame_mode, text=mode, value=mode, variable=selected_mode)
            mode_button.pack(anchor=tk.W)

        confirm_button = tk.Button(frame_right, text="开始检测",
                                   command=lambda: self.get_info(selected_methods, text_input.get("1.0", "end"),
                                                                 alpha_entry, selected_mode, input_window))
        confirm_button.pack(side=tk.BOTTOM, padx=10)

    def file_detect_window(self):
        """
        description: 通过文件输入内容，实现基本检测功能
        """
        
        # 关闭窗口时的回调函数
        def on_closing():
            self.root.deiconify()
            file_window.destroy()

        file_window = tk.Toplevel(self.root)
        file_window.title("通过文件检测")

        self.root.withdraw()  # 隐藏主窗口
        file_window.protocol("WM_DELETE_WINDOW", on_closing)  # 指定关闭窗口时的回调函数
        file_window.grab_set()

        # 创建一个Frame用于放置标题和勾选框
        selected_methods, method_checkboxes = self.frame_left(file_window)

        frame_right = tk.Frame(file_window)
        frame_right.pack(side=tk.RIGHT, padx=10, pady=10)

        frame_file = tk.Frame(frame_right)
        frame_file.pack(anchor=tk.W)

        # 创建标题标签
        title_label_r = tk.Label(frame_file, text="选择文件：")
        title_label_r.pack(anchor=tk.W, side=tk.LEFT)

        def select_file():
            input_file_path = filedialog.askopenfilename()
            if input_file_path:
                file_path.set(input_file_path)
                blank_label1.pack_forget()

        # 创建选择文件按钮
        file_button = tk.Button(frame_file, text="选择文件", command=select_file)
        file_button.pack(side=tk.LEFT, padx=10)

        # 显示文件路径
        file_path = tk.StringVar()
        file_path.set("未选择文件")
        file_path_label = tk.Label(frame_right, textvariable=file_path, wraplength=200)
        file_path_label.pack()

        blank_label1 = tk.Label(frame_right, text="")
        blank_label1.pack(anchor=tk.W)

        # 文件打开方式
        file_open_mode = tk.Label(frame_right, text="打开方式：")
        file_open_mode.pack(anchor=tk.W)

        file_modes = ["通过二进制比特流读入内容", "以字符串形式读入文件中的0和1"]
        selected_file_mode = tk.StringVar(value=file_modes[1])  # 设置默认选择为第一个选项

        frame_file_mode = tk.Frame(frame_right)
        frame_file_mode.pack()

        def update_selected_mode():
            read_mode = file_modes.index(selected_file_mode.get())

        for mode in file_modes:
            mode_button = tk.Radiobutton(frame_file_mode, text=mode, value=mode, variable=selected_file_mode,
                                         command=update_selected_mode)
            mode_button.pack(anchor=tk.W)

        blank_label2 = tk.Label(frame_right, text="")
        blank_label2.pack(anchor=tk.W)

        frame_alpha = tk.Frame(frame_right)
        frame_alpha.pack(anchor=tk.W)

        alpha_label = tk.Label(frame_alpha, text="α：")
        alpha_label.pack(anchor=tk.W, side=tk.LEFT)

        alpha_entry = tk.Entry(frame_alpha, width=15, justify=tk.CENTER)
        alpha_entry.pack(side=tk.LEFT)
        alpha_entry.insert(0, "0.01")

        mode_label = tk.Label(frame_right, text="检测模式：")
        mode_label.pack(anchor=tk.W)

        frame_mode = tk.Frame(frame_right)
        frame_mode.pack()

        modes = ["自动选择", "20000", "1000000", "100000000", "自定义"]
        selected_mode = tk.StringVar(value=modes[0])
        for mode in modes:
            mode_button = tk.Radiobutton(frame_mode, text=mode, value=mode, variable=selected_mode)
            mode_button.pack(anchor=tk.W)

        def read_file():
            """
            description: 读取文件内容
            """
            selected_path = file_path.get()
            if selected_path == "未选择文件":
                self.worng_window("未选择文件", file_window)
                return
            if not os.path.isfile(selected_path):
                self.worng_window("所选不是文件", file_window)
                return
            if not os.path.exists(selected_path):
                self.worng_window("文件不存在", file_window)
                return
            if not os.access(selected_path, os.R_OK):
                self.worng_window("文件不可读", file_window)
                return

            with open(selected_path, 'rb') as f:
                text = f.read()

            if selected_file_mode.get() == file_modes[0]:
                text = ''.join([bin(c).replace('0b', '') for c in text])
            else:
                try:
                    text = text.decode('utf-8').strip()
                except UnicodeDecodeError:
                    self.worng_window("文件不是由01字符串组成的！", file_window)
                    return

            self.get_info(selected_methods, text, alpha_entry, selected_mode, file_window)

        confirm_button = tk.Button(frame_right, text="开始检测", command=read_file)
        confirm_button.pack(side=tk.BOTTOM, padx=10)

    def frame_left(self, window):

        # 创建一个Frame用于放置标题和勾选框
        frame_left = tk.Frame(window)
        frame_left.pack(side=tk.LEFT, padx=10, pady=10)

        # 创建标题标签
        title_label_l = tk.Label(frame_left, text="可使用的方法：")
        title_label_l.grid(row=0, column=0, sticky=tk.W)

        def select_all():
            for checkbox in method_checkboxes:
                checkbox.select()

        def deselect_all():
            for checkbox in method_checkboxes:
                checkbox.deselect()

        # 创建全选和全不选按钮
        select_all_button = tk.Button(frame_left, text="全选", command=select_all)
        select_all_button.grid(row=0, column=1, sticky=tk.W)

        deselect_all_button = tk.Button(frame_left, text="全不选", command=deselect_all)
        deselect_all_button.grid(row=0, column=2, sticky=tk.W)

        # 创建勾选框
        selected_methods = []
        method_checkboxes = []
        methods_name = [method[1] for method in detect_function]
        for index, method in enumerate(methods_name):
            var = tk.IntVar(value=1)
            checkbox = tk.Checkbutton(frame_left, text=method, variable=var)
            checkbox.grid(row=index + 1, column=0, columnspan=2, sticky=tk.W)
            selected_methods.append(var)
            method_checkboxes.append(checkbox)

        return selected_methods, method_checkboxes

    def get_info(self, selected_methods, text, alpha_entry, selected_mode, window):
        """
        description: 获取输入信息，处理后调用检测方法。包括对输入内容的检测等
        param selected_methods: 勾选框
        param text: 输入的01串
        param alpha_entry: α输入框
        param selected_mode: 检测模式
        param window: 父窗口
        """
        methods = []
        for index, method in enumerate(selected_methods):
            if method.get() == 1:
                methods.append(index)
        if not methods:
            self.worng_window("至少选择一种方法！", window)
            return

        bits = text.strip()
        # 检测输入是否合法
        if not bits:
            self.worng_window("输入不能为空！", window)
            return
        for bit in bits:
            if bit != '0' and bit != '1':
                self.worng_window("输入只能为01串！", window)
                return

        try:
            alpha = float(alpha_entry.get().strip())
        except:
            self.worng_window("α必须为数字！范围为(0, 1)", window)
            return

        if alpha <= 0 or alpha >= 1:
            self.worng_window("α的范围为(0, 1)！", window)
            return

        mode = selected_mode.get()
        if mode == "自定义":
            mode = 'user_mode'
        print(methods, bits, alpha, mode, sep='\n')

        start = time.time()

        if len(bits) < 20001:
            print("单线程模式")
            res = detect(bits, methods, alpha, mode)
        else:
            print("多线程模式")
            res = detect_threads(bits, methods, alpha, mode)

        end = time.time()

        for r in res:
            print(r)

        print("花费时间:", end - start)

        self.answer_window(len(bits), end - start, res, window)

    def gen_test_data(self, window, text):
        import random

        # 创建新窗口
        test_window = tk.Toplevel(window)
        test_window.title("生成测试数据")
        test_window.geometry("300x150")

        # 创建输入框
        length_label = tk.Label(test_window, text="请输入生成数据的长度：")
        length_label.pack(side=tk.TOP, pady=10)

        length_entry = tk.Entry(test_window)
        length_entry.pack(side=tk.TOP, pady=10)

        # 输入框默认值
        length_entry.insert(0, "10000")

        # 创建确认按钮
        def gen_data():
            try:
                l = int(length_entry.get().strip())
            except:
                self.worng_window("请输入数字！", test_window)
                return
            if l <= 0:
                self.worng_window("请输入正整数！", test_window)
                return
            bits = ""
            for i in range(l):
                bits += str(random.randint(0, 1))

            text.delete(1.0, tk.END)
            text.insert('end', bits)
            test_window.destroy()

        confirm_button = tk.Button(test_window, text="开始生成", command=gen_data)
        confirm_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    def author_window(self):
        author_window = tk.Toplevel(self.root)
        author_window.title("关于")

        msg = "作者：Harrison\n" \
              "大作业题目：随机性检测\n" \
              "参考资料：\n" \
              "《GM/T 0005-2021 随机性检测规范》\n" \
              "《GB/T 32915-2016 信息安全技术二元序列随机性检测方法》\n" \
              "敬请老师和助教批评指正!"
        author_label = tk.Label(author_window, text=msg)
        author_label.pack(side=tk.TOP, pady=10)

    def worng_window(self, msg, window):
        wrong_window = tk.Toplevel(window)
        wrong_window.title("错误")
        wrong_window.geometry("300x100")

        wrong_label = tk.Label(wrong_window, text=msg)
        wrong_label.pack(side=tk.TOP, pady=10)

        # 创建确定按钮
        confirm_button = tk.Button(wrong_window, text="确定", command=wrong_window.destroy)
        confirm_button.pack(side=tk.BOTTOM, pady=10)

    def answer_window(self, length, times, res, window):
        answer_window = tk.Toplevel(window)
        answer_window.title("检测结果")

        answer_label = tk.Label(answer_window, text="检测结果如下：", font=("Arial", 20))
        answer_label.grid(row=0, column=0, sticky=tk.W)

        length_label = tk.Label(answer_window, text="输入串长度为：" + str(length))
        length_label.grid(row=1, column=0, sticky=tk.W)

        times_label = tk.Label(answer_window, text="花费时间为：" + str(times) + "s")
        times_label.grid(row=2, column=0, sticky=tk.W)

        name_label = tk.Label(answer_window, text="检测方法")
        name_label.grid(row=3, column=0, sticky=tk.W)

        res_label = tk.Label(answer_window, text="检测结果")
        res_label.grid(row=3, column=1, sticky=tk.W)

        info_label = tk.Label(answer_window, text="计算结果")
        info_label.grid(row=3, column=2, sticky=tk.W)

        for index, r in enumerate(res):
            name_label = tk.Label(answer_window, text=r[0] + ": ")
            name_label.grid(row=index + 4, column=0, sticky=tk.W)

            res_label = tk.Label(answer_window, text=str(r[1]))
            res_label.grid(row=index + 4, column=1, sticky=tk.W)

            info_label = tk.Label(answer_window, text=str(r[2]))
            info_label.grid(row=index + 4, column=2, sticky=tk.W)

        # 创建确定按钮
        confirm_button = tk.Button(answer_window, text="确定", command=answer_window.destroy)
        confirm_button.grid(row=len(res) + 5, column=1, pady=10)

    def run(self):
        try:
            import scipy
        except ImportError:
            self.worng_window("请安装scipy库！\n命令：pip install scipy", self.root)
            self.root.destroy()
        else:
            print("scipy库已安装！")
            self.root.mainloop()


if __name__ == '__main__':
    app = randomnessApp()
    app.run()
