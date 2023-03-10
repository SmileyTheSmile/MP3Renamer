from scripts.control import MVCControl
from scripts.view import MVCView
from scripts.model import Model

import logging.config


# https://www.pythontutorial.net/tkinter/tkinter-mvc/
def main():
    logging.config.fileConfig('assets/logging.ini', disable_existing_loggers=False)

    model = Model()
    control = MVCControl(model)
    view = MVCView(control)

    view.run()


if __name__ == '__main__':
    main()
