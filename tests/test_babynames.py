#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    A Test fixture for babynames.
    Checks the create_parser, extract_names, and main functions for
    correct behavior.
"""
import sys
import os
import glob
import unittest
try:
    # python2
    from StringIO import StringIO
except ImportError:
    # python3
    from io import StringIO

# uncomment one of the lines below
# import soln.babynames as babynames
import babynames

__author__ = "madarp"


class Capturing(list):
    """Context Mgr helper for capturing stdout from a function call"""
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


class TestBabynames(unittest.TestCase):

    def get_summary_file_as_list(self, summary_file):
        """Helper function for loading a summary file as a list"""
        with open(summary_file) as sf:
            summary_list = sf.read().splitlines()
            # Remove empty strings
            summary_list = filter(None, summary_list)
            return summary_list

    def remove_extension_files(self, ext):
        """Removes all files in cwd with given extension"""
        for f in glob.glob('*' + ext):
            os.remove(f)

    def test_main_print(self):
        """Test if babynames.main() prints output list"""
        self.remove_extension_files('.summary')

        with Capturing() as output:
            babynames.main(['baby1990.html'])
        self.assertIsInstance(output, list)

        # Compare captured output to list from file
        baby1990_list = self.get_summary_file_as_list(
            os.path.join('tests', 'baby1990.html.summary')
        )
        self.assertListEqual(output, baby1990_list)

        # Also check that no summary file was created
        self.assertFalse(
            glob.glob('*.summary'),
            msg='A summary file should not be created. Just printing.'
            )

    def test_main_summary(self):
        """Test if babynames.main() creates summary files"""
        # First remove any existing summary files
        self.remove_extension_files('.summary')
        cmdline = ['--summaryfile']
        cmdline.extend(glob.glob('baby*.html'))
        babynames.main(cmdline)
        files = glob.glob('*.summary')
        self.assertEqual(len(files), 10)

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
            callable(babynames.extract_names),
            msg="The extract_names function is missing"
            )

        # Get list of only html files
        html_file_list = sorted(filter(lambda f: f.endswith('.html'), os.listdir('.')))
        # Compare each result (actual) list to expected list.
        for f in html_file_list:
            summary_file = os.path.join('tests', f + '.summary')
            expected_list = self.get_summary_file_as_list(summary_file)
            actual_list = babynames.extract_names(f)
            self.assertIsInstance(actual_list, list)
            # Remove empty strings before comparing
            actual_list = filter(None, actual_list)
            # This will perform element-by-element comparison.
            self.assertListEqual(actual_list, expected_list)
