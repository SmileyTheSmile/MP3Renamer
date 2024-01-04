import flet as ft
  
from scripts.video import VideoInfo, VideoObject


class VideosListItem(ft.UserControl):
    thumbnail = ft.Ref[ft.Image]()
    title = ft.Ref[ft.Text]()
    delete_button = ft.Ref[ft.IconButton]()
    video_length = ft.Ref[ft.Text]()
    filesize = ft.Ref[ft.Text]()
    playlist = ft.Ref[ft.Text]()
    progress_bar = ft.Ref[ft.ProgressBar]()
    download_speed = ft.Ref[ft.Text]()
    download_row = ft.Ref[ft.Row]()
    
    _thumbnail: str = ""

    def __init__(self, thumbnail_url, ):
        super().__init__()
        
        self._thumbnail = self.video.thumbnail_url
        
        self.video.add_download_progress_callback(self.__on_download_progress)
        self.video.add_download_complete_callback(self.__on_download_complete)
        
    def on_download_progress(self,
            progress: float,
            speed: float,
            seconds_left: float,
        ):
        self.progress_bar.current.value = progress
        self.download_speed.current.value = f"{speed:.2f} Mb/sec, {seconds_left:.2f} сек. осталось"
        self.progress_bar.current.update()
        self.download_speed.current.update()
    
    def on_download_complete(self):
        self.progress_bar.current.bgcolor = self.progress_bar.current.color
        self.progress_bar.current.color = (0, 255, 0)
        self.progress_bar.current.value = 0
        self.progress_bar.current.update()
        self.download_row.current.visible = False
        self.download_row.current.update()
        
    def on_conversion_progress(self, progress: float):
        self.progress_bar.current.value = progress
        self.progress_bar.current.update()
        
    def on_conversion_complete(self):
        self.download_row.current.visible = False
        self.download_row.current.update()

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
                                    value="{}:{}:{}".format(*self.video.formatted_length),
                                ),
                                ft.Text(
                                    ref=self.filesize,
                                    value=f"{self.video.filesize_MB:.2f} MB",
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
                                    value=f"0.00 Mb/sec",
                                )
                            ]
                        )
                    ]
                ),
            ]
        )
    