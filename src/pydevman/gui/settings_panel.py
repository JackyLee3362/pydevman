"""应用设置 — 字体/字号选择，持久化到 ~/.pydevman_settings.json"""

import json
import tkinter as tk
from pathlib import Path
from tkinter import font, messagebox, ttk

SETTINGS_FILE = Path.home() / ".pydevman_settings.json"

DEFAULT_SETTINGS = {
    "font_family": "Microsoft YaHei UI",
    "font_size": 12,
}


def load_settings() -> dict:
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict):
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def get_app_font() -> tuple[str, int]:
    """供各模块调用，获取当前字体配置"""
    s = load_settings()
    return s["font_family"], s["font_size"]


class SettingsDialog(tk.Toplevel):
    """设置弹窗"""

    def __init__(self, parent: tk.Tk, on_save_callback=None):
        super().__init__(parent)
        self.title("设置")
        self.geometry("480x380")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()  # 模态

        self._on_save_callback = on_save_callback
        self._settings = load_settings()
        self._fonts = sorted(font.families())
        self._build_ui()
        self._apply_to_ui()

    def _build_ui(self):
        f = ttk.Frame(self, padding=20)
        f.pack(fill="both", expand=True)

        # 字体
        ttk.Label(f, text="字体", font=("", 10, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 2))
        self._combo_font = ttk.Combobox(f, values=self._fonts, state="readonly", width=42)
        self._combo_font.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        self._combo_font.bind("<<ComboboxSelected>>", lambda e: self._refresh_preview())
        self._combo_font.bind("<KeyRelease>", self._filter_font_list)

        # 字号
        ttk.Label(f, text="字号", font=("", 10, "bold")).grid(row=2, column=0, sticky="w", pady=(0, 2))
        size_bar = ttk.Frame(f)
        size_bar.grid(row=3, column=0, sticky="w", pady=(0, 12))
        self._spin_size = ttk.Spinbox(size_bar, from_=8, to=48, width=6)
        self._spin_size.pack(side="left")
        self._spin_size.bind("<<Increment>>", lambda e: self._refresh_preview())
        self._spin_size.bind("<<Decrement>>", lambda e: self._refresh_preview())
        self._spin_size.bind("<KeyRelease>", lambda e: self._refresh_preview())

        # 预览
        ttk.Label(f, text="预览", font=("", 10, "bold")).grid(row=4, column=0, sticky="w", pady=(0, 2))
        self._lbl_preview = tk.Label(
            f, text="你好世界 Hello World\n0123456789 ABCDabcd",
            relief="sunken", anchor="center", background="white", height=4,
        )
        self._lbl_preview.grid(row=5, column=0, sticky="ew", pady=(0, 16))

        # 按钮
        btn_bar = ttk.Frame(f)
        btn_bar.grid(row=6, column=0, sticky="e")
        ttk.Button(btn_bar, text="保存并应用", command=self._save).pack(side="right")
        ttk.Button(btn_bar, text="恢复默认", command=self._reset).pack(side="right", padx=(0, 8))

        f.columnconfigure(0, weight=1)

    def _apply_to_ui(self):
        family = self._settings["font_family"]
        size = self._settings["font_size"]
        self._combo_font.set(family)
        self._spin_size.set(str(size))
        self._refresh_preview()

    def _refresh_preview(self):
        family = self._combo_font.get()
        try:
            size = int(self._spin_size.get())
        except ValueError:
            size = 12
        self._lbl_preview.configure(font=(family, size))

    def _filter_font_list(self, _event=None):
        typed = self._combo_font.get().lower()
        filtered = [f for f in self._fonts if typed in f.lower()]
        self._combo_font["values"] = filtered

    def _save(self):
        family = self._combo_font.get()
        try:
            size = int(self._spin_size.get())
        except ValueError:
            size = DEFAULT_SETTINGS["font_size"]

        self._settings["font_family"] = family
        self._settings["font_size"] = size
        save_settings(self._settings)

        # 应用全局字体到 Tk 根窗口
        if self._on_save_callback:
            self._on_save_callback(family, size)

        messagebox.showinfo("设置", f"已保存\n字体: {family}\n字号: {size}\n\n新打开的模块将使用新字体。")
        self.destroy()

    def _reset(self):
        self._settings = DEFAULT_SETTINGS.copy()
        self._apply_to_ui()
