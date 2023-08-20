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
    
    def main_page(self, page: ft.Page):
        page.title = UIText.app_name
        page.appbar = self.appbar
        page.window_resizable = True
        page.window_min_height = 600
        page.window_min_width = 1200

        page.add(
            ft.Column(
                expand=1,
                controls=
                [
                    ft.Row(
                        controls=
                        [
                            self.link_input,
                            self.submit_button,
                        ],
                    ),
                    self.loading_ring_row,
                    self.download_widget,
                    self.videos_list,
                ],
            )
        )
        
    def __init__(self, control):
        self.mvc_control = control
        
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
        
        self.appbar = ft.AppBar(
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
        self.videos_list = ft.ListView(
            expand=1,
            spacing=10,
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
        
        self.download_widget = DownloadWidget(self, self.mvc_control)
        
        ft.app(target=self.main_page, assets_dir="assets")
    
    def __link_input_changed(self, e: ft.ControlEvent):
        pass
        
    def __submit_button_clicked(self, e: ft.ControlEvent):
        self.loading_ring_row.visible = True
        self.loading_ring_row.update()
        
        self.download_widget.set_video(self.link_input.value)
        
        self.loading_ring_row.visible = False
        self.loading_ring_row.update()
        self.download_widget.visible = True
        self.download_widget.update()
        
  
class DownloadWidget(ft.UserControl):
    mvc_control: MVCControl
    video: YouTube
    
    parent: ft.UserControl
        
    page_padding = 5
    thumbnail_width = 160
    thumbnail_height = 90
    
    video_thumbnail = ft.Ref[ft.Image]()
    download_type_select = ft.Ref[ft.Dropdown]()
    video_title = ft.Ref[ft.Text]()
    filepath = ft.Ref[ft.TextField]()
    filename = ft.Ref[ft.TextField]()
    extention = ft.Ref[ft.Dropdown]()
    download_button = ft.Ref[ft.ElevatedButton]()
    video_download_row = ft.Ref[ft.Row]()
    audio_download_row = ft.Ref[ft.Row]()
    
    def __init__(self, parent: ft.UserControl, control: MVCControl):
        super().__init__()
        
        self.parent = parent
        self.mvc_control = control
        
        self.visible = False
        
    def set_video(self, link: str):
        self.video = self.mvc_control.get_video(link)
        
        if self.video:
            self.video_thumbnail.current.src = self.video.thumbnail_url
            self.video_title.current.value = self.video.title
            self.filename.current.value = self.video.title
        1
    
    def build(self):
        return ft.Container(
            expand=1,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=ft.border_radius.all(self.page_padding * 2),
            padding=self.page_padding,
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
                        width=self.thumbnail_width + self.page_padding * 2,
                        controls=
                        [
                            ft.Image(
                                ref=self.video_thumbnail,
                                src=None,
                                width=self.thumbnail_width,
                                height=self.thumbnail_height,
                                fit=ft.ImageFit.COVER,
                                repeat=ft.ImageRepeat.NO_REPEAT,
                                border_radius=ft.border_radius.all(10),
                            ),
                            ft.Dropdown(
                                ref=self.download_type_select,
                                width=self.thumbnail_width,
                                value="video",
                                label=UIText.download_type_select_label,
                                hint_text=UIText.download_type_select_hint,
                                options=
                                [
                                    ft.dropdown.Option(
                                    key="audio",
                                    text=UIText.audio_download_option_text
                                    ),
                                    ft.dropdown.Option(
                                        key="video",
                                        text=UIText.video_download_option_text
                                    )
                                ],
                                on_change=self.__download_type_changed,
                            ),
                        ]
                    ),
                    ft.Column(
                        expand=1,
                        controls=
                        [
                            ft.Row(
                                controls=
                                [
                                    ft.Text(
                                        ref=self.video_title,
                                        value=None,
                                    ),
                                ],
                            ),
                            ft.Row(
                                controls=
                                [
                                    ft.TextField(
                                        ref=self.filepath,
                                        expand=2,
                                        label="Введите путь к файлу",
                                        on_change=self.__filepath_changed,
                                        value=None
                                    ),
                                    ft.TextField(
                                        ref=self.filename,
                                        expand=1,
                                        label="Введите название файла",
                                        on_change=self.__filename_changed,
                                        value=None
                                    ),
                                    ft.Dropdown(
                                        ref=self.extention,
                                        width=160,
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
                                ],
                            ),
                            ft.Row(
                                ref=self.video_download_row,
                                visible=True,
                                controls=
                                [
                                ],
                            ),
                            ft.Row(
                                ref=self.audio_download_row,
                                visible=False,
                                controls=
                                [
                                ],
                            ),
                            ft.Row(
                                controls=
                                [
                                    ft.ElevatedButton(
                                        ref=self.download_button,
                                        text=UIText.enter_video_link,
                                        on_click=self.__download_button_clicked
                                    ),
                                ],
                            )    
                        ]
                    )
                ]
            ),
        )
    
    def __download_button_clicked(self, e: ft.ControlEvent):
        self.parent.videos_list.controls.append(VideosListItem(self.video))
        self.parent.videos_list.controls.append(ft.Divider())
        self.parent.videos_list.update()
        
        self.visible = False
        self.update()

        self.mvc_control.download(self.video)

    def __download_type_changed(self, e: ft.ControlEvent):
        if self.download_type_select.current.value == "audio":
            self.video_download_row.current.hidden = True
            self.audio_download_row.current.hidden = False
        elif self.download_type_select.current.value == "video":
            self.video_download_row.current.hidden = False
            self.audio_download_row.current.hidden = True
  
    def __filepath_changed(self, value):
        pass
        
    def __filename_changed(self, value):
        pass


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
            value=str(video.length) + UIText.seconds,
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
    
    def __on_download_complete(self, stream, path):
        self.progress_bar.bgcolor = self.progress_bar.color
        self.progress_bar.color = (0, 255, 0)
        self.progress_bar.value = 0
        self.progress_bar.update()
        
    def __on_conversion_progress(self, progress: float):
        self.progress_bar.value = progress
        self.progress_bar.update()
        
    def __on_conversion_complete(self):
        self.download_row.visible = False
        self.download_row.update()