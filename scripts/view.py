import flet as ft
import flet.colors as colors

from scripts.utilities import data_classes as data
from scripts.utilities import ui_elements as ui_elems
from scripts.utilities.strings import UIText

from scripts.control import MVCControl


class MVCView:
    mvc_control: MVCControl

    def __init__(self, control):
        self.mvc_control = control

        self.file_picker = ui_elems.get_file_picker(
            self.update_files,
            self.mvc_control.settings.allowed_extensions,
            self.mvc_control.settings.initial_directory
        )
        self.appbar = ui_elems.get_appbar()
        self.side_menu = ui_elems.get_side_menu(
            on_destination_picker_click=self.destination_picker_button_clicked,
            on_rail_change=self.rail_destination_changed,
        )
        self.working_area = ui_elems.WorkingArea()

    def run(self):
        ft.app(target=self.main_page, assets_dir="assets")

    def main_page(self, page: ft.Page):
        page.title = UIText.app_name
        page.overlay.append(self.file_picker)
        page.appbar = self.appbar

        page_content = [
                            self.side_menu,
                            self.working_area
                        ]

        self.working_area.add_headers(UIText.table_header_names.values())

        page.add(
            ft.Row(
                expand=1,
                controls=page_content,
            )
        )

    def destination_picker_button_clicked(self, e: ft.ControlEvent):
        self.file_picker.get_directory_path(
            dialog_title=UIText.file_picker_dialog
        )

    def update_files(self, e: ft.FilePickerResultEvent):
        if e.path is not None:
            self.mvc_control.update_files(e.path)
            self.working_area.update_table()

    def check_item_clicked(self, e):
        pass

    def rail_destination_changed(self, e: ft.ControlEvent):
        print("Selected destination:", e.control.selected_index)
