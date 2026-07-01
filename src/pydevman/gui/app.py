"""pydevman 统一 GUI 入口 — 纯 tkinter

架构：
- 左侧栏列出所有模块，点击切换右侧面板
- 每个模块提供一个 tk.Frame 子类的工厂函数
- 模块 Frame 懒加载：首次点击时才创建
"""

import tkinter as tk

# ============================================================
# 模块注册表 — 每新增一个模块，在这里加一行即可
# ============================================================
def _json_factory(parent: tk.Widget) -> tk.Frame:
    from pydevman.gui.json_panel import JsonFrame

    return JsonFrame(parent)


MODULES: dict[str, dict] = {
    "JSON": {
        "factory": _json_factory,
        "description": "JSON 解析 / 序列化",
    },
    # 后续模块在这里注册：
    # "CSV": {
    #     "factory": _csv_factory,
    #     "description": "CSV 解析 / 拆分",
    # },
}


# ============================================================
# 主应用
# ============================================================
class PyDevmanApp:
    """统一 GUI 窗口：sidebar + content 布局"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("pydevman - 开发工具集")
        self.root.geometry("900x600")
        self.root.minsize(600, 400)

        self._frames: dict[str, tk.Frame] = {}  # name → created Frame
        self._current: tk.Frame | None = None

        self._build_sidebar()
        self._build_content()

        # 默认展示第一个模块
        first = next(iter(MODULES.keys()))
        self._show_module(first)

    # ---- 构建 UI ----

    def _build_sidebar(self):
        """左侧导航栏"""
        sidebar = tk.Frame(self.root, bg="#2c2c2c", width=160)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # 标题
        tk.Label(
            sidebar,
            text="pydevman",
            font=("", 14, "bold"),
            fg="white",
            bg="#2c2c2c",
        ).pack(pady=(16, 20))

        # 模块按钮
        for name, info in MODULES.items():
            desc = info.get("description", "")
            btn = tk.Button(
                sidebar,
                text=f"{name}\n{desc}",
                font=("", 9),
                justify="left",
                anchor="w",
                padx=12,
                pady=8,
                relief="flat",
                bg="#3c3c3c",
                fg="white",
                activebackground="#505050",
                activeforeground="white",
                command=lambda n=name: self._show_module(n),
            )
            btn.pack(fill="x", padx=6, pady=2)

    def _build_content(self):
        """右侧内容容器"""
        self._content_area = tk.Frame(self.root)
        self._content_area.pack(side="right", fill="both", expand=True)

    # ---- 模块切换 ----

    def _show_module(self, name: str):
        """切换到指定模块面板（懒加载）"""
        info = MODULES.get(name)
        if info is None:
            return

        # 懒加载
        if name not in self._frames:
            factory = info["factory"]
            frame = factory(self._content_area)
            self._frames[name] = frame

        # 隐藏当前
        if self._current is not None:
            self._current.pack_forget()

        # 显示目标
        target = self._frames[name]
        target.pack(fill="both", expand=True)
        self._current = target


# ============================================================
# 启动入口
# ============================================================
def launch_gui():
    """启动 pydevman 统一 GUI"""
    root = tk.Tk()
    PyDevmanApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
