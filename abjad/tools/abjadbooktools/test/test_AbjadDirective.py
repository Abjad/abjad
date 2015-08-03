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
                <abjad_input_block allow-exceptions hide no-stylesheet no-trim pages strip-prompt stylesheet text-width with-columns>
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
            :pages: 1-3, 5, 7-7, 10-8,
            :strip-prompt:

            assert True is False
            ''')
        document = self.handler.parse_rst(source)
        result = systemtools.TestManager.clean_string(document.pformat())
        expected = systemtools.TestManager.clean_string(
            r'''
            <document source="test">
                <abjad_input_block allow-exceptions="True" hide="True" no-stylesheet no-trim pages="(1, 2, 3, 5, 7, 10, 9, 8)" strip-prompt="True" stylesheet text-width with-columns>
                    <literal_block xml:space="preserve">
                        assert True is False
            ''')
        self.assertEqual(result, expected)

    def test_3(self):
        source = textwrap.dedent('''
        ..  abjad::
            :stylesheet: non-proportional.ly

            show(Note("c'4"))
        ''')
        document = self.handler.parse_rst(source)
        result = systemtools.TestManager.clean_string(document.pformat())
        expected = systemtools.TestManager.clean_string(
            r'''
            <document source="test">
                <abjad_input_block allow-exceptions hide no-stylesheet no-trim pages strip-prompt stylesheet="non-proportional.ly" text-width with-columns>
                    <literal_block xml:space="preserve">
                        show(Note("c'4"))
            ''')
        self.assertEqual(result, expected)

    def test_4(self):
        source = textwrap.dedent('''
        ..  abjad::
            :no-stylesheet:
            :stylesheet: non-proportional.ly

            show(Note("c'4"))
        ''')
        document = self.handler.parse_rst(source)
        result = systemtools.TestManager.clean_string(document.pformat())
        expected = systemtools.TestManager.clean_string(
            r'''
            <document source="test">
                <abjad_input_block allow-exceptions hide no-stylesheet="True" no-trim pages strip-prompt stylesheet text-width with-columns>
                    <literal_block xml:space="preserve">
                        show(Note("c'4"))
            ''')
        self.assertEqual(result, expected)