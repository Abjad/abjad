# -*- coding: utf-8 -*-
import abjad
import textwrap
import unittest


class ImportDirectiveTests(unittest.TestCase):

    def setUp(self):
        self.handler = abjad.abjadbooktools.SphinxDocumentHandler

    def test_1(self):
        source = textwrap.dedent('''
        ..  import:: abjad.tools.scoretools.make_notes
        ''')
        document = self.handler.parse_rst(source)
        result = abjad.String.normalize(document.pformat())
        expected = abjad.String.normalize(
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
        result = abjad.String.normalize(document.pformat())
        expected = abjad.String.normalize(
            r'''
            <document source="test">
                <abjad_import_block hide="True" path="abjad.tools.scoretools.make_notes">
            ''')
        self.assertEqual(result, expected)
