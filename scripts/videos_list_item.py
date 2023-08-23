import flet as ft
  
from scripts.video import Video


class VideosListItem(ft.UserControl):
    video: Video
    
    thumbnail = ft.Ref[ft.Image]()
    title = ft.Ref[ft.Text]()
    delete_button = ft.Ref[ft.IconButton]()
    video_length = ft.Ref[ft.Text]()
    filesize = ft.Ref[ft.Text]()
    playlist = ft.Ref[ft.Text]()
    progress_bar = ft.Ref[ft.ProgressBar]()
    download_speed = ft.Ref[ft.Text]()
    download_row = ft.Ref[ft.Row]()

    def __init__(self, video: Video):
        super().__init__()
        
        self.video = video
        self.video.add_download_progress_callback(self.__on_download_progress)
        self.video.add_download_complete_callback(self.__on_download_complete)
        
    def __on_download_progress(self, progress: float):
        self.progress_bar.current.value = progress
        self.progress_bar.current.update()
    
    def __on_download_complete(self):
        self.progress_bar.current.bgcolor = self.progress_bar.current.color
        self.progress_bar.current.color = (0, 255, 0)
        self.progress_bar.current.value = 0
        self.progress_bar.current.update()
        
    def __on_conversion_progress(self, progress: float):
        self.progress_bar.value = progress
        self.progress_bar.update()
        
    def __on_conversion_complete(self):
        self.download_row.visible = False
        self.download_row.update()

    def build(self):
        return ft.Row(
            expand=1,
            controls=
            [
                ft.Column(
                    controls=
                    [
                        ft.Image(
                            ref=self.thumbnail,
                            src=self.video.thumbnail_url,
                            width=128,
                            height=72,
                            fit=ft.ImageFit.COVER,
                            repeat=ft.ImageRepeat.NO_REPEAT,
                            border_radius=ft.border_radius.all(10),
                        ),
                    ]
                ),
                ft.Column(
                    controls=
                    [
                        ft.Row(
                            controls=
                            [
                                ft.Text(
                                    ref=self.title,
                                    value=self.video.title,
                                ),
                                ft.IconButton(
                                    ref=self.delete_button,
                                    icon=ft.icons.DELETE_FOREVER_ROUNDED,
                                    icon_color="pink600",
                                    icon_size=20,
                                    tooltip="Delete record",
                                ),
                            ]
                        ),
                        ft.Row(
                            controls=
                            [
                                ft.Text(
                                    ref=self.video_length,
                                    value=self.video.formatted_length,
                                ),
                                ft.Text(
                                    ref=self.filesize,
                                    value=self.video.formatted_filesize,
                                ),
                            ]
                        ),
                        ft.Row(
                            ref=self.download_row,
                            controls=
                            [
                                ft.ProgressBar(
                                    ref=self.progress_bar,
                                    value=0,
                                    width=400,
                                ),
                                ft.Text(
                                    ref=self.download_speed,
                                    value=self.video.formatted_current_download_speed,
                                )
                            ]
                        )
                    ]
                ),
            ]
        )
    