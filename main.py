from scripts.model import MVCModel
from scripts.control import MVCControl
from scripts.view import MVCView
from scripts.logger import setup_logger

def main():
    """https://www.pythontutorial.net/tkinter/tkinter-mvc/"""

    model = MVCModel()
    control = MVCControl(model)
    view = MVCView(control)


if __name__ == '__main__':
    setup_logger(__file__, 'assets/logging.ini')
    main()
