import colorlog

from scripts.utilities import file_operations as f_ops
from scripts.utilities import data_classes as data


logger = colorlog.getLogger(__name__)


class Model:
    def __init__(self):
        self.files = None
        self.settings = None

    def update_files(self, directory):
        filenames = f_ops.load_files(directory)
        logger.info(f"Loaded all files in {directory}.")
        self.files = f_ops.convert_to_file_info(directory, filenames)
        #logger.debug(self.files)

    def update_supported_files(self, directory, extensions):
        filenames = f_ops.load_supported_files(directory, extensions)
        logger.info(f"Loaded all <{', '.join(extensions)}> files in {directory}.")
        self.files = f_ops.convert_to_file_info(directory, filenames)
        logger.debug(self.files)

    def update_settings(self, settings):
        self.settings = settings
        logger.info(f"Updated settings.")

    def load_settings(self):
        # TODO Add the ability to save settings in a JSON file
        self.settings = data.Settings()
        logger.info(f"Loaded settings.")
