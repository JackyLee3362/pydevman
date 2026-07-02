import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

from loguru import logger

from pydevman.core.csv.core import split_csv_with_cnt


class CsvSplitFrame(tk.Frame):
    """CSV 拆分面板，可嵌入父窗口"""

    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **kwargs)
        self._build_ui()

    def _build_ui(self):
        # ---- 功能区域 ----
        func_frame = ttk.LabelFrame(self, text="配置")
        func_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # 行0: 标题
        ttk.Label(func_frame, text="最大行数").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self._per_csv_max_cnt = tk.IntVar(value=100000)
        ttk.Entry(func_frame, textvariable=self._per_csv_max_cnt, width=20).grid(
            row=0, column=1, sticky="w", padx=5, pady=5
        )

        # 行1: 待拆分文件
        ttk.Label(func_frame, text="待拆分文件").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self._src_file_path = tk.StringVar()
        ttk.Entry(func_frame, textvariable=self._src_file_path, state="readonly", width=40).grid(
            row=1, column=1, sticky="ew", padx=5, pady=5
        )
        ttk.Button(func_frame, text="浏览", command=self._action_pick_file).grid(
            row=1, column=2, padx=5, pady=5
        )

        # 行2: 目标目录
        ttk.Label(func_frame, text="目标目录").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self._dst_dir_path = tk.StringVar()
        ttk.Entry(func_frame, textvariable=self._dst_dir_path, state="readonly", width=40).grid(
            row=2, column=1, sticky="ew", padx=5, pady=5
        )
        ttk.Button(func_frame, text="浏览", command=self._action_pick_dir).grid(
            row=2, column=2, padx=5, pady=5
        )

        # 行3: 提交按钮
        ttk.Button(func_frame, text="提交", command=self._action_commit).grid(
            row=3, column=1, pady=10
        )
        func_frame.columnconfigure(1, weight=1)

        # ---- 结果区域 ----
        result_frame = ttk.LabelFrame(self, text="输出")
        result_frame.pack(side="bottom", fill="both", expand=True, padx=10, pady=(0, 10))

        self._list_result = ""
        self._txt_output = tk.Text(result_frame, height=8, state="disabled")
        self._txt_output.pack(fill="both", expand=True, padx=5, pady=5)
        ttk.Button(result_frame, text="复制到剪贴板", command=self._action_copy).pack(
            pady=(0, 5)
        )

    def _action_pick_file(self):
        path = filedialog.askopenfilename()
        if path:
            logger.info("选择文件: {}", path)
            self._src_file_path.set(path)

    def _action_pick_dir(self):
        path = filedialog.askdirectory()
        if path:
            logger.info("选择目录: {}", path)
            self._dst_dir_path.set(path)

    def _action_copy(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self._list_result)
        logger.info("已复制到剪贴板")

    def _action_commit(self):
        logger.info("提交任务")
        max_count = self._per_csv_max_cnt.get()
        src_file = Path(self._src_file_path.get())
        dst_dir = Path(self._dst_dir_path.get())
        split_csv_with_cnt(src_file, dst_dir, max_count)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("CSV 拆分工具")
    root.geometry("500x600")
    CsvSplitFrame(root).pack(fill="both", expand=True)
    root.mainloop()
