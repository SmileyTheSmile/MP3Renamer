import flet as ft
import sys

from typing import List

from scripts.utilities import data_classes as data
from scripts.utilities.strings import UIText

from scripts.control import MVCControl


class MVCView:
    mvc_control: MVCControl
    
    @property
    def appbar(self):
        self.button1 = ft.IconButton(ft.icons.WB_SUNNY_OUTLINED)
        self.button2 = ft.IconButton(ft.icons.FILTER_3)
        self.button3 = ft.PopupMenuButton(
            items=
            [
                ft.PopupMenuItem(text="Item 1"),
                ft.PopupMenuItem(),  # divider
                ft.PopupMenuItem(
                    text="Checked item",
                    checked=False,
                    on_click=lambda _: print("Appbar button pressed.")
                ),
            ]
        )

        return ft.AppBar(
            leading=ft.Icon(ft.icons.PALETTE),
            leading_width=40,
            title=ft.Text(UIText.app_name),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=
            [
                self.button1,
                self.button2,
                self.button3,
            ],
        )

    def main_page(self, page: ft.Page):
        page.title = UIText.app_name
        page.appbar = self.appbar
        page.window_resizable = True

        page_content = [
                            ft.Row(
                                controls=
                                [
                                    self.link_input,
                                    self.submit_button,
                                ]
                            ),
                            self.download_widget,
                            self.videos_list,
                        ]

        page.add(
            ft.Column(
                expand=1,
                controls=page_content,
            )
        )
        
    def __init__(self, control):
        self.mvc_control = control
        self.audio_extensions = ["mp3"]
        self.video_extensions = ["mp4"]
        
        self.videos_list = ft.ListView(
            expand=1,
            spacing=10,
        )
        self.link_input = ft.TextField(
            expand=1,
            label=UIText.link_input_text,
            on_change=self.__link_input_changed,
            value="https://youtu.be/J5EXnh53A1k"
            )
        self.submit_button = ft.ElevatedButton(
            text=UIText.enter_video_link,
            on_click=self.__submit_button_clicked
            )
        self.video_thumbnail = ft.Image(
                    src=None,
                    width=160,
                    height=90,
                    fit=ft.ImageFit.COVER,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                )
        self.video_title = ft.Text(
            value=None,
        )
        self.download_type_select = ft.Dropdown(
                                    value="video",
                                    label=UIText.download_type_select_label,
                                    hint_text=UIText.download_type_select_hint,
                                    options=[ft.dropdown.Option(
                                        key="audio",
                                        text=UIText.audio_download_option_text
                                    ),
                                    ft.dropdown.Option(
                                        key="video",
                                        text=UIText.video_download_option_text
                                    ),],
                                    on_change=self.__download_type_changed,
                                )
        self.audio_extentions_select = ft.Dropdown(
                            label=UIText.download_type_select_label,
                            hint_text=UIText.download_type_select_hint,
                            options=[ft.dropdown.Option(
                                key=extention,
                                text=extention.upper()
                            ) for extention in self.audio_extensions],
                        )
        self.video_download_menu = ft.Row(
                    expand=1,
                    visible=True,
                    controls=
                        [
                        ],
                )
        self.audio_download_menu = ft.Row(
                    expand=1,
                    visible=False,
                    controls=
                        [
                        ],
                )
        self.progress_bar = ft.ProgressBar(
            value=0,
            width=400,
            visible=False,
        )
        self.download_button = ft.ElevatedButton(
            text=UIText.enter_video_link,
            on_click=self.__download_button_clicked
        )
        self.download_widget = ft.Container(
            visible=False,
            expand=1,
            border_radius=ft.border_radius.all(10),
            padding=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_GREY_300,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            ),
            content=ft.Row(
                expand=1,
                controls=
                [
                    ft.Column(
                        controls=
                        [
                            self.video_thumbnail,
                        ]
                    ),
                    ft.Column(
                        controls=
                        [
                            self.video_title,
                            self.download_type_select,
                            self.video_download_menu,
                            self.audio_download_menu,
                            self.progress_bar,
                            self.download_button,
                        ]
                    )
                ]
            )
        )
        
        ft.app(target=self.main_page, assets_dir="assets")

    def __link_input_changed(self, e: ft.ControlEvent):
        pass
        
    def __submit_button_clicked(self, e: ft.ControlEvent):
        self.mvc_control.add_youtube_video(self.link_input.value,
                                        self.__on_download_progress,
                                        self.__on_download_complete)
        self.video = self.mvc_control.videos_queue[-1] 
        
        self.download_widget.visible = True
        self.video_thumbnail.src = self.video.thumbnail_url
        self.video_title.value = self.video.title
        self.download_widget.update()

    def __download_type_changed(self, e: ft.ControlEvent):
        if self.download_type_select.value == "audio":
            self.video_download_menu.hidden = True
            self.audio_download_menu.hidden = False
        elif self.download_type_select.value == "video":
            self.video_download_menu.hidden = False
            self.audio_download_menu.hidden = True
  
    def __download_button_clicked(self, e: ft.ControlEvent):
        self.progress_bar.visible = True
        self.progress_bar.update()
        self.mvc_control.download(self.video)

    def __on_download_progress(self, stream, chunk, bytes_remaining):
        current = (stream.filesize - bytes_remaining) / stream.filesize
        self.progress_bar.value = current
        self.progress_bar.update()

    def __on_download_complete(self, stream, path):
        self.progress_bar.visible = False
        self.progress_bar.update()
        print('Completed:', path)

