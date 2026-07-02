import tkinter as tk
from tkinter import ttk


class CsvFrame(tk.Frame):
    """CSV 工具集面板，可嵌入父窗口"""

    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **kwargs)
        self._build_ui()

    def _build_ui(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        self.add_tab("Csv 解析")
        self.add_tab("Csv 序列化")

    def add_tab(self, name: str):
        tab = tk.Frame(self.notebook)
        ttk.Label(tab, text=f"{name}（待实现）").pack(pady=40)
        self.notebook.add(tab, text=name)
        return tab


if __name__ == "__main__":
    root = tk.Tk()
    root.title("CSV 工具集")
    root.geometry("500x600")
    CsvFrame(root).pack(fill="both", expand=True)
    root.mainloop()
