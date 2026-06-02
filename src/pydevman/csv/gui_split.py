import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk
from loguru import logger

from pydevman.csv.core import split_csv_with_cnt


class CsvSplitApp:
    def __init__(self, master: ctk.CTk):
        # ======== 主界面 ========
        self.master = master

        # ======== 功能区域 ========
        self._init_function_frame(master)

        # ======== 结果区域 ========
        self._init_result_frame(master)

    def _init_function_frame(self, parent: ctk.CTk):
        frame = ctk.CTkFrame(parent)
        frame.pack(side="top", fill="both", expand=True)

        # ==== 功能区 ====
        self._init_function_label(frame, 0)
        # 行1: 最大行数配置
        self._init_row_max_cnt(frame, 1)
        # 行2: 文件选择器
        self._init_row_src_file(frame, 2)
        # 行3: 文件夹选择器
        self._init_row_dst_dir(frame, 3)
        # 行4: 按钮组
        self._init_buttons(frame, 4)

    def _init_function_label(self, parent: ctk.CTk, row: int):
        ctk.CTkLabel(parent, text="配置").grid(row=row)

    def _init_result_frame(self, parent: ctk.CTk):
        # ==== 结果区 ====
        frame = ctk.CTkFrame(parent)
        frame.pack(side="bottom", fill="both", expand=True)
        self._init_result_label(frame, 0)
        self._init_read_text(frame, 1)

    def _init_row_max_cnt(self, parent: ctk.CTk, row: int):
        text = "最大行数"
        ctk.CTkLabel(parent, text=text).grid(row=row, column=0)

        self._per_csv_max_cnt: int = tk.IntVar(value=100000)
        ctk.CTkEntry(parent, textvariable=self._per_csv_max_cnt).grid(row=row, column=1)

    def _init_row_src_file(self, parent: ctk.CTk, row: int):
        label_text = "待拆分文件"
        ctk.CTkLabel(parent, text=label_text).grid(row=row, column=0, padx=5, pady=5)

        self._src_file_path = ctk.StringVar()
        entry = ctk.CTkEntry(parent, textvariable=self._src_file_path, state="disable")
        entry.grid(row=row, column=1, padx=5, pady=5)

        text = "浏览"
        btn = ctk.CTkButton(parent, text=text, command=self._action_pick_file)
        btn.grid(row=row, column=2, padx=5, pady=5)

    def _init_row_dst_dir(self, parent: ctk.CTk, row: int):
        self._dst_dir_path = ctk.StringVar()

        label_text = "目标目录"
        ctk.CTkLabel(parent, text=label_text).grid(row=row, column=0, padx=5, pady=5)

        entry = ctk.CTkEntry(parent, textvariable=self._dst_dir_path, state="disable")
        entry.grid(row=row, column=1, padx=5, pady=5)

        text = "浏览"
        btn = ctk.CTkButton(parent, text=text, command=self._action_pick_dir)
        btn.grid(row=row, column=2, padx=5, pady=5)

    def _init_buttons(self, parent: ctk.CTk, row: int):
        text = "提交"
        btn = ctk.CTkButton(parent, text=text, command=self._action_commit)
        btn.grid(row=row, column=1, padx=5, pady=5)

    def _init_result_label(self, parent: ctk.CTk, row: int):
        ctk.CTkLabel(parent, text="输出").grid(row=row)

    def _init_read_text(self, parent: ctk.CTk, row: int):
        self._list_result = ""
        tk.Text(parent, state="disabled").grid(row=row)

    def _action_pick_file(self):
        path = filedialog.askopenfilename()
        logger.info("选择文件:", path)
        self._src_file_path.set(path)

    def _action_pick_dir(self):
        path = filedialog.askdirectory()
        logger.info("选择目录,", path)
        self._dst_dir_path.set(path)

    def _action_copy(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self._list_result)
        logger.info("已复制到剪贴板...")

    def _action_commit(self):
        # 目录路径
        logger.info("提交任务")
        max_count = self._per_csv_max_cnt.get()
        src_file = Path(self._src_file_path.get())
        dst_dir = Path(self._dst_dir_path.get())
        split_csv_with_cnt(src_file, dst_dir, max_count)


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("CSV 拆分工具")
    app.geometry("500x600")
    gui = CsvSplitApp(app)
    app.mainloop()
