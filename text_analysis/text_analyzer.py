#!/usr/bin/python

"""
A simple program to analyze user loaded text data
"""

import os
import os.path
import csv

from contextlib import contextmanager


_PROCESSED_FILES = os.path.abspath('THINGS_TO_DELETE')
_AG_DATA_DIR = os.path.abspath('data')
_RAW_DATA_DIR = os.path.abspath('raw_data')
_DATA_DICTS = []


@contextmanager
def change_directory(dir_name):
    """
    Changes directory if possible and then
    changes back to current working directory
    """
    current_directory = os.getcwd()

    if os.path.isdir(dir_name):
        os.chdir(dir_name)
    else:
        os.chdir(current_directory)
        raise FileNotFoundError

    yield

    os.chdir(current_directory)


def process_data(file_ptr):
    """
    Processes the data_file for further use

    @param file_ptr -- a pointer to the data file
    """

    data_container = {}
    date = file_ptr.name.split('.')[0]

    for line in file_ptr:
        values = line.split()

        # skip the header line
        if values[0] == '#Person':
            continue

        data_container['date'] = date
        data_container['person'] = values[0]
        data_container['sent'] = values[1]
        data_container['received'] = values[2]
        data_container['mode'] = values[3]

        _DATA_DICTS.append(data_container)


def load_data():
    """
    Load data from pickle
    """
    with change_directory(_RAW_DATA_DIR):
        for file_name in os.listdir(_RAW_DATA_DIR):

            # skip the aggregate file
            if file_name == 'text_data.csv':
                continue

            with open(file_name, "r") as file_ptr:
                print(file_ptr)
                process_data(file_ptr)

            # moves processed files to into delection directory
            os.rename(file_name, os.path.join(_PROCESSED_FILES, file_name))


def write_csv():
    """
    Write the data dictionaries to a CSV file
    for use with pandas
    """

    data_keys = _DATA_DICTS[0].keys()

    with change_directory(_AG_DATA_DIR):
        with open('text_data.csv', 'a') as f_ptr:
            writer = csv.DictWriter(f_ptr, data_keys)
            writer.writerows(_DATA_DICTS)


def save_data():
    """
    Save data into tarfile
    """


def update_data():
    """
    Updates entry in data set or
    adds a new entry
    """


def text_analyzer():
    """
    Entry point for text analyzer
    """


if __name__ == '__main__':
    load_data()
    write_csv()
