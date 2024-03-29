
import json
import os
from pathlib import Path

import requests

import db


def scrape_job_boards(database: db.Database, target_path: str) -> None:
    ats_job_board_pairs = database.execute_sql('select_ats_job_board.sql', 'without_commit')

    for ats_job_board_pair in ats_job_board_pairs:
        ats_id = ats_job_board_pair[0]
        ats_name = ats_job_board_pair[1]
        job_board_id = ats_job_board_pair[2]
        job_board_name = ats_job_board_pair[3]

        if ats_name == 'greenhouse':
            url = 'https://boards-api.greenhouse.io/v1/boards/' + job_board_name + '/jobs?content=true'
        elif ats_name == 'lever':
            url = 'https://jobs.lever.co/v0/postings/' + job_board_name + '?mode=json'
        else:
            raise 'Incorrect name!'
        json_path = target_path / Path(ats_name) / str(job_board_name + ".json")
        scrape_board_token(url, job_board_name, json_path)


def scrape_board_token(url: str, board_token: str, json_path: Path) -> None:
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Save the JSON data to a file
        with open(json_path, "w") as file:
            json.dump(data, file, indent=4)

        print(f'{board_token} saved')
    else:
        print(f'{board_token} failed: {response.status_code}')

#
# def scrape_lever():
#     board_token = 'palantir'
#
#     response = requests.get(url)
#     print(response)
#     if response.status_code == 200:
#         # Parse the JSON response
#         data = response.json()
#         print(data)

def main() -> None:


    YEAR = '2024'
    MONTH = '03'
    DATA_FOLDER = 'files/data'
    SQL_ROOT_FOLDER = os.path.join(os.getcwd(), 'sql')
    WITH_COMMIT_FOLDER = SQL_ROOT_FOLDER + '/' + 'with_commit'
    WITHOUT_COMMIT_FOLDER = SQL_ROOT_FOLDER + '/' + 'without_commit'
    database = db.Database(SQL_ROOT_FOLDER, WITH_COMMIT_FOLDER, WITHOUT_COMMIT_FOLDER)


    root_folder = os.path.dirname(Path(__file__).resolve().parents[0])
    target_path = root_folder / Path(DATA_FOLDER) / Path(YEAR + '_' + MONTH)

    scrape_job_boards(database, target_path)

    #
    # GREENHOUSE = 'greenhouse'
    # GREENHOUSE_BOARD_TOKENS = 'files/master_data/greenhouse_board_tokens.txt'
    # gr_board_tokens = get_board_tokens(root_folder / Path(GREENHOUSE_BOARD_TOKENS))
    # scrape_board_tokens(GREENHOUSE, target_path, gr_board_tokens)
    #
    # LEVER = 'lever'
    # LEVER_BOARD_TOKENS = 'files/master_data/lever_board_tokens.txt'
    # le_board_tokens = get_board_tokens(root_folder / Path(LEVER_BOARD_TOKENS))
    # scrape_board_tokens(LEVER, target_path, le_board_tokens)

if __name__ == "__main__":
    main()

