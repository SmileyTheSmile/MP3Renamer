from scripts import ui
from scripts import business_logic
import logging.config


def main():
    logging.config.fileConfig('resources/logging.ini', disable_existing_loggers=False)
    bl = business_logic.BusinessLogic(*ui.get_params_from_UI())
    #ui.run()


if __name__ == '__main__':
    main()
