"""
Extract job title, content and location from json files
"""

import json
import os
import html
import re

from bs4 import BeautifulSoup

from constants import TARGET_PATH

#
# def greenhouse_extract_data():
#     name = 'greenhouse'
#     path = TARGET_PATH / name
#     zzz = os.listdir(path)


def greenhouse_extract_data():
    """
    Extract data from greenhouse json files
    """
    mypath = r'c:\PycharmProjects\data_site\data\2024_03\greenhouse\databricks.json'
    with open(mypath, 'r') as file:
        try:
            json_content = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding {mypath}: {e}")

    jobs = json_content['jobs']
    for job in jobs:
        job_title = text_cleansing(job['title'])
        job_desc = text_cleansing(job['content'])

        print(f"Job Title: {job_title}")
        print(f"Job Content: {job_desc}")
        print("------")
        break


def text_cleansing(text):
    # unescape html tags
    escaped_text = html.unescape(text)
    # remove html tags
    text_without_html_tags = BeautifulSoup(escaped_text, "html.parser").text
    # remove all non-word characters
    clean_text = re.sub(r'\W+', ' ', text_without_html_tags)
    # lowercase text
    lowercase_text = clean_text.lower()
    return lowercase_text


def main():
    greenhouse_extract_data()


if __name__ == "__main__":
    main()
