"""
Scraper
"""

import json
import string
import os
from pathlib import Path

import requests

import db
import utils
from constants import YEAR, MONTH, DATA_FOLDER, SQL_ROOT_FOLDER, WITH_COMMIT_FOLDER, WITHOUT_COMMIT_FOLDER


def scrape_job_boards(target_path: Path) -> None:
    """
    List through all ats systems from database
    """
    ats_job_board_pairs = select_job_boards_to_scrape()

    for ats_job_board_pair in ats_job_board_pairs:
        ats_id = int(ats_job_board_pair[0])
        ats_name = ats_job_board_pair[1]
        job_board_id = int(ats_job_board_pair[2])
        job_board_name = ats_job_board_pair[3]

        if ats_name == 'greenhouse':
            url = 'https://boards-api.greenhouse.io/v1/boards/' + job_board_name + '/jobs?content=true'
        elif ats_name == 'lever':
            url = 'https://jobs.lever.co/v0/postings/' + job_board_name + '?mode=json'
        else:
            raise ValueError
        json_path = target_path / Path(ats_name) / str(job_board_name + ".json")
        scrape_board_token(url, job_board_name, json_path, ats_id, job_board_id)


def scrape_board_token(url: str, board_token: str, json_path: Path, ats_id: int, job_board_id: int) -> None:
    """
    Scrape a job board (url)
    """
    response = requests.get(url, timeout=15)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Save the JSON data to a file
        with open(json_path, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4)

        print(f'{board_token} saved')
        insert_record_into_scrape_log(ats_id, job_board_id, success_or_fail=1)
    else:
        print(f'{board_token} failed: {response.status_code}')
        insert_record_into_scrape_log(ats_id, job_board_id, success_or_fail=0)


def insert_record_into_scrape_log(ats_id: int, job_board_id: int, success_or_fail: int) -> None:
    """
    Insert a record into scrape log table
    """
    sql = utils.read_sql_file(WITH_COMMIT_FOLDER + '/' + 'insert_scrape_log.sql')
    sql_command = string.Template(sql).substitute(
        year_month=YEAR + '_' + MONTH,
        ats_id=ats_id,
        job_board_id=job_board_id,
        succeeded_or_failed=success_or_fail)
    database = db.Database(SQL_ROOT_FOLDER, WITH_COMMIT_FOLDER, WITHOUT_COMMIT_FOLDER)
    database.execute_sql_command(sql_command, 'with_commit')


def select_job_boards_to_scrape():
    """
    Select only those job boards that have the last log failed or have not been scraped yet
    :return:
    """
    sql = utils.read_sql_file(WITHOUT_COMMIT_FOLDER + '/' + 'select_ats_job_board_to_scrape.sql')
    sql_command = string.Template(sql).substitute(
        year_month=YEAR + '_' + MONTH
    )
    database = db.Database(SQL_ROOT_FOLDER, WITH_COMMIT_FOLDER, WITHOUT_COMMIT_FOLDER)
    return database.execute_sql_command(sql_command, 'without_commit')


def main() -> None:
    """
    Main function
    """
    root_folder = os.path.dirname(Path(__file__).resolve().parents[0])
    target_path = root_folder / Path(DATA_FOLDER) / Path(YEAR + '_' + MONTH)

    scrape_job_boards(target_path)


if __name__ == "__main__":
    main()
