# -*- encoding: utf-8 -*-
from abjad.tools import abjadbooktools
import unittest
from abjad.tools import systemtools


class TestLaTeXDocumentHandler_syntax_error(unittest.TestCase):

    def test_syntax_error_1(self):
        input_file_contents = [
            '<abjad>',
            'foo bar baz',
            '</abjad>',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        self.assertRaises(
            abjadbooktools.AbjadBookError,
            document_handler.__call__,
            )

    def test_syntax_error_2(self):
        input_file_contents = [
            '<abjad>[allow_exceptions=true]',
            'foo bar baz',
            '</abjad>',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        rebuilt_source = document_handler(return_source=True)
        assert rebuilt_source == systemtools.TestManager.clean_string(
            '''
            <abjad>[allow_exceptions=true]
            foo bar baz
            </abjad>

            %%% ABJADBOOK START %%%
            \\begin{lstlisting}
            >>> foo bar baz
              File "<stdin>", line 1
                foo bar baz
                      ^
            SyntaxError: invalid syntax
            \\end{lstlisting}
            %%% ABJADBOOK END %%%
            ''',
            )

    def test_syntax_error_3(self):
        input_file_contents = [
            '<abjad>[allow_exceptions=true]',
            'foo bar baz',
            '</abjad>',
            '',
            '<abjad>',
            'foo bar baz',
            '</abjad>',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        self.assertRaises(
            abjadbooktools.AbjadBookError,
            document_handler.__call__
            )