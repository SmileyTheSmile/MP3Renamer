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
    def __init__(self, name, resolution):
        self.name = name
        self.resolution = resolution
        
        self.window = self._setup_window(name, self.resolution)
        
        self.menu = self._setup_menu(self.window)
        self.window.config(menu=self.menu)
        
    def start(self):
        self._setup_layout()
        self.window.mainloop()


    def _setup_window(self, name, resolution):
        window = Tk()
        window.title(name)
        window.geometry(resolution)
        
        return window
    
    def _setup_menu(self, window):
        menu = Menu(window)

        new_item = Menu(menu, tearoff=0)
        new_item.add_command(label='Новый')
        new_item.add_separator()
        new_item.add_command(label='Изменить')

        menu.add_cascade(label='Файл', menu=new_item)

        return menu
    
    def _setup_layout(self):
        font = ("Arial Bold", 12)
        
        file_location_pos = 0
        artist_pos = 1
        album_pos = 2
        year_pos = 3
        genre_pos = 4
        purification_mode_pos = 5
        start_button_pos = 6
        
        self.song_dir_desc = self._setup_desc((0, file_location_pos),
                                                    "Enter the song folder location",
                                                    font)
        self.song_dir_input = self._setup_input(50,
                                                    (1, file_location_pos),
                                                    getcwd())

        self.rename_files_bool = BooleanVar()
        self.rename_files_bool.set(True)
        self.rename_files_input = Checkbutton(self.window,
                                                text="Rename files to their generated titles",
                                                var=self.rename_files_bool)
        self.rename_files_input.grid(column=2, row=file_location_pos)
        
        self.artist_desc = self._setup_desc((0, artist_pos),
                                            "Enter the all the album artists",
                                            font)
        self.artist_input = self._setup_input(50,
                                            (1, artist_pos))

        self.album_desc = self._setup_desc((0, album_pos),
                                            "Enter the all the album names",
                                            font)
        self.album_input = self._setup_input(50,
                                            (1, album_pos))

        self.year_desc = self._setup_desc((0, year_pos),
                                            "Enter the all the album years",
                                            font)
        self.year_input = self._setup_input(50,
                                            (1, year_pos))

        self.genre_desc = self._setup_desc((0, genre_pos),
                                            "Enter the all the album genres",
                                            font)
        self.genre_input = self._setup_input(50,
                                            (1, genre_pos))

        self.selected_purification_mode = IntVar()
        self.split_by_symbol_radio = Radiobutton(self.window,
                                                text="Separate the junk with a symbol",
                                                value=PurificationMode.splitBySymbol, 
                                                command=self.enable_purification_menu_1,
                                                variable=self.selected_purification_mode)
        self.remove_clutter_radio = Radiobutton(self.window,
                                                text="Remove junk words by index",
                                                value=PurificationMode.removeSymbolsAtIndexes,
                                                variable=self.selected_purification_mode)
        self.slice_off_ends_radio = Radiobutton(self.window,
                                                text="Slice off words from both ends",
                                                value=PurificationMode.sliceOffEnds,
                                                variable=self.selected_purification_mode)
        self.split_by_symbol_radio.grid(column=0, row=purification_mode_pos)
        self.remove_clutter_radio.grid(column=1, row=purification_mode_pos)
        self.slice_off_ends_radio.grid(column=2, row=purification_mode_pos)
    
        self.start_button = Button(self.window, 
                                    text="Rename files", 
                                    command=self.finish_input)
        self.start_button.grid(column=1, row=start_button_pos)
    
    def _setup_input(self, width, pos, text=None, focus=False):
        input = Entry(self.window, width=width)
        input.grid(column=pos[0], row=pos[1])
        
        if text != None:
            input.insert(0, text)
        if focus:
            input.focus()
        
        return input
        
    def _setup_desc(self, pos, text, font):
        desc_label = Label(self.window,
                                text=text,
                                font=font,
                                justify=LEFT,
                                anchor="w",
                                width=25)
        desc_label.grid(column=pos[0], row=pos[1])
        
        return desc_label
    
    def _ignore(self):
        txt2 = Entry(self.window, width=10, state='disabled')

        combo = Combobox(self.window)
        combo['values'] = ("Split off the clutter through a ", 2, 3, 4, 5, "Текст")
        combo.current(1)
        combo.grid(column=0, row=0)


        txt = scrolledtext.ScrolledText(self.window, width=40, height=10)
        txt.grid(column=0, row=0)
        txt.insert(INSERT, 'Текстовое поле')

        messagebox.showinfo('Заголовок', 'Текст')

        messagebox.showwarning('Заголовок', 'Текст')
        messagebox.showerror('Заголовок', 'Текст')

        self.window.mainloop()

    def enable_purification_menu_1(self):
        pass

    def finish_input(self):
        pass

    def get_params_from_UI(self):
        song_dir_name = self.song_dir_input.get()
        rename_files = self.rename_files_bool.get()

        artist = self.artist_input.get()
        album = self.album_input.get()
        year = self.year_input.get()
        genre = self.genre_input.get()
        
        purification_mode = self.selected_purification_mode.get()
        split_symbol = None
        split_index = None
        clutter_indexes = None
        left_end = 1
        right_end = None

        params = {
            "song_dir_name": song_dir_name,
            "rename_files": rename_files,
            "song_params": {
                "artist": artist,
                "album": album,
                "year": year,
                "genre": genre
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
