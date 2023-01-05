from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import scrolledtext
    
    
class UIFactory():
    """Wrapper class for making tkinter UI elements, because the default class inits there suck."""
    
    
    def __set_enabled__(self, enabled, item):
        if not enabled:
            item.pack_forget()
    
    
    def window(self, name, resolution, resizable):
        window = Tk()
        window.title(name)
        window.geometry(resolution)
        window.resizable(width=resizable, height=resizable)

        return window
    
    
    def toolbar(self, window):
        toolbar = Menu(window)
        new_item = Menu(toolbar, tearoff=0)
        new_item.add_command(label='Новый')
        new_item.add_separator()
        new_item.add_command(label='Изменить')

        toolbar.add_cascade(label='Файл', menu=new_item)
        
        return toolbar
    
    
    def input_box(self, pos, enabled, width, text=None, focus=False):
        input_box = Entry(width=width)
        input_box.grid(column=pos[0], row=pos[1])

        self.__set_enabled__(enabled, input_box)
            
        if text != None:
            input_box.insert(0, text)
        if focus:
            input_box.focus()

        return input_box


    def label(self, pos, enabled, text, font, width):
        label = Label(text=text, font=font, justify=LEFT, anchor="w", width=width)
        label.grid(column=pos[0], row=pos[1])

        self.__set_enabled__(enabled, label)
        
        return label


    def button(self, pos, enabled, text, command=None):
        button = Button(text=text, command=command)
        button.grid(column=pos[0], row=pos[1])

        self.__set_enabled__(enabled, button)

        return button
    
    
    def radio_button(self, pos, enabled, text, value, target_variable, command=None):
        radio_button = Radiobutton(text=text, value=value, command=command, variable=target_variable)
        radio_button.grid(column=pos[0], row=pos[1])
        
        self.__set_enabled__(enabled, radio_button)

        return radio_button
    
    
    def check_button(self, pos, enabled, text, target_variable, command=None):
        check_button = Checkbutton(text=text, command=command, variable=target_variable)
        check_button.grid(column=pos[0], row=pos[1])

        self.__set_enabled__(enabled, check_button)

        return check_button
    
    
    def int_var(self, value):
        return IntVar(value=value)


    def bool_var(self, value):
        return BooleanVar(value=value)


    def _unused_stuff(self):
        txt2 = Entry(self.window, width=10, state='disabled')

        combo = Combobox(self.window)
        combo['values'] = (
            "Split off the clutter through a ", 2, 3, 4, 5, "Текст")
        combo.current(1)
        combo.grid(column=0, row=0)

        txt = scrolledtext.ScrolledText(self.window, width=40, height=10)
        txt.grid(column=0, row=0)
        txt.insert(INSERT, 'Текстовое поле')

        messagebox.showinfo('Заголовок', 'Текст')

        messagebox.showwarning('Заголовок', 'Текст')
        messagebox.showerror('Заголовок', 'Текст')