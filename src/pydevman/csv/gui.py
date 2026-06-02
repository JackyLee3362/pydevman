import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

from .core import get_csv_no, split_csv_with_cnt


class GetCustomerApp:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("提取用户请求")
        self.master.geometry("500x600")

        # 框架
        self._init_left_frame()
        self._init_right_frame()

        # left
        self._init_max_count_part()
        self._init_file_picker()
        self._init_dst_dir_picker()
        self._init_submit_part()

        # right
        self._init_read_text()

    def _init_left_frame(self):
        # ==== 左侧面板 ====
        self.left_frame = ttk.Frame(self.master, padding=12)
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.left_label = ttk.Label(self.left_frame, text="配置")
        self.left_label.pack()

    def _init_right_frame(self):
        # ==== 右侧面板 ====
        self.right_frame = ttk.Frame(self.master)
        self.right_frame.pack(side="right", fill="both", expand=True)
        self.right_label = ttk.Label(self.right_frame, text="输出")
        self.right_label.pack()

    def _init_max_count_part(self):
        self._per_csv_max_cnt: int = tk.IntVar(value=100000)
        ttk.Label(self.left_frame, text="每个csv最大数量").pack()
        ttk.Entry(self.left_frame, textvariable=self._per_csv_max_cnt).pack()

    def _init_submit_part(self):
        ttk.Button(self.left_frame, text="提交", command=self._action_commit).pack()

    def _init_file_picker(self):
        self._src_file_path: Path | None = None
        ttk.Label(self.left_frame, text=self._src_file_path or "").pack()
        ttk.Button(
            self.left_frame, text="选择原始文件", command=self._action_pick_file
        ).pack()

    def _init_dst_dir_picker(self):
        self._dst_dir_path: Path | None = None
        ttk.Label(self.left_frame, text=self._src_file_path or "").pack()
        ttk.Button(
            self.left_frame, text="选择目标文件夹", command=self._action_pick_dir
        ).pack()

    def _init_read_text(self):
        self._list_result = ""
        tk.Text(self.right_frame, state="disabled").pack(fill="y")

    def _action_pick_file(self):
        path = Path(filedialog.askopenfilename())
        print("选择文件:", path)
        self._src_file_path = path

    def _action_pick_dir(self):
        path = Path(filedialog.askdirectory())
        print("选择目录,", path)
        self._dst_dir_path = path

    def _action_copy(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self._list_result)
        print("已复制到剪贴板...")

    def _action_commit(self):
        # 目录路径
        print("提交任务")
        li = get_csv_no(self._src_file_path, 0)
        print("总行数是: ", len(li))
        max_count = self._per_csv_max_cnt.get()
        split_csv_with_cnt(self._src_file_path, self._dst_dir_path, max_count)


if __name__ == "__main__":
    app = tk.Tk()
    gui = GetCustomerApp(app)
    app.mainloop()
