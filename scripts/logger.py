import os
import logging.config


def setup_logger(exec_directory: str, config_file: str):
    root_directory = os.path.dirname(os.path.abspath(exec_directory))
    logs_directory = os.path.join(root_directory, "logs")

    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)
    
    logging.config.fileConfig(config_file, disable_existing_loggers=False)