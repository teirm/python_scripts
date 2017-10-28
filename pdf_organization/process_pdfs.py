#!/usr/bin/python3

"""
Purpose: This is a simple script to tame
         an unruly downloads folder and
         collect Pdfs.

Author:  Cyrus
Date:    24 October 2017
"""

import os
import sys

from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError


DOWNLOADS = '/home/teirm/Downloads'
CS_DIR = '/home/teirm/Downloads/comp_sci'
MATH_DIR = '/home/teirm/Downloads/math'
PHIL_DIR = '/home/teirm/Downloads/phil'
UNSORTED_DIR = '/home/teirm/Downloads/unsorted'

SUB_DIRS = [CS_DIR, MATH_DIR, PHIL_DIR, UNSORTED_DIR]

MATH_KEYS = ['math', 'algebra', 'calc', 'stat', 'proof']
CS_KEYS = ['algo', 'disc', 'syst', 'cpp', 'prog', 'optim']
PHIL_KEYS = ['phil', 'logic']


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

    have_title = []
    no_title = []
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

        pdf_title = pdf_meta_data['/Title']

        if not pdf_title:
            print('{} has empty title'
                  .format(file_name))
            no_title.append(file_name)

        have_title.append((file_name, pdf_meta_data))

    return (have_title, no_title, no_md)


def check_dir(sub_dir):
    """
    Check for the existence of subject
    director and create them if
    needed.

    @param sub_dir  the subject directory
    """
    if not os.path.exists(sub_dir):
        print('Created {}'.format(sub_dir),
              file=sys.stderr)
        os.mkdir(sub_dir)


def move_pdf(pdf_path, category):
    """
    Move pdf to directory based on
    category.

    @param pdf_path     path to pdf
    @param category     category of pdf

    @return None
    """
    pdf_basename = os.path.basename(pdf_path)

    if category == 'CS':
        new_path = os.path.join(CS_DIR, pdf_basename)
    elif category == 'MATH':
        new_path = os.path.join(MATH_DIR, pdf_basename)
    elif category == 'PHIL':
        new_path = os.path.join(PHIL_DIR, pdf_basename)
    else:
        new_path = os.path.join(UNSORTED_DIR, pdf_basename)

    os.rename(pdf_path, new_path)


def organize_pdfs(have_title, no_title, no_md):
    """
    Move pdfs based on type to specific
    directories

    @param have_title[]  pdfs with titles
    @param no_title[]    pdfs without titles
    @param no_md[]       pdfs without metadata

    @return none
    """
    for sub_dir in SUB_DIRS:
        check_dir(sub_dir)

    for pdf, meta_data in have_title:
        category = process_titles(meta_data['/Title'])
        move_pdf(pdf, category)

    for pdf in no_title.extend(no_md):
        category = process_titles(pdf)
        move_pdf(pdf, category)


def process_titles(pdf_title):
    """
    Process pdfs with title metadata.

    @param pdf_path     path to the pdf
    @param pdf_title    metadata for the pdf

    @return category    categorization of pdf
    """
    for cs_key in CS_KEYS:
        if cs_key in pdf_title:
            return 'CS'

    for math_key in MATH_KEYS:
        if math_key in pdf_title:
            return 'MATH'

    for phil_key in PHIL_KEYS:
        if phil_key in pdf_title:
            return 'PHIL'

    return 'UNSORTED'


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

    have_title, no_title, no_md = check_titles(pdfs)

    print('Of those that are pdfs: {} have titles and {} do not'
          .format(len(have_title), len(no_md)))

    organize_pdfs(have_title, no_title, no_md)


if __name__ == '__main__':
    process_pdfs()
