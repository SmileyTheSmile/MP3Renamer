import flet as ft

from scripts.strings import UIText
from scripts.download_widget import DownloadWidget
from scripts.video import Video
from scripts.videos_list_item import VideosListItem
from scripts.control_new import VideoControl


def main_page(page: ft.Page):
    page.title = UIText.app_name
    page.appbar = __appbar()
    page.window_resizable = True
    page.window_min_width = 1200
    page.window_min_height = 600

    page.add(MainPage())
    

def __appbar():
    return ft.AppBar(
        leading=ft.Icon(ft.icons.PALETTE),
        leading_width=40,
        title=ft.Text(UIText.app_name),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=
        [
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.icons.FILTER_3),
            ft.PopupMenuButton(
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
        ],
    )


class MainPage(ft.UserControl):
    video_control = VideoControl()
    
    link_input = ft.Ref[ft.TextField]()
    download_widget = ft.Ref[DownloadWidget]()
    videos_list = ft.Ref[ft.ListView]()
    
    def add_video(self, video: Video):
        self.videos_list.current.controls.append(VideosListItem(video))
        self.videos_list.current.controls.append(ft.Divider())
        self.videos_list.current.update()

        self.video_control.add(video)
        self.video_control.start_download()
    
    def __submit_button_clicked(self, e: ft.ControlEvent):
        self.download_widget.current.set_video(self.link_input.current.value)

    def build(self):
        return ft.Column(
            controls=
            [
                ft.Row(
                    controls=
                    [
                        ft.TextField(
                            expand=1,
                            ref=self.link_input,
                            label=UIText.link_input_text,
                            value="https://youtu.be/J5EXnh53A1k"
                        ),
                        ft.ElevatedButton(
                            text=UIText.enter_video_link,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                            on_click=self.__submit_button_clicked
                        ),
                    ],
                ),
                ft.Row(
                    controls=
                    [
                        DownloadWidget(
                            expand=1,
                            ref=self.download_widget,
                            add_video_to_queue_callback=self.add_video,
                            visible=False,
                        ),
                    ],
                ),
                ft.Row(
                    controls=
                    [
                        ft.ListView(
                            expand=1,
                            ref=self.videos_list,
                            spacing=10,
                        )
                    ],
                )  
            ],
        )
    