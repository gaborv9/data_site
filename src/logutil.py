"""
Logging config
"""
import json
import logging
import logging.config
from constants import LOG_CONFIG_PATH


def set_up_root_logger() -> None:
    """
    Set up logger
    """
    # Create log path
    log_file_path = 'my_log.log'

    # Load the JSON file into a Python object
    with open(LOG_CONFIG_PATH, 'rt', encoding='utf-8') as log_file:
        config = json.load(log_file)
    # Setting the path of the .log file dynamically
    config['handlers']['file']['filename'] = log_file_path
    logging.config.dictConfig(config)
