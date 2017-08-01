# -*- coding: utf-8 -*-
import abjad
import platform
import unittest
from abjad.tools import abjadbooktools


@unittest.skipIf(
    platform.python_implementation() != 'CPython',
    'Only for CPython',
    )
class TestCase(unittest.TestCase):

    maxDiff = None

    input_file_contents = abjad.String.normalize(r'''
    foo

    \begin{comment}
    <lilypond>
    { c'4 d'4 e'4 f'4 }
    </lilypond>
    \end{comment}

    bar

    \begin{comment}
    <lilypond>[stylesheet=quux.ily]
    {
        b'1
        fs'1
    }
    </lilypond>
    \end{comment}

    baz
    ''').split('\n')

    def test_lilypond_1(self):
        document_handler = abjadbooktools.LaTeXDocumentHandler()
        input_blocks = document_handler.collect_input_blocks(
            self.input_file_contents)
        assert input_blocks == {
            (3, 5): abjadbooktools.LilyPondBlock(
                (
                    "{ c'4 d'4 e'4 f'4 }",
                    ),
                starting_line_number=5,
                ),
            (11, 16): abjadbooktools.LilyPondBlock(
                (
                    '{',
                    "    b'1",
                    "    fs'1",
                    '}',
                    ),
                image_render_specifier=abjadbooktools.ImageRenderSpecifier(
                    stylesheet='quux.ily',
                    ),
                starting_line_number=16,
                )
            }

    def test_lilypond_2(self):
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=self.input_file_contents,
            )
        rebuilt_source = document_handler(return_source=True)
        assert rebuilt_source == abjad.String.normalize(r"""
            foo

            \begin{comment}
            <lilypond>
            { c'4 d'4 e'4 f'4 }
            </lilypond>
            \end{comment}

            %%% ABJADBOOK START %%%
            \noindent\includegraphics{assets/lilypond-09540b526d368c57363f2e1774dd74e5.pdf}
            %%% ABJADBOOK END %%%

            bar

            \begin{comment}
            <lilypond>[stylesheet=quux.ily]
            {
                b'1
                fs'1
            }
            </lilypond>
            \end{comment}

            %%% ABJADBOOK START %%%
            \noindent\includegraphics{assets/lilypond-9908e347a02914cf77c6f44c3067ed7f.pdf}
            %%% ABJADBOOK END %%%

            baz
        """)
