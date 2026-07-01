from tkinter import font

import customtkinter as ctk


class App:
    def __init__(self, master: ctk.CTk):
        self.master = master
        self.master.geometry("800x500")

        # 列出所有字体
        all_fonts = list(font.families())
        all_fonts.sort()
        for f in all_fonts:
            print(f)


if __name__ == "__main__":
    app = ctk.CTk()
    gui = App(master=app)
    app.mainloop()
