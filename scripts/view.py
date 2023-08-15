import flet as ft
import sys

from pytube import YouTube, Playlist, extract
from typing import Any, List, Optional, Union

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

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
        page.window_min_height = 600
        page.window_min_width = 1200

        page_content = [
                            self.link_row,
                            self.loading_ring_row,
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
        self.link_row = ft.Row(
            controls=
                [
                    self.link_input,
                    self.submit_button,
                ],
        )        
        
        
        self.loading_ring_row = ft.Row(
            expand=1,
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=
            [
                ft.ProgressRing(),
            ]
        )
        
        
        self.filepath = ft.TextField(
            label="Введите путь к файлу",
            on_change=self.__link_input_changed,
            value="/home/dannyboy/Documents/Projects/MP3Renamer/"
        )
        self.filename = ft.TextField(
            label="Введите название файла",
            on_change=self.__link_input_changed,
            value="J5EXnh53A1k"
        )
        self.extentions_select = ft.Dropdown(
            label=UIText.download_type_select_label,
            hint_text=UIText.download_type_select_hint,
            options=
            [
                ft.dropdown.Option
                (
                    key=extention,
                    text=extention.upper()
                ) for extention in self.mvc_control.audio_extensions
            ],
        )
        self.file_row = ft.Row(
            controls=
            [
                self.filepath,
                self.filename,
                self.extentions_select,
            ],
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
        self.title_row = ft.Row(
            controls=
                [
                    self.video_title,
                    self.download_type_select,
                ],
        )    
        
        self.video_download_row = ft.Row(
            visible=True,
            controls=
            [
            ],
        )
        
        self.audio_download_row = ft.Row(
            visible=False,
            controls=
            [
            ],
        )
        
        self.download_button = ft.ElevatedButton(
            text=UIText.enter_video_link,
            on_click=self.__download_button_clicked
        )
        
        self.download_widget = ft.Container(
            expand=1,
            visible=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=ft.border_radius.all(10),
            padding=5,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.SURFACE_VARIANT,
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
                            self.title_row,
                            self.file_row,
                            self.video_download_row,
                            self.audio_download_row,
                            ft.Row(
                                controls=
                                [
                                    self.download_button,
                                ],
                            )    
                        ]
                    )
                ]
            )
        )


        self.videos_list = ft.ListView(
            expand=1,
            spacing=10,
        )
        
        ft.app(target=self.main_page, assets_dir="assets")
    
    
    def __link_input_changed(self, e: ft.ControlEvent):
        pass
        
    def __set_loading_ring_visibility(self, value):
        self.loading_ring_row.visible = value
        self.loading_ring_row.update()

    def __submit_button_clicked(self, e: ft.ControlEvent):
        self.__set_loading_ring_visibility(True)

        self.video = self.mvc_control.get_video(self.link_input.value)
        self.download_widget.visible = True
        if self.video:
            self.video_thumbnail.src = self.video.thumbnail_url
            self.video_title.value = self.video.title

        self.__set_loading_ring_visibility(False)
        self.download_widget.update()
        
    def __download_button_clicked(self, e: ft.ControlEvent):
        self.videos_list.controls.append(VideosListItem(self.video))
        self.videos_list.controls.append(ft.Divider())
        self.download_widget.visible = False
        self.videos_list.update()
        self.download_widget.update()

        self.mvc_control.download(self.video)

    def __download_type_changed(self, e: ft.ControlEvent):
        if self.download_type_select.value == "audio":
            self.video_download_row.hidden = True
            self.audio_download_row.hidden = False
        elif self.download_type_select.value == "video":
            self.video_download_row.hidden = False
            self.audio_download_row.hidden = True
  

class VideosListItem(ft.UserControl):
    video: YouTube

    def __init__(self, video: YouTube):
        super().__init__()

        video.register_on_complete_callback(self.__on_download_complete)
        video.register_on_progress_callback(self.__on_download_progress)

        self.thumbnail = ft.Image(
            src=video.thumbnail_url,
            width=128,
            height=72,
            fit=ft.ImageFit.COVER,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(10),
        )
        self.title = ft.Text(
            value=video.title,
        )
        self.progress_bar = ft.ProgressBar(
            value=0,
            width=400,
        )
        self.filesize = ft.Text(
            value="0.0 MB",
        )
        self.playlist = ft.Text(
            value=None,
        )
        self.length = ft.Text(
            value=str(video.length),
        )
        self.internet_speed = ft.Text(
            value="0.0 Mb/sec",
        )
        self.delete_button = ft.IconButton(
            icon=ft.icons.DELETE_FOREVER_ROUNDED,
            icon_color="pink600",
            icon_size=20,
            tooltip="Delete record",
        )
        
        self.download_row = ft.Row(
                                controls=
                                [
                                    self.progress_bar,
                                    self.internet_speed
                                ]
                            )

    def build(self):
        return ft.Row(
                expand=1,
                controls=
                [
                    ft.Column(
                        controls=
                        [
                            self.thumbnail,
                        ]
                    ),
                    ft.Column(
                        controls=
                        [
                            ft.Row(
                                controls=
                                [
                                    self.title,
                                    self.delete_button,
                                ]
                            ),
                            ft.Row(
                                controls=
                                [
                                    self.length,
                                    self.filesize,
                                    self.playlist,
                                ]
                            ),
                            self.download_row
                        ]
                    ),
                ]
        )
    
    def __on_download_progress(self, stream, chunk, bytes_remaining):
        current = (stream.filesize - bytes_remaining) / stream.filesize
        self.progress_bar.value = current
        self.progress_bar.update()
        '''
        global download_start_time
        seconds_since_download_start = (datetime.now()-        download_start_time).total_seconds()    
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        speed = round(((bytes_downloaded / 1024) / 1024) / seconds_since_download_start, 2)    
        seconds_left = round(((bytes_remaining / 1024) / 1024) / float(speed), 2)
        '''
    
    def __update_progress_bar(self):
        pass

    def __on_download_complete(self, stream, path):
        self.download_row.visible = False
        self.download_row.update()