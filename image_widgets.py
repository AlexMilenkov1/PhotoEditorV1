import customtkinter as ctk
from tkinter import filedialog, Canvas
from settings import *


class ImportImage(ctk.CTkFrame):
    def __init__(self, parent, import_funct):
        super().__init__(master=parent)

        self.import_funct = import_funct

        self.grid(row=0, columnspan=2, column=0, sticky="nsew")

        import_image_button = ctk.CTkButton(self, text='open image', command=self.open_dialog)
        import_image_button.pack(expand=True)

    def open_dialog(self):
        path = filedialog.askopenfile().name
        self.import_funct(path)


class ImageOutput(Canvas):
    def __init__(self, parent, resize_image):
        super().__init__(parent, background='#242424', bd=0, highlightthickness=0, relief='ridge')

        self.grid(row=0, column=1, sticky="nsew")

        self.bind("<Configure>", resize_image)


class CloseImage(ctk.CTkButton):
    def __init__(self, parent, funct):
        super().__init__(master=parent,
                         text="x",
                         text_color=WHITE,
                         hover_color=CLOSE_RED,
                         fg_color='transparent',
                         width=40,
                         height=40,
                         command=funct)

        self.place(relx=0.99, rely=0.03, anchor='ne')
