#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BabyNames python coding exercise.

__author__ = 'Mike Gabbard'
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import argparse

def extract_names(filename):
    """
    Given a single file name for babyXXXX.html, returns a single list starting
    with the year string followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    names = []
    # +++your code here+++
    with open(filename) as f:
        data = f.read()
    year = re.search(r'Popularity\sin\s(\d\d\d\d)', data).group(1)
    names.append(year)
    extracted_names = re.findall(r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>', data)
    name_dict = {}
    for item in extracted_names:
        (rank, boy, girl) = item
        name_dict[girl] = rank
        name_dict[boy] = rank
    sorted_names = sorted(name_dict.keys())

    for item in sorted_names:
        names.append(item + ' ' + name_dict[item])

    return names


def create_parser():
    """Create a cmd line parser object with 2 argument definitions"""
    parser = argparse.ArgumentParser(description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser

def main(args):
    parser = create_parser()
    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    file_list = ns.files

    create_summary = ns.summaryfile


    for file_name in file_list:
        names = extract_names(file_name)
        output = '\n'.join(names) + '\n'
        if create_summary:
            with open(file_name + '.summary', 'w') as output_file:
                output_file.write(output)
        else: 
            print(output)

if __name__ == '__main__':
    main(sys.argv[1:])