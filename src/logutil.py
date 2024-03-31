import logging, logging.config
import json

def set_up_root_logger():
    # Create log path
    LOG_CONFIG_PATH = 'log_config.json'

    log_file_path = 'my_log.log'

    # Load the JSON file into a Python object
    with open(LOG_CONFIG_PATH, 'rt') as log_file:
        config = json.load(log_file)
    # Setting the path of the .log file dynamically
    config['handlers']['file']['filename'] = log_file_path
    logging.config.dictConfig(config)
