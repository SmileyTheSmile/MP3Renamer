import flet as ft
from typing import Callable

from scripts.strings import UIText
from scripts.video import VideoInfo, VideoObject


class VideoParametersMenu(ft.UserControl):
    video = VideoInfo()
    
    on_download_callback: Callable
        
    page_padding = 10
    thumbnail_width = 160
    thumbnail_height = 90
    
    video_thumbnail = ft.Ref[ft.Image]()
    video_title = ft.Ref[ft.Text]()
    filepath = ft.Ref[ft.TextField]()
    filename = ft.Ref[ft.TextField]()
    extension = ft.Ref[ft.Dropdown]()
    download_button = ft.Ref[ft.ElevatedButton]()
    streams = ft.Ref[ft.Dropdown]()
    errors_row = ft.Ref[ft.Row]()
    error_display = ft.Ref[ft.Text]()
    
    loading_ring_row = ft.Ref[ft.Row]()
    controls_row = ft.Ref[ft.Row]()
    video_download_row = ft.Ref[ft.Row]()
    audio_download_row = ft.Ref[ft.Row]()
    
    def __init__(self, add_video_to_queue_callback, *args, **kwargs):
        super(VideoParametersMenu, self).__init__(*args, **kwargs)
        self.on_download_callback = add_video_to_queue_callback
                
    def set_video(self, url: str):
        self.loading_ring_row.current.visible = True
        self.controls_row.current.visible = False
        self.visible = True
        self.update()
        
        if self.video.connect(url):
            self.video_thumbnail.current.src = self.video.thumbnail_url
            self.video_title.current.value = self.video.title
            self.filename.current.value = self.video.title
            self.extension.current.options = [
                ft.dropdown.Option
                (
                    key=extention,
                    text=extention.upper()
                )
                for extention in self.video.available_extensions
            ]
            self.controls_row.current.visible = True
            self.errors_row.current.visible = False
        else:
            self.error_display.current.value = UIText.connection_failed
            self.errors_row.current.visible = True
            self.controls_row.current.visible = False
        
        self.loading_ring_row.current.visible = False
        self.update()
    
    def __download_button_clicked(self, e: ft.ControlEvent):
        self.visible = False
        self.update()
        
        self.__set_video_attributes()
        self.on_download_callback(self.video.get_stream())
        
    def __set_video_attributes(self):
        self.video.filename = self.filename.current.value
        self.video.filepath = self.filepath.current.value
        
    def __stream_changed(self, e: ft.ControlEvent):
        pass

    def __extension_changed(self, e: ft.ControlEvent):
        if self.extension.current.value in self.video.video_extensions:
            self.video_download_row.current.visible = True
            self.audio_download_row.current.visible = False
        elif self.extension.current.value in self.video.audio_extensions:
            self.video_download_row.current.visible = False
            self.audio_download_row.current.visible = True
  
    def __filepath_changed(self, value):
        pass
        
    def __filename_changed(self, value):
        pass
           
    def build(self):
        return ft.Container(
            expand=1,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=ft.border_radius.all(self.page_padding),
            padding=self.page_padding,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.SURFACE_VARIANT,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            ),
            content=ft.Column(
                expand=1,
                spacing=self.page_padding,
                controls=
                [       
                    ft.Row(
                        ref=self.loading_ring_row,
                        visible=True,
                        height=120,
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=
                        [
                            ft.ProgressRing(),
                        ]
                    ),
                    ft.Row(
                        ref=self.errors_row,
                        visible=False,
                        controls=
                        [
                            ft.Text(
                                ref=self.error_display,
                                value=None,
                                color=ft.colors.RED_100,
                            ),
                        ],
                    ),
                    ft.Row(
                        ref=self.controls_row,
                        visible=False,
                        controls=
                        [
                            ft.Column(
                                width=self.thumbnail_width + self.page_padding * 2,
                                spacing=self.page_padding * 2,
                                alignment=ft.MainAxisAlignment.START,
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
                                                size=20,
                                            ),
                                        ]
                                    ),
                                    ft.Row(
                                        controls=
                                        [
                                            ft.TextField(
                                                expand=1,
                                                ref=self.filepath,
                                                label="Введите путь к файлу",
                                                on_change=self.__filepath_changed,
                                                value="/home/dannyboy/Documents/Projects/MP3Renamer/downloads"
                                            ),
                                            ft.TextField(
                                                expand=1,
                                                ref=self.filename,
                                                label="Введите название файла",
                                                on_change=self.__filename_changed,
                                            ),
                                            ft.Dropdown(
                                                width=160,
                                                ref=self.extension,
                                                label=UIText.download_type_select_label,
                                                hint_text=UIText.download_type_select_hint,
                                                on_change=self.__extension_changed,
                                            )
                                        ],
                                    ),
                                    ft.Row(
                                        ref=self.video_download_row,
                                        visible=True,
                                        controls=
                                        [
                                            ft.Dropdown(
                                                width=160,
                                                ref=self.streams,
                                                label=UIText.stream_select_label,
                                                hint_text=UIText.stream_select_hint,
                                                on_change=self.__stream_changed,
                                            )
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
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=10),
                                                ),
                                                height=60,
                                                text=UIText.enter_video_link,
                                                on_click=self.__download_button_clicked
                                            ),
                                        ],
                                    )    
                                ]
                            ),
                        ],
                    ),
                ]
            ),
        )