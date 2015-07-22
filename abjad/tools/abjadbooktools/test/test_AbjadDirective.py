# -*- encoding: utf-8 -*-
from abjad.tools import abjadbooktools
import textwrap
import unittest
from abjad.tools import systemtools


class AbjadDirectiveTests(unittest.TestCase):

    def setUp(self):
        self.handler = abjadbooktools.SphinxDocumentHandler

    def test_1(self):
        source = textwrap.dedent('''
        ..  abjad::

            note = Note("c'4")
            if True:
                note.written_pitch = "ds,"
        ''')
        document = self.handler.parse_rst(source)
        result = systemtools.TestManager.clean_string(document.pformat())
        expected = systemtools.TestManager.clean_string(
            r'''
            <document source="test">
                <abjad_input_block allow-exceptions="False" hide="False" strip-prompt="False" text-width>
                    <literal_block xml:space="preserve">
                        note = Note("c'4")
                        if True:
                            note.written_pitch = "ds,"
            ''')
        self.assertEqual(result, expected)

    def test_2(self):
        source = textwrap.dedent('''
        ..  abjad::
            :allow-exceptions:
            :hide:
            :strip-prompt:

            assert True is False
            ''')
        document = self.handler.parse_rst(source)
        result = systemtools.TestManager.clean_string(document.pformat())
        expected = systemtools.TestManager.clean_string(
            r'''
            <document source="test">
                <abjad_input_block allow-exceptions="True" hide="True" strip-prompt="True" text-width>
                    <literal_block xml:space="preserve">
                        assert True is False
            ''')
        self.assertEqual(result, expected)