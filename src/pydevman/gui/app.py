"""pydevman 统一 GUI 入口 — 纯 tkinter

架构：
- 菜单栏提供「设置」入口
- 左侧栏列出所有模块，点击切换右侧面板
- 每个模块提供一个 tk.Frame 子类的工厂函数
- 模块 Frame 懒加载：首次点击时才创建
"""

import tkinter as tk

from pydevman.gui.settings_panel import SettingsDialog, get_app_font

# ============================================================
# 模块注册表 — 每新增一个模块，在这里加一行即可
# ============================================================
def _json_factory(parent: tk.Widget) -> tk.Frame:
    from pydevman.gui.json_panel import JsonFrame

    return JsonFrame(parent)


def _csv_factory(parent: tk.Widget) -> tk.Frame:
    from pydevman.gui.csv_panel import CsvFrame

    return CsvFrame(parent)


def _csv_split_factory(parent: tk.Widget) -> tk.Frame:
    from pydevman.gui.csv_split_panel import CsvSplitFrame

    return CsvSplitFrame(parent)


MODULES: dict[str, dict] = {
    "JSON": {
        "factory": _json_factory,
        "description": "JSON 解析 / 序列化",
    },
    "CSV": {
        "factory": _csv_factory,
        "description": "CSV 解析 / 序列化",
    },
    "CSV 拆分": {
        "factory": _csv_split_factory,
        "description": "大文件拆分",
    },
}


# ============================================================
# 主应用
# ============================================================
class PyDevmanApp:
    """统一 GUI 窗口：菜单栏 + sidebar + content 布局"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("pydevman - 开发工具集")
        self.root.geometry("900x600")
        self.root.minsize(600, 400)

        self._frames: dict[str, tk.Frame] = {}
        self._current: tk.Frame | None = None

        # 加载字体设置并全局应用
        self._apply_global_font()

        self._build_menu()
        self._build_sidebar()
        self._build_content()

        # 默认展示第一个模块
        first = next(iter(MODULES.keys()))
        self._show_module(first)

    # ---- 全局字体 ----

    def _apply_global_font(self):
        """将保存的字体应用到根窗口（影响后续新建的 ttk 组件）"""
        family, size = get_app_font()
        font_tuple = (family, size)
        self.root.option_add("*Font", font_tuple)
        # ttk 需要特殊处理
        style = tk.ttk.Style()
        style.configure(".", font=font_tuple)

    # ---- 菜单栏 ----

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="设置...", command=self._open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.destroy)

    # ---- 侧边栏 ----

    def _build_sidebar(self):
        sidebar = tk.Frame(self.root, bg="#2c2c2c", width=160)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="pydevman",
            font=("", 14, "bold"), fg="white", bg="#2c2c2c",
        ).pack(pady=(16, 20))

        for name, info in MODULES.items():
            desc = info.get("description", "")
            btn = tk.Button(
                sidebar,
                text=f"{name}\n{desc}",
                font=("", 9),
                justify="left", anchor="w",
                padx=12, pady=8,
                relief="flat",
                bg="#3c3c3c", fg="white",
                activebackground="#505050", activeforeground="white",
                command=lambda n=name: self._show_module(n),
            )
            btn.pack(fill="x", padx=6, pady=2)

    # ---- 内容区 ----

    def _build_content(self):
        self._content_area = tk.Frame(self.root)
        self._content_area.pack(side="right", fill="both", expand=True)

    # ---- 模块切换 ----

    def _show_module(self, name: str):
        info = MODULES.get(name)
        if info is None:
            return

        if name not in self._frames:
            factory = info["factory"]
            frame = factory(self._content_area)
            self._frames[name] = frame

        if self._current is not None:
            self._current.pack_forget()

        target = self._frames[name]
        target.pack(fill="both", expand=True)
        self._current = target

    # ---- 设置 ----

    def _open_settings(self):
        """打开设置弹窗"""

        def on_save(family: str, size: int):
            """设置保存后全局应用字体"""
            font_tuple = (family, size)
            self.root.option_add("*Font", font_tuple)
            style = tk.ttk.Style()
            style.configure(".", font=font_tuple)

        SettingsDialog(self.root, on_save_callback=on_save)


# ============================================================
# 启动入口
# ============================================================
def launch_gui():
    root = tk.Tk()
    PyDevmanApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
