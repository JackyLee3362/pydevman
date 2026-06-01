import customtkinter as ctk


class JsonApp:
    def __init__(self, master: ctk.CTk, font: ctk.CTkFont):
        self.master = master
        self.master.geometry("800x500")

        # ==== 左栏目 ====
        # side=left 靠左排列，fill=y 垂直填满，expand=False 宽度固定
        self.left_frame = ctk.CTkFrame(self.master)
        self.left_frame.pack(side="left", fill="y", padx=5, pady=5)
        ctk.CTkLabel(self.left_frame, text="左侧栏", font=font).pack(pady=20)
        ctk.CTkButton(self.left_frame, text="按钮1", font=font).pack(
            fill="x", padx=10, pady=5
        )
        ctk.CTkButton(self.left_frame, text="按钮2", font=font).pack(
            fill="x", padx=10, pady=5
        )

        # ==== 右栏目 ====
        self.right_frame = ctk.CTkFrame(self.master)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.right_label = ctk.CTkLabel(self.right_frame, text="右侧内容区", font=font)
        self.right_label.pack(pady=20)


if __name__ == "__main__":
    app = ctk.CTk()
    font = ctk.CTkFont(family="Microsoft YaHei UI", size=14)
    gui = JsonApp(master=app, font=font)
    app.mainloop()
