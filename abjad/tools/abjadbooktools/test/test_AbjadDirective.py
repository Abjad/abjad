# -*- coding: utf-8 -*-
from abjad.tools import abjadbooktools
import textwrap
import unittest
from abjad.tools import stringtools


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
        result = stringtools.normalize(document.pformat())
        expected = stringtools.normalize(
            r'''
            <document source="test">
                <abjad_input_block>
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
            :no-resize:
            :no-trim:
            :strip-prompt:
            :with-thumbnail:

            note = Note("c'4")
            if True:
                note.written_pitch = "ds,"
        ''')
        document = self.handler.parse_rst(source)
        result = stringtools.normalize(document.pformat())
        expected = stringtools.normalize(
            r'''
            <document source="test">
                <abjad_input_block allow-exceptions="True" hide="True" no-resize="True" no-trim="True" strip-prompt="True" with-thumbnail="True">
                    <literal_block xml:space="preserve">
                        note = Note("c'4")
                        if True:
                            note.written_pitch = "ds,"
            ''')
        self.assertEqual(result, expected)

    def test_3(self):
        source = textwrap.dedent('''
        ..  abjad::
            :allow-exceptions:
            :hide:
            :pages: 1-3, 5, 7-7, 10-8,
            :strip-prompt:

            assert True is False
            ''')
        document = self.handler.parse_rst(source)
        result = stringtools.normalize(document.pformat())
        expected = stringtools.normalize(
            r'''
            <document source="test">
                <abjad_input_block allow-exceptions="True" hide="True" pages="(1, 2, 3, 5, 7, 10, 9, 8)" strip-prompt="True">
                    <literal_block xml:space="preserve">
                        assert True is False
            ''')
        self.assertEqual(result, expected)

    def test_4(self):
        source = textwrap.dedent('''
        ..  abjad::
            :stylesheet: non-proportional.ly

            show(Note("c'4"))
        ''')
        document = self.handler.parse_rst(source)
        result = stringtools.normalize(document.pformat())
        expected = stringtools.normalize(
            r'''
            <document source="test">
                <abjad_input_block stylesheet="non-proportional.ly">
                    <literal_block xml:space="preserve">
                        show(Note("c'4"))
            ''')
        self.assertEqual(result, expected)

    def test_5(self):
        source = textwrap.dedent('''
        ..  abjad::
            :no-stylesheet:
            :stylesheet: non-proportional.ly

            show(Note("c'4"))
        ''')
        document = self.handler.parse_rst(source)
        result = stringtools.normalize(document.pformat())
        expected = stringtools.normalize(
            r'''
            <document source="test">
                <abjad_input_block no-stylesheet="True">
                    <literal_block xml:space="preserve">
                        show(Note("c'4"))
            ''')
        self.assertEqual(result, expected)

    def test_6(self):
        source = textwrap.dedent('''
        ..  abjad::
            :text-width: 80
            :with-columns: 2

            show(Note("c'4"))
        ''')
        document = self.handler.parse_rst(source)
        result = stringtools.normalize(document.pformat())
        expected = stringtools.normalize(
            r'''
            <document source="test">
                <abjad_input_block text-width="80" with-columns="2">
                    <literal_block xml:space="preserve">
                        show(Note("c'4"))
            ''')
        self.assertEqual(result, expected)
