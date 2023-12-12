import os

import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError

load_dotenv()


class UrlConnector:
    def __init__(self):
        pass

    def get_json(self, url):
        try:
            response = requests.get(url, cookies={"session": os.getenv("SESSION")}).text
            # response_formatted = response.read().split('\n')
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Python 3.6
        except Exception as err:
            print(f"Other error occurred: {err}")  # Python 3.6
        else:
            return response

    def _store_text_to_file(self, file_name, response):
        with open(file_name, "w") as f:
            f.write(response)

    def download_file(self, url, file_name):
        response = self.get_json(url)
        store_file = self._store_text_to_file(file_name, response)
        return file_name


if __name__ == "__main__":
    connection_instance = UrlConnector()
    # day 1
    connection_instance.download_file("https://adventofcode.com/2023/day/1/input", "day_1.txt")
    # day 2
    connection_instance.download_file("https://adventofcode.com/2023/day/2/input", "day_2.txt")
    # day 3
    connection_instance.download_file("https://adventofcode.com/2023/day/3/input", "day_3.txt")
    # day 4
    connection_instance.download_file("https://adventofcode.com/2023/day/4/input", "day_4.txt")
    # day 5
    connection_instance.download_file("https://adventofcode.com/2023/day/5/input", "day_5.txt")
    # day 6
    connection_instance.download_file("https://adventofcode.com/2023/day/6/input", "day_6.txt")
    # day 7
    connection_instance.download_file("https://adventofcode.com/2023/day/7/input", "day_7.txt")
    # day 8
    connection_instance.download_file("https://adventofcode.com/2023/day/8/input", "day_8.txt")
    # day 9
    connection_instance.download_file("https://adventofcode.com/2023/day/9/input", "day_9.txt")
    # day 10
    connection_instance.download_file("https://adventofcode.com/2023/day/10/input", "day_10.txt")
    # day 11
    connection_instance.download_file("https://adventofcode.com/2023/day/11/input", "day_11.txt")
    # day 12
    connection_instance.download_file("https://adventofcode.com/2023/day/12/input", "day_12.txt")