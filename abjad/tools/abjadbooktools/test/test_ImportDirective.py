# -*- coding: utf-8 -*-
import textwrap
import unittest
from abjad.tools import abjadbooktools
from abjad.tools import stringtools


class ImportDirectiveTests(unittest.TestCase):

    def setUp(self):
        self.handler = abjadbooktools.SphinxDocumentHandler

    def test_1(self):
        source = textwrap.dedent('''
        ..  import:: abjad.tools.scoretools.make_notes
        ''')
        document = self.handler.parse_rst(source)
        result = stringtools.normalize(document.pformat())
        expected = stringtools.normalize(
            r'''
            <document source="test">
                <abjad_import_block path="abjad.tools.scoretools.make_notes">
            ''')
        self.assertEqual(result, expected)

    def test_2(self):
        source = textwrap.dedent('''
        ..  import:: abjad.tools.scoretools.make_notes
            :hide:
        ''')
        document = self.handler.parse_rst(source)
        result = stringtools.normalize(document.pformat())
        expected = stringtools.normalize(
            r'''
            <document source="test">
                <abjad_import_block hide="True" path="abjad.tools.scoretools.make_notes">
            ''')
        self.assertEqual(result, expected)
