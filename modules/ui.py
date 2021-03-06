"""
This module deals with all the UI features
"""
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageGrab
from modules.autotyper import AutoTyper
import keyboard

class Slider:
    def __init__(self,root, max, variable) -> None:
        self.scale = ttk.Scale(root, orient=HORIZONTAL, length=250, from_=0.0, to=max, variable=variable)


class Field:
    def __init__(self,root, variable) -> None:
        self.entry = ttk.Entry(root, textvariable=variable, width=7, font="Verdana")


class UserInterface:
    def __init__(self, root, SCREEN_WIDTH, SCREEN_HEIGHT) -> None:
        self.root = root
        root.title('Typeracer AutoTyper')
        previewframe = ttk.Frame(root, padding=10)
        previewframe.place(x=360, y=75)

        # x label
        X = ttk.Label(root, text='x value of box position:', font='Verdana', padding=10)
        X.grid(column=0, row=0, sticky='nw')

        # x variable
        self.x_value = IntVar()
        self.x_value.set(0.0)

        # x slider
        x_scale = Slider(root, SCREEN_WIDTH, self.x_value)
        x_scale.scale.grid(columnspan=2, column=0, row=1, sticky='nw', pady=10, padx=5)

        # x entry field
        x_field = Field(root, self.x_value)
        x_field.entry.grid(column=1, row=1, padx=5)

        # y labels
        Y = ttk.Label(root, text='y value of box position:', font='Verdana', padding=5)
        Y.grid(column=0, row=4, sticky='nw')

        # y variable
        self.y_value = IntVar()
        self.y_value.set(0.0)

        # y sliders
        y_scale = Slider(root, SCREEN_HEIGHT, self.y_value)
        y_scale.scale.grid(column=0, row=5, sticky='nw', pady=10, padx=5)

        # y entry field
        y_field = Field(root, self.y_value)
        y_field.entry.grid(column=1, row=5, padx=5)

        # height labels
        height = ttk.Label(root, text='The height of the box:', font='Verdana', padding=5)
        height.grid(column=0, row=6, sticky='nw')

        #height variable
        self.height_value = IntVar()
        self.height_value.set(0.0)

        # height slider
        height_scale = Slider(root, SCREEN_HEIGHT, self.height_value)
        height_scale.scale.grid(column=0, row=7, sticky='nw', pady=10, padx=5)

        # height field
        height_field = Field(root, self.height_value)
        height_field.entry.grid(column=1, row=7,padx=5)

        # width labels
        width = ttk.Label(root, text='The width of the box:', font='Verdana', padding=5)
        width.grid(column=0, row=8, sticky='nw', pady=10)

        #width variable
        self.width_value = IntVar()
        self.width_value.set(0.0)

        # width slider
        width_scale = Slider(root, SCREEN_WIDTH, self.width_value)
        width_scale.scale.grid(column=0, row=9, sticky='nw', pady=10, padx=5)

        # width field
        width_field = Field(root, self.width_value)
        width_field.entry.grid(column=1, row=9, padx=5)

        # delay label and sliders
        width = ttk.Label(root, text='Typing delay:', font='Verdana', padding=5)
        width.grid(column=0, row=10, sticky='nw', pady=10)

        #delay variable
        self.delay_value = StringVar()
        self.delay_value.set(0.0)

        # delay slider
        delay_scale = Slider(root, 1.0, self.delay_value)
        delay_scale.scale.grid(column=0, row=11, sticky='nw', pady=10, padx=5)

        # delay field
        delay_field = Field(root, self.delay_value)
        delay_field.entry.grid(column=1, row=11, padx=5)

        #creates a canvas for preview
        self.canvas = Canvas(previewframe, width=700, height=500)
        self.canvas.grid(sticky='E')

        # Preview Buttons and Labels
        self.preview_button = Button(root, text="See Preview", command=self.load_preview, height=1, width=17, font="Verdana", border=5 )
        self.preview_button.grid(column=0, row=16, sticky='nw', padx=10, pady=10)

        preview_label = Message(root, text='Preview of what the program sees below \n     (click the preview button to see)', font="Verdana", width=500)
        preview_label.place(x=445, y=25)

        # set the colour of the default viewing area to black
        self.canvas.create_rectangle(0, 0, 500, 300, fill='black' )

        # keybind for the execution of the program
        self.keybind = "F12"  # default value

        self.run_button = Button(root, text='Run Program', font="Verdana", border=5, command=self.run)
        self.run_button.place(x=550, y=450)

        # change keybind button
        self.change_keybind = Button(root, text='Change Keybinding', font="Verdana",
                                height=1, width=17, border=5, command=self.update_keybinding)
        self.change_keybind.grid(column=0, row=13, sticky='nw', padx=10, pady=10)

    def run(self):
        self.check_error_message()
        # Special Inputs
        key_dict = {'Prior': 'page up',
                    'Next': 'page down',
                    'Shift_L': 'left shift',
                    'Shift_R': 'right shift',
                    'Control_L': 'left control',
                    'Control_R': 'right control',
                    'Alt_L': 'left alt',
                    'Alt_R': 'right alt',
                    'Win_L': 'left windows',
                    'Win_R': 'right windows',
                    'quoteleft': '`'}

        self.button_state('disabled')
        self.root.update()

        try:
            autotyper = AutoTyper(self.x_value.get(), self.y_value.get(),
                                  self.width_value.get(), self.height_value.get())
            autotyper.getImage()
        except:
            self.error_message = Message(self.root, text= "INVALID BOX DIMENSIONS. TRY AGAIN", font="Verdana", width=600, foreground='red',)
            self.error_message.place(x=450, y=500)
            self.root.update()
            self.button_state('active')
            return -1

        self.load_preview()
        self.run_button.destroy()
        self.keybind_label = Message(self.root, text= f"The Program is Running! Press \"{self.keybind}\" to AutoType! \n           Press \"Escape\" to stop Running.", font="Verdana", width=500)
        self.keybind_label.place(x=410, y=450)
        self.root.update()

        key = self.keybind
        if key in key_dict:
            key = key_dict[key]


        while True:
            self.root.update()
            if keyboard.is_pressed(key):
                self.type_text()
            if keyboard.is_pressed('esc'):
                self.keybind_label.destroy()
                self.run_button = Button(self.root, text='Run Program', font="Verdana", border=5, command=self.run)
                self.run_button.place(x=550, y=450)
                break

        self.root.update()
        self.button_state('active')

    def type_text(self) -> None:
        """Type the text on typeracer out"""
        autotyper = AutoTyper(self.x_value.get(), self.y_value.get(),
                            self.width_value.get(), self.height_value.get())
        autotyper.getImage()
        autotyper.readText()
        print('Typing Now')
        autotyper.type(delay = float(self.delay_value.get()))

    def load_preview(self):
        """Load the Preview onto the window"""
        self.check_error_message()
        self.canvas.delete('all')
        try:
            image = ImageGrab.grab(bbox=(self.x_value.get(), self.y_value.get(),
                                        self.width_value.get() + self.x_value.get(),
                                        self.height_value.get() + self.y_value.get()))

            image.save('image.png')

            image = Image.open('image.png')
            image = image.resize((500, 300), Image.ANTIALIAS)
            screen = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor='nw', image=screen)
            self.canvas.image = screen
            print('Showing Preview Now')

        except: # catches invalid box dimensions
            self.canvas.create_text(250, 150, anchor='center', text='PLEASE ENTER A VALID INPUT FOR THE DIMENSIONS \nOF THE BOX',
                                    fill='red', font="Verdana")

    def update_keybinding(self) -> None:
        """Updates the Keybind"""
        self.check_error_message()
        self.button_state('disabled')
        self.root.update()
        self.temp_label = Message(self.root, text= "Listening... Press The Desired Button", font="Verdana", width=500, fg='red')
        self.temp_label.place(x=465, y=500)
        self.root.bind("<Key>", self._update)

    def _update(self, event):
        """ Secondary function that does all the work"""
        self.root.unbind("<Key>")
        self.temp_label.destroy()
        if event.keysym == 'Escape':
            self.error_message = Message(self.root, text= "Escape isn't a valid input (You need it to quit the program). \n \t  Press the button to try again", font="Verdana", width=600, foreground='red',)
            self.error_message.place(x=380, y=500)
        else:
            self.error_message = Message(self.root, text= "Success!", font="Verdana", width=600, foreground='green',)
            self.error_message.place(x=570, y=500)
            self.keybind = event.keysym

        self.root.update()
        self.button_state('active')

    def check_error_message(self):
        try:
            self.error_message.destroy()
        except:
            pass

    def button_state(self, option: str):
        self.preview_button.config(state=option)
        self.run_button.config(state=option)
        self.change_keybind.config(state=option)


if __name__ == '__main__':
    root = Tk()

    root.resizable(width=False, height=False)
    root.geometry('900x560')
    # constants
    SCREEN_WIDTH = root.winfo_screenwidth()
    SCREEN_HEIGHT = root.winfo_screenheight()

    UserInterface(root, SCREEN_WIDTH, SCREEN_HEIGHT)
    root.mainloop()