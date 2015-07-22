# -*- encoding: utf-8 -*-
from abjad.tools import abjadbooktools
import unittest
from abjad.tools import systemtools


class TestLaTeXDocumentHandler(unittest.TestCase):

    def test_strip_prompt_1(self):
        input_file_contents = [
            '\\begin{comment}',
            '<abjad>[strip_prompt=true]',
            'def do_something(expr):',
            "    print('before')",
            '    print(expr + 1)',
            "    print('after')",
            '',
            '</abjad>',
            '\\end{comment}',
            '',
            '\\begin{comment}',
            '<abjad>',
            'do_something(23)',
            '</abjad>',
            '\\end{comment}',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler()
        input_blocks = document_handler.collect_input_blocks(input_file_contents)
        input_blocks = tuple(input_blocks.values())
        assert input_blocks[0].strip_prompt
        assert not input_blocks[1].strip_prompt

    def test_strip_prompt_2(self):
        input_file_contents = [
            '\\begin{comment}',
            '<abjad>[strip_prompt=true]',
            'def do_something(expr):',
            "    print('before')",
            '    print(expr + 1)',
            "    print('after')",
            '',
            '</abjad>',
            '\\end{comment}',
            '',
            '\\begin{comment}',
            '<abjad>',
            'do_something(23)',
            '</abjad>',
            '\\end{comment}',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        rebuilt_source = document_handler(return_source=True)
        assert rebuilt_source == systemtools.TestManager.clean_string(
            """
            \\begin{comment}
            <abjad>[strip_prompt=true]
            def do_something(expr):
                print('before')
                print(expr + 1)
                print('after')

            </abjad>
            \\end{comment}

            %%% ABJADBOOK START %%%
            \\begin{lstlisting}
            def do_something(expr):
                print('before')
                print(expr + 1)
                print('after')
            \\end{lstlisting}
            %%% ABJADBOOK END %%%

            \\begin{comment}
            <abjad>
            do_something(23)
            </abjad>
            \\end{comment}

            %%% ABJADBOOK START %%%
            \\begin{lstlisting}
            >>> do_something(23)
            before
            24
            after
            \\end{lstlisting}
            %%% ABJADBOOK END %%%
            """,
            )