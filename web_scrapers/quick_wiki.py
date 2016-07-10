#!/usr/bin/python

"""
Purpose: Given user input, cleanly display the wikipedia summary for the input.
Author: Cyrus Ramavarapu
Date: 10 July 2016
"""

import sys
import pprint

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://en.wikipedia.org/wiki/"

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


def create_search_url(search_terms):
    """
    Joins the words in entered search with under scores
    and appends them to the BASE_URL

    Keyword arguments:
    search_terms -- words consisten of search

    Returns: string
    """
    underscored_string = search_terms[1]
    for term in search_terms[2:]:
        underscored_string = ('_').join([underscored_string, term])

    return BASE_URL + underscored_string

if __name__ == '__main__':
    SEARCH_URL = create_search_url(sys.argv)
    get_content(SEARCH_URL)
