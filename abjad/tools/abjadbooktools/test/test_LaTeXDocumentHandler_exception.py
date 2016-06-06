# -*- coding: utf-8 -*-
import platform
import unittest
from abjad.tools import abjadbooktools
from abjad.tools import stringtools


@unittest.skipIf(
    platform.python_implementation() != 'CPython',
    'Only for CPython',
    )
class TestLaTeXDocumentHandler_exception(unittest.TestCase):

    maxDiff = None

    def test_exception_1(self):
        input_file_contents = [
            '<abjad>',
            "'foo' / 19",
            '</abjad>',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        self.assertRaises(
            abjadbooktools.AbjadBookError,
            document_handler.__call__,
            )

    def test_exception_2(self):
        input_file_contents = [
            '<abjad>[allow_exceptions=true]',
            "'foo' / 19",
            '</abjad>',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        rebuilt_source = document_handler(return_source=True)
        assert rebuilt_source == stringtools.normalize(
            '''
            <abjad>[allow_exceptions=true]
            'foo' / 19
            </abjad>

            %%% ABJADBOOK START %%%
            \\begin{lstlisting}
            >>> 'foo' / 19
            Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
            TypeError: unsupported operand type(s) for /: 'str' and 'int'
            \\end{lstlisting}
            %%% ABJADBOOK END %%%
            ''',
            )

    def test_exception_3(self):
        input_file_contents = [
            '<abjad>[allow_exceptions=true]',
            "'foo' / 19",
            '</abjad>',
            '',
            '<abjad>',
            "23 + 'baz'",
            '</abjad>',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        self.assertRaises(
            abjadbooktools.AbjadBookError,
            document_handler.__call__,
            )
