# -*- coding: utf-8 -*-
import abjad
import textwrap
import unittest
from abjad.tools import abjadbooktools


class ImportDirectiveTests(unittest.TestCase):

    def setUp(self):
        self.handler = abjadbooktools.SphinxDocumentHandler

    def test_1(self):
        source = textwrap.dedent('''
        ..  import:: abjad.tools.topleveltools.attach
        ''')
        document = self.handler.parse_rst(source)
        result = abjad.String.normalize(document.pformat())
        expected = abjad.String.normalize(
            r'''
            <document source="test">
                <abjad_import_block path="abjad.tools.topleveltools.attach">
            ''')
        self.assertEqual(result, expected)

    def test_2(self):
        source = textwrap.dedent('''
        ..  import:: abjad.tools.topleveltools.attach
            :hide:
        ''')
        document = self.handler.parse_rst(source)
        result = abjad.String.normalize(document.pformat())
        expected = abjad.String.normalize(
            r'''
            <document source="test">
                <abjad_import_block hide="True" path="abjad.tools.topleveltools.attach">
            ''')
        self.assertEqual(result, expected)
