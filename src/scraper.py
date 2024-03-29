
import requests
import json
import os
from pathlib import Path




def get_board_tokens(all_tokens_file_path: Path) -> list:
    with open(all_tokens_file_path, "r") as file:
        tokens = file.readlines()
    tokens = [line.strip() for line in tokens]
    return tokens


def scrape_greenhouse_boards(target_path: Path, board_tokens: list) -> None:
    for board_token in board_tokens:
        scrape_greenhouse_board(target_path, board_token)

def scrape_greenhouse_board(target_path: Path, board_token: str) -> None:
    NAME = 'greenhouse'
    url = 'https://boards-api.greenhouse.io/v1/boards/' + board_token + '/jobs?content=true'
    response = requests.get(url)
    save_path = target_path / Path(NAME) / str(board_token + ".json")
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Save the JSON data to a file
        with open(save_path, "w") as file:
            json.dump(data, file, indent=4)

        print(f'{board_token} saved')
    else:
        print(f'{board_token} failed: {response.status_code}')

# def lever_scraper()
#     'https://api.eu.lever.co/v0/postings/' + board_token + '?mode=json'
#

def main() -> None:
    YEAR = '2024'
    MONTH = '03'
    DATA_FOLDER = 'files/data'
    GREENHOUSE_TOKENS = 'files/master_data/greenhouse_tokens.txt'

    root_folder = os.path.dirname(Path(__file__).resolve().parents[0])
    target_path = root_folder / Path(DATA_FOLDER) / Path(YEAR + '_' + MONTH)

    greenhouse_board_tokens = get_board_tokens(root_folder / Path(GREENHOUSE_TOKENS))
    scrape_greenhouse_boards(target_path, greenhouse_board_tokens)




if __name__ == "__main__":
    main()

