"""
 @description: 
 @author: Harrison-1eo
 @date: 2023/6/23
 @version: 1.0
"""
import tkinter as tk
from task_functions import *

class randomnessApp():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("随机性检测")
        

    def detect_window_input(self):
        # self.window置顶
        self.window.lift()
        
        # 创建一个Frame用于放置标题和勾选框
        frame_left = tk.Frame(self.window)
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

        frame_right = tk.Frame(self.window)
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
        text = tk.Text(frame_text, width=30, height=15)
        text.pack()

        # 将滚动条与文本框关联
        text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text.yview)

        frame_alpha = tk.Frame(frame_right)
        frame_alpha.pack(anchor=tk.W)

        alpha_label = tk.Label(frame_alpha, text="α：")
        alpha_label.pack(anchor=tk.W, side=tk.LEFT)

        alpha_entry = tk.Entry(frame_alpha, width=15, justify=tk.CENTER)
        alpha_entry.pack(side=tk.LEFT)
        alpha_entry.insert(0, "0.01")

        def gen_test_bits():
            bits = self.gen_test_data()
            text.insert('end', bits)

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

        def get_info():
            methods = []
            for index, method in enumerate(selected_methods):
                if method.get() == 1:
                    methods.append(index)
            if not methods:
                self.worng_window("至少选择一种方法！")
                return

            bits = text.get("1.0", "end").strip()
            # 检测输入是否合法
            if not bits:
                self.worng_window("输入不能为空！")
                return
            for bit in bits:
                if bit != '0' and bit != '1':
                    self.worng_window("输入只能为01串！")
                    return

            alpha = float(alpha_entry.get())
            if alpha <= 0 or alpha >= 1:
                self.worng_window("α的范围为(0, 1)！")
                return

            mode = selected_mode.get()
            if mode == "自定义":
                mode = 'user_mode'
            print(methods, bits, alpha, mode, sep='\n')

            detecting_window = tk.Toplevel(self.window)
            detecting_window.title("检测中")
            detecting_window.geometry("300x100")

            detecting_label = tk.Label(detecting_window, text="检测中，请稍后...", font=("Arial", 20))
            detecting_label.pack()

            res = detect(bits, methods, alpha, mode)
            for r in res:
                print(r)

            detecting_window.destroy()
            self.answer_window(len(bits), res)


        # 创建确定按钮
        confirm_button = tk.Button(frame_right, text="开始检测", command=get_info)
        confirm_button.pack(side=tk.BOTTOM, pady=10)


    def gen_test_data(self, l=1000):
        import random
        bits = ""
        for i in range(l):
            bits += str(random.randint(0, 1))
        return bits


    def worng_window(self, msg):
        wrong_window = tk.Toplevel(self.window)
        wrong_window.title("错误")
        wrong_window.geometry("300x100")

        wrong_label = tk.Label(wrong_window, text=msg)
        wrong_label.pack(side=tk.TOP, pady=10)

        # 创建确定按钮
        confirm_button = tk.Button(wrong_window, text="确定", command=wrong_window.destroy)
        confirm_button.pack(side=tk.BOTTOM, pady=10)


    def answer_window(self, l, res):
        answer_window = tk.Toplevel(self.window)
        answer_window.title("检测结果")

        answer_label = tk.Label(answer_window, text="检测结果如下：", font=("Arial", 20))
        answer_label.grid(row=0, column=0, sticky=tk.W)

        length_label = tk.Label(answer_window, text="输入串长度为："+str(l))
        length_label.grid(row=1, column=0, sticky=tk.W)

        for index, r in enumerate(res):
            name_label = tk.Label(answer_window, text=r[0]+": ")
            name_label.grid(row=index+2, column=0, sticky=tk.W)

            res_label = tk.Label(answer_window, text=str(r[1]))
            res_label.grid(row=index+2, column=1, sticky=tk.W)

            info_label = tk.Label(answer_window, text=str(r[2]))
            info_label.grid(row=index+2, column=2, sticky=tk.W)

        # 创建确定按钮
        confirm_button = tk.Button(answer_window, text="确定", command=answer_window.destroy)
        confirm_button.grid(row=len(res)+2, column=0, columnspan=3, pady=10)


    def run(self):
        self.detect_window_input()
        self.window.mainloop()
        
        try:
            import scipy
        except ImportError:
            self.worng_window("请安装scipy库！\n命令：pip install scipy")
            self.window.destroy()

if __name__ == '__main__':
    app = randomnessApp()
    app.run()
