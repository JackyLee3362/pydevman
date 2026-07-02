import tkinter as tk
from tkinter import font


class FontInfoFrame(tk.Frame):
    """系统字体列表面板"""

    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **kwargs)
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="系统字体列表（已输出到控制台）").pack(pady=20)
        all_fonts = list(font.families())
        all_fonts.sort()
        listbox = tk.Listbox(self)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)
        for f in all_fonts:
            listbox.insert("end", f)
            print(f)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("系统字体列表")
    root.geometry("600x400")
    FontInfoFrame(root).pack(fill="both", expand=True)
    root.mainloop()
