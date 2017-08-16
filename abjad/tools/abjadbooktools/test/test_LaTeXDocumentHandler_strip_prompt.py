import abjad
import platform
import unittest
from abjad.tools import abjadbooktools


@unittest.skipIf(
    platform.python_implementation() != 'CPython',
    'Only for CPython.',
    )
class TestLaTeXDocumentHandler(unittest.TestCase):

    maxDiff = None

    def test_strip_prompt_1(self):
        input_file_contents = [
            '\\begin{comment}',
            '<abjad>[strip_prompt=true]',
            'def do_something(argument):',
            "    print('before')",
            '    print(argument + 1)',
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
        assert input_blocks[0].code_block_specifier is not None
        assert input_blocks[0].code_block_specifier.strip_prompt
        assert input_blocks[1].code_block_specifier is None

    def test_strip_prompt_2(self):
        input_file_contents = [
            '\\begin{comment}',
            '<abjad>[strip_prompt=true]',
            'def do_something(argument):',
            "    print('before')",
            '    print(argument + 1)',
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
        assert rebuilt_source == abjad.String.normalize(
            """
            \\begin{comment}
            <abjad>[strip_prompt=true]
            def do_something(argument):
                print('before')
                print(argument + 1)
                print('after')

            </abjad>
            \\end{comment}

            %%% ABJADBOOK START %%%
            \\begin{lstlisting}
            def do_something(argument):
                print('before')
                print(argument + 1)
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
