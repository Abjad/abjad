# -*- coding: utf-8 -*-
import platform
import unittest
from abjad.tools import abjadbooktools
from abjad.tools import stringtools


@unittest.skipIf(
    platform.python_implementation() != 'CPython',
    'Only for CPython',
    )
class TestLaTeXDocumentHandler(unittest.TestCase):

    maxDiff = None

    def test_abjadextract_1(self):
        input_file_contents = [
            '',
            '\\begin{comment}',
            '<abjadextract abjad.tools.abjadbooktools:example_function \>',
            '\\end{comment}',
            '',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler()
        input_blocks = document_handler.collect_input_blocks(input_file_contents)
        code_block = tuple(input_blocks.values())[0]
        assert code_block.executed_lines == (
            'from abjad.tools.abjadbooktools import example_function',
            )
        assert code_block.input_file_contents == (
            'def example_function(expr):',
            "    r'''This is a multiline docstring.",
            '',
            '    This is the third line of the docstring.',
            "    '''",
            '    # This is a comment.',
            "    print('Entering example function.')",
            '    try:',
            '        expr = expr + 1',
            '    except TypeError:',
            "        print('Wrong type!')",
            '    print(expr)',
            "    print('Leaving example function.')",
            )

    def test_abjadextract_2(self):
        input_file_contents = [
            '\\begin{comment}',
            '<abjadextract abjad.tools.abjadbooktools:example_function \>',
            '\\end{comment}',
            '',
            '\\begin{comment}',
            '<abjad>[allow_exceptions=true]',
            "example_function('foo')",
            '</abjad>',
            '\\end{comment}',
            '',
            '\\begin{comment}',
            '<abjad>[allow_exceptions=true]',
            "example_function(23)",
            '</abjad>',
            '\\end{comment}',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        rebuilt_source = document_handler(return_source=True)
        assert rebuilt_source == stringtools.normalize(
            """
            \\begin{comment}
            <abjadextract abjad.tools.abjadbooktools:example_function \\>
            \\end{comment}

            %%% ABJADBOOK START %%%
            \\begin{lstlisting}
            def example_function(expr):
                r'''This is a multiline docstring.

                This is the third line of the docstring.
                '''
                # This is a comment.
                print('Entering example function.')
                try:
                    expr = expr + 1
                except TypeError:
                    print('Wrong type!')
                print(expr)
                print('Leaving example function.')
            \\end{lstlisting}
            %%% ABJADBOOK END %%%

            \\begin{comment}
            <abjad>[allow_exceptions=true]
            example_function('foo')
            </abjad>
            \\end{comment}

            %%% ABJADBOOK START %%%
            \\begin{lstlisting}
            >>> example_function('foo')
            Entering example function.
            Wrong type!
            foo
            Leaving example function.
            \\end{lstlisting}
            %%% ABJADBOOK END %%%

            \\begin{comment}
            <abjad>[allow_exceptions=true]
            example_function(23)
            </abjad>
            \\end{comment}

            %%% ABJADBOOK START %%%
            \\begin{lstlisting}
            >>> example_function(23)
            Entering example function.
            24
            Leaving example function.
            \\end{lstlisting}
            %%% ABJADBOOK END %%%
            """,
            )

    def test_abjadextract_3(self):
        input_file_contents = [
            '\\begin{comment}',
            '<abjadextract abjad.tools.abjadbooktools:example_function \>[hide=true]',
            '\\end{comment}',
            '',
            '\\begin{comment}',
            '<abjad>[allow_exceptions=true]',
            "example_function('foo')",
            '</abjad>',
            '\\end{comment}',
            '',
            '\\begin{comment}',
            '<abjad>[allow_exceptions=true]',
            "example_function(23)",
            '</abjad>',
            '\\end{comment}',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        rebuilt_source = document_handler(return_source=True)
        assert rebuilt_source == stringtools.normalize(
            """
            \\begin{comment}
            <abjadextract abjad.tools.abjadbooktools:example_function \\>[hide=true]
            \\end{comment}

            \\begin{comment}
            <abjad>[allow_exceptions=true]
            example_function('foo')
            </abjad>
            \\end{comment}

            %%% ABJADBOOK START %%%
            \\begin{lstlisting}
            >>> example_function('foo')
            Entering example function.
            Wrong type!
            foo
            Leaving example function.
            \\end{lstlisting}
            %%% ABJADBOOK END %%%

            \\begin{comment}
            <abjad>[allow_exceptions=true]
            example_function(23)
            </abjad>
            \\end{comment}

            %%% ABJADBOOK START %%%
            \\begin{lstlisting}
            >>> example_function(23)
            Entering example function.
            24
            Leaving example function.
            \\end{lstlisting}
            %%% ABJADBOOK END %%%
            """,
            )
