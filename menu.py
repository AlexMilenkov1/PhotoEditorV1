import customtkinter as ctk
from panels import *


class Menu(ctk.CTkTabview):
    def __init__(self, parent, pos_var, color_var, effect_var, save_image):
        super().__init__(master=parent)

        self.grid(column=0, row=0, sticky='nsew')

        # tabs
        self.add('Position')
        self.add('Color')
        self.add('Effect')
        self.add('Export')

        # widgets
        PositionFrame(self.tab('Position'), pos_var)
        ColorFrame(self.tab('Color'), color_var)
        EffectFrame(self.tab('Effect'), effect_var)
        ExportFrame(self.tab('Export'), save_image)


class PositionFrame(ctk.CTkFrame):
    def __init__(self, parent, pos_var):
        super().__init__(master=parent, fg_color="transparent")

        SliderPanel(self, 'Rotation', pos_var['rotation'], 0, 360)
        SliderPanel(self, 'Zoom', pos_var['zoom'], 0, 200)
        SegmentPanel(self, 'Invert', pos_var['flip'], FLIP_OPTIONS)
        RevertButton(self,
                     (pos_var['rotation'], ROTATE_DEFAULT),
                     (pos_var['zoom'], ZOOM_DEFAULT),
                     (pos_var['flip'], FLIP_OPTIONS[0]))

        self.pack(expand=True, fill='both')


class ColorFrame(ctk.CTkFrame):
    def __init__(self, parent, color_var):
        super().__init__(master=parent, fg_color="transparent")

        SwitchPanel(self, (color_var['grayscale'], 'B/W'), (color_var['invert'], 'Invert'))
        SliderPanel(self, 'Brightness', color_var['brightness'], 0, 5)
        SliderPanel(self, 'Vibrance', color_var['vibrance'], 0, 5)
        RevertButton(self,
                     (color_var['grayscale'], GRAYSCALE_DEFAULT),
                     (color_var['invert'], INVERT_DEFAULT),
                     (color_var['brightness'], BRIGHTNESS_DEFAULT),
                     (color_var['vibrance'], VIBRANCE_DEFAULT))

        self.pack(expand=True, fill='both')


class EffectFrame(ctk.CTkFrame):
    def __init__(self, parent, effect_var):
        super().__init__(master=parent, fg_color="transparent")

        DropDownPanel(self, EFFECT_OPTIONS, effect_var['effect'])
        SliderPanel(self, 'Contrast', effect_var['contrast'], 0, 5)
        SliderPanel(self, 'Blur', effect_var['blur'], 0, 10)
        RevertButton(self,
                     (effect_var['contrast'], CONTRAST_DEFAULT),
                     (effect_var['blur'], BLUR_DEFAULT),
                     (effect_var['effect'], EFFECT_OPTIONS[0]))

        self.pack(expand=True, fill='both')


class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent, save_image):
        super().__init__(master=parent, fg_color="transparent")

        self.file_string = ctk.StringVar(value='jpg')
        self.name_string = ctk.StringVar()

        self.path_string = ctk.StringVar()

        FilePanel(self, self.file_string, self.name_string)
        FilePathPanel(self, self.path_string)
        SaveButton(self, save_image, self.file_string, self.name_string, self.path_string)

        self.pack(expand=True, fill='both')
