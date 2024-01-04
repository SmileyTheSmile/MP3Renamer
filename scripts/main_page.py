import flet as ft

from scripts.strings import UIText
from scripts.download_widget import VideoParametersMenu
from scripts.video import VideoInfo, VideoObject
from scripts.videos_list_item import VideosListItem
from scripts.control_new import VideosList


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
    link = ft.Ref[ft.TextField]()
    download_widget = ft.Ref[VideoParametersMenu]()
    videos_list = ft.Ref[VideosList]()
    
    def __add_video(self, video: VideoObject):
        self.videos_list.current.add(video)
    
    def __submit_button_clicked(self, e: ft.ControlEvent):
        self.download_widget.current.set_video(self.link.current.value)

    def build(self):
        return ft.Column(
            controls=
            [
                ft.Row(
                    controls=
                    [
                        ft.TextField(
                            expand=1,
                            ref=self.link,
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
                        VideoParametersMenu(
                            expand=1,
                            ref=self.download_widget,
                            add_video_to_queue_callback=self.__add_video,
                            visible=False,
                        ),
                    ],
                ),
                ft.Row(
                    controls=
                    [
                        VideosList(
                            expand=1,
                            ref=self.videos_list,
                            spacing=10,
                        )
                    ],
                )  
            ],
        )
    