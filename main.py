import flet as ft

from scripts.logger import setup_logger
from scripts.main_page import main_page


if __name__ == '__main__':
    setup_logger(__file__, 'assets/logging.ini')
    ft.app(target=main_page, assets_dir="assets")
