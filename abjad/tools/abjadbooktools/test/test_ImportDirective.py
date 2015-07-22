# -*- encoding: utf-8 -*-
from abjad.tools import abjadbooktools
import textwrap
import unittest
from abjad.tools import systemtools


class ImportDirectiveTests(unittest.TestCase):

    def setUp(self):
        self.handler = abjadbooktools.SphinxDocumentHandler

    def test_1(self):
        source = textwrap.dedent('''
        ..  import:: abjad.tools.scoretools.make_notes
        ''')
        document = self.handler.parse_rst(source)
        result = systemtools.TestManager.clean_string(document.pformat())
        expected = systemtools.TestManager.clean_string(
            r'''
            <document source="test">
                <abjad_import_block hide="False" path="abjad.tools.scoretools.make_notes">
            ''')
        self.assertEqual(result, expected)

    def test_2(self):
        source = textwrap.dedent('''
        ..  import:: abjad.tools.scoretools.make_notes
            :hide:
        ''')
        document = self.handler.parse_rst(source)
        result = systemtools.TestManager.clean_string(document.pformat())
        expected = systemtools.TestManager.clean_string(
            r'''
            <document source="test">
                <abjad_import_block hide="True" path="abjad.tools.scoretools.make_notes">
            ''')
        self.assertEqual(result, expected)