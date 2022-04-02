import argparse
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import validators
from validators import ValidationFailure


def is_string_an_url(url_string: str) -> bool:
    result = validators.url(url_string)
    if isinstance(result, ValidationFailure):
        return False
    return result


def get_request(url: str) -> tuple:
    response = requests.get(url)
    return response.status_code, response.text


def parse_response(html_text: str) -> list:
    soup = BeautifulSoup(html_text, 'html.parser')
    links = []
    for selector in soup.find_all("a"):
        link = selector.get("href")
        if link is not None:
            links.append(link)
    return links


def request_and_parse_result(url: str) -> list:
    status_code, content = get_request(url)
    if status_code == 200:
        links_list = parse_response(content)
    else:
        links_list = list()
    return links_list


def main(link, log_file: str = None):
    links = {link: request_and_parse_result(link)}
    for link_in_site in links[link]:
        if is_string_an_url(link_in_site):
            links[link_in_site] = request_and_parse_result(link_in_site)
    if log_file:
        output = Path(log_file)
        with open(output, 'w') as out_file:
            for key, value in links.items():
                out_file.write(f"For this url  - {key} find next url or reason why this url doesn't work :\n")
                for href in value:
                    if is_string_an_url(href):
                        out_file.write(f"{href}\n")
                    else:
                        out_file.write(f"This string isn't url - {href}\n")
    else:
        for key, value in links.items():
            print(f"For this url  - {key} find next url or reason why this url doesn't work :\n")
            for href in value:
                if is_string_an_url(href):
                    print(f"{href}\n")
                else:
                    print(f"This string isn't url - {href}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script for parsing urls request. '
                                                 'Outputs in terminal or saved in file only url')
    parser.add_argument('--input_link', '-i',
                        help='Input link address. Ex: http://translate.google.com/',
                        default="https://translate.google.com/?hl=ru", type=str)
    parser.add_argument('--output_file', '-o',
                        help='Path to log file', type=str)
    args = parser.parse_args()

    main(link=args.input_link, log_file=args.output_file)
