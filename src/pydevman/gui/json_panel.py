"""JSON 工具 — GUI 面板（纯 tkinter，可嵌入统一 GUI 窗口）"""

import json
import tkinter as tk
from tkinter import messagebox, ttk

from pydevman.core.json.handler import api_dump_json
from pydevman.core.json.processor import JsonHandler, JsonProcessor
from pydevman.helper.interactive import from_clipboard_or_file, to_clipboard_or_file


class JsonFrame(tk.Frame):
    """JSON 解析/序列化面板"""

    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **kwargs)
        self._build_ui()

    def _build_ui(self):
        # ================================================================
        # 第 1 行：操作工具栏
        # ================================================================
        toolbar = tk.Frame(self, bd=1, relief="groove")
        toolbar.pack(fill="x", padx=6, pady=(6, 2))

        tk.Button(toolbar, text="▶ 解析 JSON", font=("", 10, "bold"),
                  bg="#4a90d9", fg="white", width=14,
                  command=self._action_parse).pack(side="left", padx=4, pady=6)
        tk.Button(toolbar, text="▶ 序列化输出", font=("", 9),
                  width=14, command=self._action_dump).pack(side="left", padx=4, pady=6)

        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=8, pady=2)

        self._var_inline = tk.BooleanVar(value=False)
        tk.Checkbutton(toolbar, text="单行输出", variable=self._var_inline,
                       font=("", 9)).pack(side="left", padx=4)

        # ================================================================
        # 第 2 行：Handler 链配置（4 个卡片）
        # ================================================================
        handler_bar = ttk.LabelFrame(self, text=" Handler 链 · 按编号顺序执行 ", padding=6)
        handler_bar.pack(fill="x", padx=6, pady=2)

        # ①
        f1 = tk.Frame(handler_bar, bd=1, relief="solid", bg="#f0f0f0")
        f1.pack(side="left", padx=3, pady=2, ipadx=4, ipady=2)
        self._var_recursive = tk.BooleanVar(value=False)
        tk.Checkbutton(f1, text="① 递归去转义", variable=self._var_recursive,
                       font=("", 9, "bold"), bg="#f0f0f0").pack(anchor="w", padx=4)
        tk.Label(f1, text="  str → json 再解析", fg="gray", bg="#f0f0f0",
                 font=("", 7)).pack(anchor="w", padx=4)

        # ②
        f2 = tk.Frame(handler_bar, bd=1, relief="solid", bg="#f0f0f0")
        f2.pack(side="left", padx=3, pady=2, ipadx=4, ipady=2)
        self._var_del_tag = tk.BooleanVar(value=False)
        tk.Checkbutton(f2, text="② 去除 HTML 标签", variable=self._var_del_tag,
                       font=("", 9, "bold"), bg="#f0f0f0").pack(anchor="w", padx=4)
        tk.Label(f2, text="  <p>text</p> → text", fg="gray", bg="#f0f0f0",
                 font=("", 7)).pack(anchor="w", padx=4)

        # ③
        f3 = tk.Frame(handler_bar, bd=1, relief="solid", bg="#f0f0f0")
        f3.pack(side="left", padx=3, pady=2, ipadx=4, ipady=2)
        self._var_prefix = tk.BooleanVar(value=False)
        tk.Checkbutton(f3, text="③ 过滤前缀字段", variable=self._var_prefix,
                       font=("", 9, "bold"), bg="#f0f0f0").pack(anchor="w", padx=4)
        self._entry_prefix = tk.Entry(f3, width=16, font=("", 8))
        self._entry_prefix.pack(fill="x", padx=4, pady=(0, 4))
        self._entry_prefix.insert(0, "_, __")

        # ④
        f4 = tk.Frame(handler_bar, bd=1, relief="solid", bg="#f0f0f0")
        f4.pack(side="left", padx=3, pady=2, ipadx=4, ipady=2)
        self._var_suffix = tk.BooleanVar(value=False)
        tk.Checkbutton(f4, text="④ 过滤后缀字段", variable=self._var_suffix,
                       font=("", 9, "bold"), bg="#f0f0f0").pack(anchor="w", padx=4)
        self._entry_suffix = tk.Entry(f4, width=16, font=("", 8))
        self._entry_suffix.pack(fill="x", padx=4, pady=(0, 4))
        self._entry_suffix.insert(0, "Id, Key")

        # ================================================================
        # 第 3+4 行：输入 / 输出（左右分栏）
        # ================================================================
        panes = tk.PanedWindow(self, orient="horizontal", sashrelief="raised", sashwidth=4)
        panes.pack(fill="both", expand=True, padx=6, pady=(2, 6))

        # 输入
        input_frame = ttk.LabelFrame(panes, text=" 输入 ", padding=4)
        panes.add(input_frame, stretch="always")
        self._txt_input = tk.Text(input_frame, wrap="none", undo=True, font=("Consolas", 10))
        self._txt_input.pack(fill="both", expand=True)

        input_bar = tk.Frame(input_frame)
        input_bar.pack(fill="x", pady=(2, 0))
        tk.Button(input_bar, text="粘贴", command=self._paste_input, font=("", 8)).pack(side="left")
        tk.Button(input_bar, text="清空", command=lambda: self._clear(self._txt_input),
                  font=("", 8)).pack(side="left", padx=2)

        # 输出
        output_frame = ttk.LabelFrame(panes, text=" 输出 ", padding=4)
        panes.add(output_frame, stretch="always")
        self._txt_output = tk.Text(output_frame, wrap="none", state="disabled",
                                   font=("Consolas", 10))
        self._txt_output.pack(fill="both", expand=True)

        output_bar = tk.Frame(output_frame)
        output_bar.pack(fill="x", pady=(2, 0))
        tk.Button(output_bar, text="复制", command=self._copy_output, font=("", 8)).pack(side="left")
        tk.Button(output_bar, text="清空", command=lambda: self._clear(self._txt_output),
                  font=("", 8)).pack(side="left", padx=2)

    # ============================================================
    # 动作
    # ============================================================

    def _action_parse(self):
        raw = self._get_input()
        if not raw.strip():
            messagebox.showwarning("提示", "输入为空")
            return

        try:
            processor = JsonProcessor()
            if self._var_recursive.get():
                processor.register(JsonHandler.RECURSIVE_UNESCAPE)
            if self._var_del_tag.get():
                processor.register(JsonHandler.DEL_HTML_TAG)
            if self._var_prefix.get():
                prefix = self._parse_list(self._entry_prefix.get())
                if prefix:
                    processor.register(JsonHandler.FILTER_FIELD_BY_PREFIX, prefix_filter=prefix)
            if self._var_suffix.get():
                suffix = self._parse_list(self._entry_suffix.get())
                if suffix:
                    processor.register(JsonHandler.FILTER_FIELD_BY_SUFFIX, suffix_filter=suffix)
            result = processor.process(raw)

            output = api_dump_json(result, inline=self._var_inline.get())
            self._set_output(output)
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON 解析失败", str(e))
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def _action_dump(self):
        raw = self._get_input()
        if not raw.strip():
            messagebox.showwarning("提示", "输入为空")
            return
        try:
            result = api_dump_json(raw, inline=self._var_inline.get())
            self._set_output(result)
        except Exception as e:
            messagebox.showerror("错误", str(e))

    # ============================================================
    # 辅助
    # ============================================================

    def _get_input(self) -> str:
        return self._txt_input.get("1.0", "end-1c")

    def _set_output(self, text: str):
        self._txt_output.configure(state="normal")
        self._txt_output.delete("1.0", "end")
        self._txt_output.insert("1.0", text)
        self._txt_output.configure(state="disabled")

    def _clear(self, widget: tk.Text):
        state = widget.cget("state")
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        if state == "disabled":
            widget.configure(state="disabled")

    def _paste_input(self):
        try:
            text = from_clipboard_or_file(None)
            self._txt_input.delete("1.0", "end")
            self._txt_input.insert("1.0", text)
        except Exception as e:
            messagebox.showerror("剪贴板错误", str(e))

    def _copy_output(self):
        text = self._txt_output.get("1.0", "end-1c")
        if text.strip():
            to_clipboard_or_file(None, text, force=True)
        else:
            messagebox.showwarning("提示", "输出为空")

    @staticmethod
    def _parse_list(entry_text: str) -> list[str] | None:
        text = entry_text.strip()
        if not text:
            return None
        return [s.strip() for s in text.split(",") if s.strip()]


if __name__ == "__main__":
    root = tk.Tk()
    root.title("JSON 工具")
    root.geometry("900x550")
    JsonFrame(root).pack(fill="both", expand=True)
    root.mainloop()
