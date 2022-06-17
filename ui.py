from tkinter import *
from tkinter.ttk import *
from support_funcs import PurificationMode
from tkinter import messagebox
from tkinter import scrolledtext
from os import getcwd


def get_params_from_UI():
    song_dir_name = "E:\My Stuff\My Programs\MP3Renamer\songs"
    supported_extensions = [".mp3"]
    rename_files = False

    artist = "Joe Hisaishi"
    album = "Kiki's Delivery Service"
    date = "1989"
    genre = "Orchestral"
    albumartist = None
    albumartist = None
    tracknum = None

    purification_mode = PurificationMode.none
    split_symbol = "- "
    split_index = 1
    clutter_indexes = None
    left_end = None
    right_end = None

    params = {
        "file_params": {
            "song_directory": song_dir_name,
            "supported_extensions": supported_extensions,
            "rename_files": rename_files,
        },
        "song_params": {
            "artist": artist,
            "album": album,
            "date": date,
            "genre": genre,
            "albumartist": albumartist,
            "tracknumber": tracknum
        },
        "purification_params": {
            "purification_mode": purification_mode,
            "split_symbol": split_symbol,
            "split_index": split_index,
            "clutter_indexes": clutter_indexes,
            "left_end": left_end,
            "right_end": right_end
        }
    }

    return params

class Window():
    def __init__(self, name, resolution, resizable):
        self.name = name
        self.resolution = resolution
        
        ui_factory = UIFactory()
        self.window = ui_factory.window(name, resolution, resizable)
        self.toolbar = ui_factory.toolbar(self.window)
        
        self.window.config(menu=self.toolbar)
        
    def start(self):
        self._setup_layout()
        self.window.mainloop()
    
    def _setup_layout(self):
        ui_factory = UIFactory()
        
        font = ("Arial Bold", 12)
        
        self.selected_purification_mode = IntVar(value=0)
        self.rename_files_bool = BooleanVar(value=True)
        
        file_location_pos = 0
        artist_pos = 1
        album_pos = 2
        year_pos = 3
        genre_pos = 4
        purification_mode_pos = 5
        start_button_pos = 6

        self.song_dir_input = ui_factory.input_box((1, file_location_pos), True, 50, getcwd())
        self.genre_input = ui_factory.input_box((1, genre_pos), True, 50)
        self.artist_input = ui_factory.input_box((1, artist_pos), True, 50)
        self.album_input = ui_factory.input_box((1, album_pos), True, 50)
        self.year_input = ui_factory.input_box((1, year_pos), True, 50)
        
        self.song_dir_desc = ui_factory.label((0, file_location_pos), True,
                                            "Enter the song folder location",
                                            font,
                                            25)
        self.artist_desc = ui_factory.label((0, artist_pos), True,
                                            "Enter the all the album artists",
                                            font,
                                            25)
        self.album_desc = ui_factory.label((0, album_pos), True,
                                            "Enter the all the album names",
                                            font,
                                            25)
        self.year_desc = ui_factory.label((0, year_pos), True,
                                            "Enter the all the album years",
                                            font,
                                            25)
        self.genre_desc = ui_factory.label((0, genre_pos), True,
                                            "Enter the all the album genres",
                                            font,
                                            25)
        
        self.rename_files_check = ui_factory.check_button((2, file_location_pos), True,
                                                        "Rename files to their generated titles",
                                                        self.rename_files_bool)

        self.split_by_symbol_radio = ui_factory.radio_button((0, purification_mode_pos), True,
                                                "Separate the junk with a symbol",
                                                PurificationMode.splitBySymbol, 
                                                self.enable_purification_menu_1,
                                                self.selected_purification_mode)
        self.remove_symbols_at_indexes_radio = ui_factory.radio_button((1, purification_mode_pos), True,
                                                "Remove junk words by index",
                                                PurificationMode.removeSymbolsAtIndexes,
                                                self.selected_purification_mode)
        self.slice_off_ends_radio = ui_factory.radio_button((2, purification_mode_pos), True,
                                                "Slice off words from both ends",
                                                PurificationMode.sliceOffEnds,
                                                self.selected_purification_mode)
        
        self.start_button = ui_factory.button((0, start_button_pos), True,
                                                "Rename files", 
                                                self._finish_input)

    def enable_purification_menu_1(self):
        pass

    def _finish_input(self):
        pass

    def _enable_element(self, element):
        element.pack()
        
    def _disable_element(self, element):
        element.pack_forget()
    
    
class UIFactory():
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

        if not enabled:
            input_box.pack_forget()
        if text != None:
            input_box.insert(0, text)
        if focus:
            input_box.focus()

        return input_box

    def label(self, pos, enabled, text, font, width):
        label = Label(text=text, font=font, justify=LEFT, anchor="w", width=width)
        label.grid(column=pos[0], row=pos[1])

        if not enabled:
            label.pack_forget()
        
        return label

    def button(self, pos, enabled, text, command=None):
        button = Button(text=text, command=command)
        button.grid(column=pos[0], row=pos[1])

        if not enabled:
            button.pack_forget()

        return button
    
    def radio_button(self, pos, enabled, text, value, target_variable, command=None):
        radio_button = Radiobutton(text=text, value=value, command=command, variable=target_variable)
        radio_button.grid(column=pos[0], row=pos[1])
        
        if not enabled:
            radio_button.pack_forget()

        return radio_button
    
    def check_button(self, pos, enabled, text, target_variable, command=None):
        check_button = Checkbutton(text=text, command=command, variable=target_variable)
        check_button.grid(column=pos[0], row=pos[1])

        if not enabled:
            check_button.pack_forget()

        return check_button

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