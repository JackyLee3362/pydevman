import customtkinter as ctk


class CsvApp:
    def __init__(self, master: ctk.CTk):
        self.master = master
        self.master.title("CSV 工具集")
        self.master.geometry("500x600")

        self._init_tabview()
        self.add_tab("Csv 解析")
        self.add_tab("Csv 序列化")

    def _init_tabview(self):
        """初始化标签页容器"""
        self.tabview = ctk.CTkTabview(self.master)
        self.tabview.pack(expand=True, fill="both", padx=20, pady=20)

    def add_tab(self, name: str):
        tab = self.tabview.add(name)
        return tab


if __name__ == "__main__":
    app = ctk.CTk()
    gui = CsvApp(app)
    app.mainloop()
