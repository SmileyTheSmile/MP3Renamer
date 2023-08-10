import flet as ft

from typing import List

from scripts.utilities import data_classes as data
from scripts.utilities.strings import UIText

from scripts.control import MVCControl

class MVCView:
    mvc_control: MVCControl
    
    def main_page(self, page: ft.Page):
        page.title = UIText.app_name
        page.appbar = self.appbar
        page.window_resizable = True

        page_content = [
                            self.link_input_row,
                            self.download_widget,
                            self.videos_list,
                        ]

        page.add(
            ft.Column(
                expand=1,
                controls=page_content,
            )
        )
        
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
        
    @property
    def link_input_row(self):
        return ft.Row(
            controls=
            [
                self.link_input,
                self.submit_button,
            ]
        )
    
    
    def __init__(self, control):
        self.mvc_control = control
        
        self.videos_list = ft.ListView(
            expand=1,
            spacing=10,
        )
        self.link_input = ft.TextField(
            expand=1,
            label=UIText.link_input_text,
            on_change=self.__link_input_changed,
            value="https://www.youtube.com/watch?v=HyhDzkVsLwc&list=PL924DFB59EB36FA1A&index=31"
            )
        self.submit_button = ft.ElevatedButton(
            text=UIText.enter_video_link,
            on_click=self.__submit_button_clicked
            )
        
        self.download_widget = DownloadWidget(["mp3"], ["mp4"])
        
        ft.app(target=self.main_page, assets_dir="assets")

    def __link_input_changed(self, e: ft.ControlEvent):
        pass
    
    def __update_videos_list(self, e: ft.ControlEvent):
        for video in self.mvc_control.videos_queue:
            self.videos_list.controls.append(VideoListItem(video, ["mp4", "mp3"]))
            self.videos_list.controls.append(ft.Divider())
        self.videos_list.update()
        
    def __submit_button_clicked(self, e: ft.ControlEvent):
        self.mvc_control.add_youtube_video(self.link_input.value)
        video = self.mvc_control.videos_queue[-1]
        self.download_widget.disabled = False
        self.download_widget.visible = True
        self.download_widget.set_video(video)


class DownloadWidget(ft.UserControl):
    def __init__(self, audio_extensions: List[str], video_extensions: List[str]):
        super().__init__()
        self.audio_extensions = audio_extensions
        self.video_extensions = video_extensions
        
        self.download_type_select = ft.Dropdown(
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
        
        self.video_download_menu = ft.Row(
                    expand=1,
                    disabled=False,
                    visible=True,
                    controls=
                        [
                        ],
                )
        
        self.music_download_menu = ft.Row(
                    expand=1,
                    disabled=True,
                    visible=False,
                    controls=
                        [
                        ],
                )
        self.raw_layout = ft.Row(
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
                        self.music_download_menu,
                    ]
                )
            ]
        )
        self.layout = ft.Container(
            content=self.raw_layout,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_GREY_300,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            )
        )
        
    def build(self):
        self.expand = True
        self.disabled = True
        self.visible = False
        
        return self.layout
    
    def set_video(self, video):
        self.video = video 
        self.video_thumbnail.src = self.video.thumbnail_url
        self.video_title.value = self.video.title
        self.update()
        
    def __download_type_changed(self, e: ft.ControlEvent):
        if self.download_type_select.value == "music":
            self.video_download_menu.disabled = True
            self.music_download_menu.disabled = False
        elif self.download_type_select.value == "video":
            self.video_download_menu.disabled = False
            self.music_download_menu.disabled = True


class VideoListItem(ft.UserControl):
    def __init__(self, video, possible_extensions: List[str]):
        super().__init__()
        self.video = video
        
        self.selected_extension = ft.Dropdown(
                                    label="Color",
                                    hint_text="Choose your favourite color?",
                                    width=100,
                                    options=[ft.dropdown.Option(option) for option in possible_extensions],
                                )
        
        self.layout = ft.Row(
            expand=1,
            controls=
            [
                ft.Image(
                    src=self.video.thumbnail_url,
                    width=160,
                    height=90,
                    fit=ft.ImageFit.COVER,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                ),
                ft.Column(
                    expand=1,
                    controls=
                        [
                            ft.Text(self.video.title),
                            self.selected_extension,
                        ]
                ),
            ]
        )
        
    def build(self):
        self.expand=True
        return self.layout

