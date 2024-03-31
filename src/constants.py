"""
Constants:
YEAR, MONTH, DATA_FOLDER, SQL_ROOT_FOLDER, WITH_COMMIT_FOLDER, WITHOUT_COMMIT_FOLDER
"""

from pathlib import Path
import os

YEAR = '2024'
MONTH = '03'
DATA_FOLDER = 'data'
SQL_ROOT_FOLDER = os.path.join(os.getcwd(), 'sql')
WITH_COMMIT_FOLDER = SQL_ROOT_FOLDER + '/' + 'with_commit'
WITHOUT_COMMIT_FOLDER = SQL_ROOT_FOLDER + '/' + 'without_commit'

LOG_CONFIG_PATH = 'log_config.json'

root_folder = os.path.dirname(Path(__file__).resolve().parents[0])
TARGET_PATH = root_folder / Path(DATA_FOLDER) / Path(YEAR + '_' + MONTH)