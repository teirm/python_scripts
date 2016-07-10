#!/usr/bin/python

"""
Purpose: Given user input, cleanly display the wikipedia summary for the input.
Author: Cyrus Ramavarapu
Date: 10 July 2016
"""
import pprint

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://en.wikipedia.org/wiki/kittens"

def get_content(section_url):

    """
    Returns HTML content of a given site.

    Keyword arguments:
    section_url -- The desired website to be scraped.

    Returns: None
    """
    summary_pp = pprint.PrettyPrinter(width=80)
    proxy = {'http':section_url}
    response = requests.get(section_url, proxies=proxy)
    soup = BeautifulSoup(response.text, 'lxml')
    body_text = soup.find('div', {'id': 'mw-content-text'})
    paragraphs = body_text.find_all('p')
    summary = paragraphs[0].text
    summary_pp.pprint(summary)
    print(section_url)

if __name__ == '__main__':
    get_content(BASE_URL)
