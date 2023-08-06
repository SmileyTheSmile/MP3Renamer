from scripts.control import MVCControl
from scripts.view import MVCView, MVCViewOld
from scripts.model import Model
from scripts.logger import setup_logger

def main():
    """https://www.pythontutorial.net/tkinter/tkinter-mvc/"""

    model = Model()
    control = MVCControl(model)
    view = MVCView(control)

    view.run()


if __name__ == '__main__':
    #setup_logger(__file__, 'assets/logging.ini')
    main()
