from scripts.data_classes import *
import flet as ft


def get_params_from_UI():
    file_params = FileParams(
        directory="E:/My Stuff/My Programs/MP3Renamer/songs",
        supported_extensions=[".mp3", ".mp4"],
        rename_files=False
    )

    song_params = SongTags(
        artist="Kensuke Ushio",
        album="Chainsaw Man",
        date="2022",
        genre="Indie",
        albumartist='',
        tracknumber='',
    )

    purification_params = PurificationParams(
        mode=PurificationMode.splitBySymbol,
        split_symbol=" - ",
        split_index=2,
        clutter_indexes=[],
        left_end=0,
        right_end=0
    )

    return file_params, song_params, purification_params


def main_page(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


def run():
    ft.app(target=main_page)
