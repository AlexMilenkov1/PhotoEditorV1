import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
from menu import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # setup
        ctk.set_appearance_mode("dark")
        self.geometry('1000x600')
        self.minsize(800, 500)
        self.title('Photo Editor')

        # grid
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='yes')
        self.columnconfigure(1, weight=6, uniform='yes')

        # canvas_data
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0

        self.init_parameters()
        self.import_image_but = ImportImage(self, self.import_image)

        # run
        self.mainloop()

    def init_parameters(self):
        self.pos_var = {
            "rotation": ctk.DoubleVar(value=ROTATE_DEFAULT),
            "zoom": ctk.DoubleVar(value=ZOOM_DEFAULT),
            "flip": ctk.StringVar(value=FLIP_OPTIONS[0])
        }
        self.color_var = {
            'brightness': ctk.DoubleVar(value=BRIGHTNESS_DEFAULT),
            'vibrance': ctk.DoubleVar(value=VIBRANCE_DEFAULT),
            'grayscale': ctk.BooleanVar(value=GRAYSCALE_DEFAULT),
            'invert': ctk.BooleanVar(value=INVERT_DEFAULT)
        }
        self.effect_var = {
            'effect': ctk.StringVar(value=EFFECT_OPTIONS[0]),
            'contrast': ctk.DoubleVar(value=CONTRAST_DEFAULT),
            'blur': ctk.DoubleVar(value=BLUR_DEFAULT)
        }

        combined_vars = list(self.pos_var.values()) + list(self.color_var.values()) + list(self.effect_var.values())

        for var in combined_vars:
            var.trace('w', self.manipulate_image)

    def manipulate_image(self, *args):
        self.image = self.original_image

        # rotation
        if self.pos_var['rotation'].get() != ROTATE_DEFAULT:
            self.image = self.image.rotate(self.pos_var['rotation'].get())

        # zoom
        if self.pos_var['zoom'].get() != ZOOM_DEFAULT:
            self.image = ImageOps.crop(image=self.image, border=int(self.pos_var['zoom'].get()))

        # flip
        if self.pos_var['flip'].get() != FLIP_OPTIONS[0]:
            if self.pos_var['flip'].get() == 'X':
                self.image = ImageOps.mirror(self.image)
            if self.pos_var['flip'].get() == 'Y':
                self.image = ImageOps.flip(self.image)
            if self.pos_var['flip'].get() == 'Both':
                self.image = ImageOps.mirror(self.image)
                self.image = ImageOps.flip(self.image)

        # brightness and enhance
        self.image = self.image.convert('RGB')
        if self.color_var['brightness'].get() != BRIGHTNESS_DEFAULT:
            brightness_enhance = ImageEnhance.Brightness(self.image)
            self.image = brightness_enhance.enhance(self.color_var['brightness'].get())
        if self.color_var['vibrance'].get() != VIBRANCE_DEFAULT:
            vibrance_enhance = ImageEnhance.Color(self.image)
            self.image = vibrance_enhance.enhance(self.color_var['vibrance'].get())

        # grayscale and invert
        if self.color_var['grayscale'].get() and self.color_var['grayscale'].get() != GRAYSCALE_DEFAULT:
            self.image = ImageOps.grayscale(self.image)
        if self.color_var['invert'].get() and self.color_var['invert'].get() != INVERT_DEFAULT:
            self.image = ImageOps.invert(self.image)

        # blur and contrast
        if self.effect_var['blur'].get() != BLUR_DEFAULT:
            self.image = self.image.filter(ImageFilter.GaussianBlur(self.effect_var['blur'].get()))
        if self.effect_var['contrast'].get() != CONTRAST_DEFAULT:
            self.image = self.image.filter(ImageFilter.UnsharpMask(self.effect_var['contrast'].get()))
        if self.effect_var['effect'].get() != EFFECT_OPTIONS[0]:
            if self.effect_var['effect'].get() == "Emboss":
                self.image = self.image.filter(ImageFilter.EMBOSS)
            if self.effect_var['effect'].get() == "Find Edges":
                self.image = self.image.filter(ImageFilter.FIND_EDGES)
            if self.effect_var['effect'].get() == "Contour":
                self.image = self.image.filter(ImageFilter.CONTOUR)
            if self.effect_var['effect'].get() == "Edge enhance":
                self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)

        self.place_image()

    def import_image(self, path):
        self.original_image = Image.open(path)
        self.image = self.original_image
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_ratio = self.image.size[0] / self.image.size[1]

        self.import_image_but.grid_forget()

        self.image_output = ImageOutput(self, self.resize_image)
        self.close_image = CloseImage(self, self.close_edit)
        self.menu = Menu(self, self.pos_var, self.color_var, self.effect_var, self.save_image)

    def close_edit(self):
        self.image_output.grid_forget()
        self.close_image.place_forget()
        self.menu.grid_forget()
        self.import_image_but = ImportImage(self, self.import_image)

    def resize_image(self, event):
        self.canvas_width = event.width
        self.canvas_height = event.height

        canvas_ratio = self.canvas_width / self.canvas_height

        if canvas_ratio > self.image_ratio:
            self.image_height = self.canvas_height
            self.image_width = self.image_height * self.image_ratio
        else:
            self.image_width = self.canvas_width
            self.image_height = self.image_width / self.image_ratio

        self.place_image()

    def place_image(self):
        self.image_output.delete('all')
        resized_image = self.image.resize((int(self.image_width), int(self.image_height)))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk)

    def save_image(self, path, name, file_type):
        full_file = f'{path}/{name}.{file_type}'
        self.image.save(full_file)

App()
