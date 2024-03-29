
import requests
import json
import os
from pathlib import Path


def gr_scraper(target_path: Path, gr_token: str) -> None:
    NAME = 'greenhouse'
    url = 'https://boards-api.greenhouse.io/v1/boards/' + gr_token + '/jobs?content=true'
    response = requests.get(url)
    save_path = target_path / Path(NAME) / str(gr_token + ".json")
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Save the JSON data to a file
        with open(save_path, "w") as file:
            json.dump(data, file, indent=4)

        print(f'{gr_token} saved')
    else:
        print(f'{gr_token} failed: {response.status_code}')


def main() -> None:
    YEAR = '2024'
    MONTH = '03'
    DATA_FOLDER = 'files/data'
    GREENHOUSE_TOKENS = 'files/master_data/greenhouse_tokens.txt'

    root_folder = os.path.dirname(Path(__file__).resolve().parents[0])
    target_path = root_folder / Path(DATA_FOLDER) / Path(YEAR + '_' + MONTH)

    gr_tokens_path = root_folder / Path(GREENHOUSE_TOKENS)

    with open(gr_tokens_path, "r") as file:
        gr_tokens = file.readlines()
    gr_tokens_list = [line.strip() for line in gr_tokens]

    for gr_token in gr_tokens_list:
        gr_scraper(target_path, gr_token)



if __name__ == "__main__":
    main()

