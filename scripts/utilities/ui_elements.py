import flet as ft

from scripts.utilities.strings import UIText


class VideosList(ft.UserControl):
    def __init__(self):
        super().__init__()
        
        self.videos_list = ft.ListView(
            expand=True,
            spacing=10,
            )
        
        self.link_input = ft.TextField(
            label="Textbox with 'change' event:",
            on_change=self.__link_input_changed,
        )
        
    def __link_input_changed(self, e: ft.ControlEvent):
        pass
        
    def build(self):
        self.expand=True
        
        return ft.Column(
            expand=1,
            controls=
            [
                self.link_input,
                self.videos_list,
            ]
        )

def get_url_input_popup(on_click, on_dismiss):
    return ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text("This is sheet's content!"),
                    ft.ElevatedButton("Close bottom sheet", on_click=on_click),
                ],
                tight=True,
            ),
            padding=10,
        ),
        open=True,
        on_dismiss=on_dismiss,
    )

def get_appbar():
    button1 = ft.IconButton(ft.icons.WB_SUNNY_OUTLINED)
    button2 = ft.IconButton(ft.icons.FILTER_3)
    button3 = ft.PopupMenuButton(
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
            button1,
            button2,
            button3,
        ],
    )

def get_file_picker(on_result, allowed_extensions, initial_directory):
    file_picker = ft.FilePicker(on_result=on_result)
    file_picker.allow_multiple = True
    file_picker.allowed_extensions = allowed_extensions
    file_picker.initial_directory = initial_directory
    return file_picker

def get_side_menu(on_destination_picker_click=None,
                  on_rail_change=None):

    destination_picker_button = ft.FloatingActionButton(
        text=UIText.open_folder_button,
        icon=ft.icons.UPLOAD_FILE,
        on_click=on_destination_picker_click,
    )
    return ft.Container(
        border=ft.border.all(3, ft.colors.SECONDARY),
        border_radius=5,
        content=ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            expand=True,
            min_extended_width=400,
            leading=destination_picker_button,
            group_alignment=-0.8,
            destinations=
            [
                ft.NavigationRailDestination(
                    icon=ft.icons.FAVORITE_BORDER,
                    selected_icon=ft.icons.FAVORITE,
                    label="First",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.BOOKMARK_BORDER,
                    # icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                    selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                    label="Second",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                    label_content=ft.Text("Settings"),
                ),
            ],
            on_change=on_rail_change,
        )
    )

class WorkingArea(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.list_header = ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )
        self.files_table = ft.DataTable(
            border=ft.border.all(2, ft.colors.BLACK),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.colors.BLACK38),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.BLACK12),
            heading_row_color=ft.colors.BLACK12,
        )
        self.table_area = ft.Row(
            spacing=10,
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=
            [
                ft.Column(
                    scroll=ft.ScrollMode.ALWAYS,
                    controls=
                    [
                        self.files_table
                    ]
                )
            ],
        )

    def build(self):
        self.expand=True
        return ft.Column(
            expand=1,
            controls=
            [
                ft.Container(
                    border=ft.border.all(3, ft.colors.SECONDARY),
                    border_radius=5,
                    expand=1,
                    content=self.list_header
                ),
                ft.Container(
                    border=ft.border.all(3, ft.colors.SECONDARY),
                    border_radius=5,
                    expand=9,
                    content=self.table_area,
                )
            ]
        )

    def add_headers(self, headers):
        for header in headers:
            text_object = ft.Text(header)
            self.list_header.controls.append(text_object)
            self.files_table.columns.append(ft.DataColumn(text_object))

    def clear_headers(self):
        self.list_header.controls.clear()
        self.files_table.columns.clear()

    def set_headers(self, headers):
        self.clear_headers()
        self.add_headers(headers)

    def update_table(self):
        self.files_table.rows = get_rows(len(self.files_table.columns))
        self.update()


def get_cells(headers_num):
    return [ft.DataCell(ft.Text("John")) for _ in range(headers_num)]

def get_rows(headers_num):
    return [ft.DataRow(cells=get_cells(headers_num)) for _ in range(40)]