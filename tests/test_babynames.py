#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import soln.babynames as babynames


class TestBabynames(unittest.TestCase):

    def test_create_parser(self):
        """Check if parser can parse args"""
        p = babynames.create_parser()
        test_args = ['dummyfile1', 'dummyfile2', '--summaryfile']
        ns = p.parse_args(test_args)
        self.assertTrue(len(ns.files) == 2)
        self.assertTrue(ns.summaryfile)

    def test_extract_names(self):
        """Extraction, alphabetizing, de-duping, ranking of names from all html files"""
        # Is the function callable?
        self.assertTrue(
            callable(babynames.extract_names), msg="The extract_names function is missing")

        # Get list of only html files
        html_file_list = sorted(filter(lambda f: f.endswith('.html'), os.listdir('.')))
        # Compare each result (actual) list to expected list.
        for f in html_file_list:
            print("Checking extract_names({})".format(f))
            summary_file = os.path.join('./tests', f + '.summary')
            with open(summary_file) as sf:
                expected_list = sf.read().split('\n')
                expected_list = filter(None, expected_list)

            actual_list = babynames.extract_names(f)
            self.assertTrue(isinstance(actual_list, list),
                            msg="Returned object is not a list")

            # Remove empty strings before comparing
            actual_list = filter(None, actual_list)
            # This will perform element-by-element comparison.
            self.assertListEqual(actual_list, expected_list)
