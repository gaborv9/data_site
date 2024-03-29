
import requests
import json
import os
from pathlib import Path




def get_board_tokens(all_tokens_file_path: Path) -> list:
    with open(all_tokens_file_path, "r") as file:
        tokens = file.readlines()
    tokens = [line.strip() for line in tokens]
    return tokens


def scrape_board_tokens(name: str, target_path: Path, board_tokens: list) -> None:
    for board_token in board_tokens:
        if name == 'greenhouse':
            url = 'https://boards-api.greenhouse.io/v1/boards/' + board_token + '/jobs?content=true'
        elif name == 'lever':
            url = 'https://jobs.lever.co/v0/postings/' + board_token + '?mode=json'
        else:
            raise 'Incorrect name!'
        json_path = target_path / Path(name) / str(board_token + ".json")
        scrape_board_token(url, board_token, json_path)


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

    root_folder = os.path.dirname(Path(__file__).resolve().parents[0])
    target_path = root_folder / Path(DATA_FOLDER) / Path(YEAR + '_' + MONTH)

    # GREENHOUSE = 'greenhouse'
    # GREENHOUSE_BOARD_TOKENS = 'files/master_data/greenhouse_board_tokens.txt'
    # gr_board_tokens = get_board_tokens(root_folder / Path(GREENHOUSE_BOARD_TOKENS))
    # scrape_board_tokens(GREENHOUSE, target_path, gr_board_tokens)

    LEVER = 'lever'
    LEVER_BOARD_TOKENS = 'files/master_data/lever_board_tokens.txt'
    le_board_tokens = get_board_tokens(root_folder / Path(LEVER_BOARD_TOKENS))
    scrape_board_tokens(LEVER, target_path, le_board_tokens)

if __name__ == "__main__":
    main()

