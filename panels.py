import customtkinter as ctk
from settings import *
from tkinter import filedialog


class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=DARK_GRAY)

        self.pack(fill='x', pady=4, ipady=8)


class SliderPanel(Panel):
    def __init__(self, parent, text, data, start_value, end_value):
        super().__init__(parent=parent)

        # layout
        self.rowconfigure(0, weight=1, uniform='yes')
        self.rowconfigure(1, weight=1, uniform='yes')
        self.columnconfigure(1, weight=1, uniform='yes')
        self.columnconfigure(1, weight=1, uniform='yes')

        self.data = data
        self.data.trace('w', self.update_value)

        ctk.CTkLabel(self, text=text).grid(row=0, column=0, sticky='w', padx=4)
        self.num_label = ctk.CTkLabel(self, text=data.get())
        self.num_label.grid(row=0, column=1, sticky='e', padx=4)
        ctk.CTkSlider(self,
                      from_=start_value,
                      to=end_value,
                      variable=data).grid(row=1, column=0, columnspan=2, padx=3, pady=3)

    def update_value(self, *args):
        self.num_label.configure(text=f'{round(self.data.get(), 2)}')


class SegmentPanel(Panel):
    def __init__(self, parent, text, data, options):
        super().__init__(parent=parent)

        ctk.CTkLabel(self, text=text).pack()
        ctk.CTkSegmentedButton(self, values=options, variable=data).pack(expand=True, fill='both', padx=4, pady=4)


class SwitchPanel(Panel):
    def __init__(self, parent, *args):
        super().__init__(parent=parent)

        for var, text in args:
            switch = ctk.CTkSwitch(self, text=text, variable=var, fg_color=SLIDER_BG, button_color=BLUE)
            switch.pack(side='left', expand=True, fill='both', padx=10, pady=10)


class DropDownPanel(ctk.CTkOptionMenu):
    def __init__(self, window, drop_options, variable):
        super().__init__(master=window,
                         values=drop_options,
                         variable=variable,
                         dropdown_fg_color='#666',
                         button_color='#444',
                         button_hover_color='#333')

        self.pack(fill='x', pady=5)


class RevertButton(ctk.CTkButton):
    def __init__(self, parent, *args):
        super().__init__(master=parent, text='Revert', command=self.revert)

        self.args = args

        self.pack(side='bottom', pady=10)

    def revert(self):
        for var, value in self.args:
            var.set(value)


class FilePanel(Panel):
    def __init__(self, parent, file_string, name_string):
        super().__init__(parent=parent)

        # data
        self.file_string = file_string
        self.name_string = name_string

        # widgets
        ctk.CTkEntry(self, textvariable=self.name_string).pack(fill='x', padx=20, pady=5)

        frame = ctk.CTkFrame(self, fg_color='transparent')

        jpg_check = ctk.CTkCheckBox(frame, text='jpg', variable=file_string, onvalue='jpg', offvalue='png', command=lambda: self.update_format('jpg'))
        png_check = ctk.CTkCheckBox(frame, text='png', variable=file_string, onvalue='png', offvalue='jpg', command=lambda: self.update_format('png'))

        jpg_check.pack(expand=True, fill='x', pady=10, side='left')
        png_check.pack(expand=True, fill='x', pady=10, side='left')

        frame.pack(fill='x', padx=20)

        self.output = ctk.CTkLabel(self, text=' ')
        self.output.pack()

        self.name_string.trace('w', self.update_text)

    def update_format(self, format_value):
        self.file_string.set(format_value)
        self.update_text()

    def update_text(self, *args):
        if self.name_string:
            text = self.name_string.get().replace(' ', '_') + '.' + self.file_string.get()

            self.output.configure(text=text)


class FilePathPanel(Panel):
    def __init__(self, parent, path_string):
        super().__init__(parent=parent)

        self.path_string = path_string

        explorer_button = ctk.CTkButton(self, text='Open Explorer', command=self.open_dialog)
        explorer_button.pack(fill='x', pady=5, padx=25)

        file_entry = ctk.CTkEntry(self, textvariable=self.path_string)
        file_entry.pack(fill='both', pady=5, padx=12)

    def open_dialog(self):
        path = filedialog.askdirectory()

        self.update_file_entry(path)

    def update_file_entry(self, path):
        self.path_string.set(path)


class SaveButton(ctk.CTkButton):
    def __init__(self, parent, saving_function, file_type, file_name, file_path):
        super().__init__(master=parent, text='save', command=lambda: self.save(saving_function))

        self.file_type = file_type
        self.file_name = file_name
        self.file_path = file_path

        self.pack(side='bottom', pady=10)

    def save(self, saving_function):
        saving_function(self.file_path.get(),
                        self.file_name.get(),
                        self.file_type.get())
