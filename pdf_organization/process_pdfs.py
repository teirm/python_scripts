#!/usr/bin/python3

"""
Purpose: This is a simple script to tame
         an unruly downloads folder and
         collect Pdfs.

Author:  Cyrus
Date:    24 October 2017
"""

import os

from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError


DOWNLOADS = '/home/teirm/Downloads'


def is_not_pdf(file_name):
    """
    Determine if the file is not a pdf.

    arg: file_name - name of the file
    returns: bool
    """
    return not file_name[-3:] == 'pdf'

def check_titles(pdfs):
    """
    Check metadata of pdfs for titles.

    arg: pdfs - list of pdfs
    returns: (list, list)
    """

    have_md = []
    no_md = []

    for file_name in pdfs:

        pdf = PdfFileReader(open(file_name, 'rb'))

        try:
            pdf_meta_data = pdf.documentInfo
        except PdfReadError:
            print('ERROR: failed to decrypt {}'
                  .format(file_name))
            continue

        if not pdf_meta_data:
            print('ERROR: no metadata for {}'
                  .format(file_name))
            continue

        if '/Title' not in pdf_meta_data.keys():
            no_md.append(file_name)
            continue

        have_md.append(file_name)

    return (have_md, no_md)


def process_pdfs():
    """
    Entry point for processing pdfs from
    the downloads folder.
    """

    pdfs = []
    not_pdfs = []

    files_dl = os.listdir(DOWNLOADS)
    os.chdir(DOWNLOADS)
    for name in files_dl:
        if is_not_pdf(name):
            not_pdfs.append(name)
            continue
        pdfs.append(name)

    print('In {} there are {} pdfs and {} not pdfs'
          .format(DOWNLOADS, len(pdfs), len(not_pdfs)))

    have_md, no_md = check_titles(pdfs)

    print('Of those that are pdfs: {} have titles and {} do not'
          .format(len(have_md), len(no_md)))


if __name__ == '__main__':
    process_pdfs()
