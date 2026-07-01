"""JSON 工具 — GUI 面板（纯 tkinter，可嵌入统一 GUI 窗口）"""

import json
import tkinter as tk
from tkinter import messagebox, ttk

from pydevman.core.json.handler import api_dump_json
from pydevman.core.json.service import parse_str_to_json
from pydevman.helper.interactive import from_clipboard_or_file, to_clipboard_or_file


class JsonFrame(tk.Frame):
    """JSON 解析/序列化面板，可嵌入父窗口"""

    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **kwargs)
        self._build_ui()

    # ============================================================
    # UI 构建
    # ============================================================

    def _build_ui(self):
        """两栏布局：左侧操作栏 + 右侧输入/输出区"""
        # ---- 右侧：输入/输出（先创建，因为左侧按钮需要引用） ----
        right = tk.Frame(self)
        right.pack(side="right", fill="both", expand=True)

        # 输入区
        tk.Label(right, text="输入", anchor="w").pack(fill="x", padx=4, pady=(4, 0))
        self._txt_input = tk.Text(right, height=10, wrap="none", undo=True)
        self._txt_input.pack(fill="both", expand=True, padx=4, pady=2)

        # 输入区工具栏
        input_bar = tk.Frame(right)
        input_bar.pack(fill="x", padx=4)
        tk.Button(input_bar, text="从剪贴板粘贴", command=self._paste_input).pack(
            side="left"
        )
        tk.Button(input_bar, text="清空输入", command=lambda: self._clear(self._txt_input)).pack(
            side="left", padx=2
        )

        # 输出区
        tk.Label(right, text="输出", anchor="w").pack(fill="x", padx=4, pady=(6, 0))
        self._txt_output = tk.Text(right, height=10, wrap="none", state="disabled")
        self._txt_output.pack(fill="both", expand=True, padx=4, pady=2)

        # 输出区工具栏
        output_bar = tk.Frame(right)
        output_bar.pack(fill="x", padx=4)
        tk.Button(output_bar, text="复制输出", command=self._copy_output).pack(side="left")
        tk.Button(
            output_bar, text="清空输出", command=lambda: self._clear(self._txt_output)
        ).pack(side="left", padx=2)

        # ---- 左侧：操作按钮 + 选项 ----
        left = tk.Frame(self, width=180)
        left.pack(side="left", fill="y", padx=4, pady=4)
        left.pack_propagate(False)  # 固定宽度

        # 操作按钮
        tk.Label(left, text="操作", font=("", 10, "bold")).pack(anchor="w", pady=(0, 4))
        tk.Button(left, text="▶ 解析 JSON", command=self._action_parse).pack(fill="x", pady=1)
        tk.Button(left, text="▶ 序列化输出", command=self._action_dump).pack(fill="x", pady=1)

        # 分隔线
        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=8)

        # 选项
        tk.Label(left, text="解析选项", font=("", 10, "bold")).pack(anchor="w", pady=(0, 4))

        self._var_recursive = tk.BooleanVar(value=False)
        tk.Checkbutton(left, text="递归去转义", variable=self._var_recursive).pack(
            anchor="w"
        )

        self._var_del_tag = tk.BooleanVar(value=False)
        tk.Checkbutton(left, text="去除 HTML 标签", variable=self._var_del_tag).pack(
            anchor="w"
        )

        self._var_inline = tk.BooleanVar(value=False)
        tk.Checkbutton(left, text="单行输出", variable=self._var_inline).pack(anchor="w")

        # 过滤选项
        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=8)

        tk.Label(left, text="过滤前缀（逗号分隔）").pack(anchor="w")
        self._entry_prefix = tk.Entry(left)
        self._entry_prefix.pack(fill="x", pady=1)

        tk.Label(left, text="过滤后缀（逗号分隔）").pack(anchor="w", pady=(4, 0))
        self._entry_suffix = tk.Entry(left)
        self._entry_suffix.pack(fill="x", pady=1)

    # ============================================================
    # 动作
    # ============================================================

    def _action_parse(self):
        """解析输入区文本为 JSON"""
        raw = self._get_input()
        if not raw.strip():
            messagebox.showwarning("提示", "输入为空")
            return

        try:
            prefix = self._parse_list(self._entry_prefix.get())
            suffix = self._parse_list(self._entry_suffix.get())
            result = parse_str_to_json(
                raw,
                recursive=self._var_recursive.get(),
                del_tag=self._var_del_tag.get(),
                prefix=prefix,
                suffix=suffix,
            )
            output = api_dump_json(result, inline=self._var_inline.get())
            self._set_output(output)
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON 解析失败", str(e))
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def _action_dump(self):
        """把输入区内容当作 JSON 序列化为紧凑字符串"""
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
    # 输入 / 输出 辅助
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
        """从剪贴板粘贴到输入区"""
        try:
            text = from_clipboard_or_file(None)
            self._txt_input.delete("1.0", "end")
            self._txt_input.insert("1.0", text)
        except Exception as e:
            messagebox.showerror("剪贴板错误", str(e))

    def _copy_output(self):
        """复制输出区内容"""
        text = self._txt_output.get("1.0", "end-1c")
        if text.strip():
            to_clipboard_or_file(None, text, force=True)
        else:
            messagebox.showwarning("提示", "输出为空")

    @staticmethod
    def _parse_list(entry_text: str) -> list[str] | None:
        """把逗号分隔的字符串解析为列表，空串返回 None"""
        text = entry_text.strip()
        if not text:
            return None
        return [s.strip() for s in text.split(",") if s.strip()]


# ============================================================
# 独立运行
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("JSON 工具")
    root.geometry("800x550")
    JsonFrame(root).pack(fill="both", expand=True)
    root.mainloop()
