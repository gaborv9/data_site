"""
Constants:
YEAR, MONTH, DATA_FOLDER, SQL_ROOT_FOLDER, WITH_COMMIT_FOLDER, WITHOUT_COMMIT_FOLDER
"""

import os

YEAR = '2024'
MONTH = '03'
DATA_FOLDER = 'files/data'
SQL_ROOT_FOLDER = os.path.join(os.getcwd(), 'sql')
WITH_COMMIT_FOLDER = SQL_ROOT_FOLDER + '/' + 'with_commit'
WITHOUT_COMMIT_FOLDER = SQL_ROOT_FOLDER + '/' + 'without_commit'
